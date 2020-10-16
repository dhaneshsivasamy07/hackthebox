# SECUREAUTH LABS. Copyright 2018 SecureAuth Corporation. All rights reserved.
#
# This software is provided under under a slightly modified version
# of the Apache Software License. See the accompanying LICENSE file
# for more information.
#
# Description: Mini shell using some of the LDAP functionalities of the library
#
# Author:
#  Mathieu Gascon-Lefebvre (@mlefebvre)
#
#
import string
import sys
import cmd
import random
import ldap3
from ldap3.core.results import RESULT_UNWILLING_TO_PERFORM
from ldap3.utils.conv import escape_filter_chars
from six import PY2
import shlex
from impacket import LOG
from ldap3.protocol.microsoft import security_descriptor_control
from impacket.ldap.ldaptypes import ACCESS_ALLOWED_OBJECT_ACE, ACCESS_MASK, ACCESS_ALLOWED_ACE, ACE, OBJECTTYPE_GUID_MAP
from impacket.ldap import ldaptypes


class LdapShell(cmd.Cmd):
    LDAP_MATCHING_RULE_IN_CHAIN = "1.2.840.113556.1.4.1941"

    def __init__(self, tcp_shell, domain_dumper, client):
        cmd.Cmd.__init__(self, stdin=tcp_shell.stdin, stdout=tcp_shell.stdout)

        if PY2:
            # switch to unicode.
            reload(sys) # noqa: F821 pylint:disable=undefined-variable
            sys.setdefaultencoding('utf8')

        sys.stdout = tcp_shell.stdout
        sys.stdin = tcp_shell.stdin
        sys.stderr = tcp_shell.stdout
        self.use_rawinput = False
        self.shell = tcp_shell

        self.prompt = '\n# '
        self.tid = None
        self.intro = 'Type help for list of commands'
        self.loggedIn = True
        self.last_output = None
        self.completion = []
        self.client = client
        self.domain_dumper = domain_dumper

    def emptyline(self):
        pass

    def onecmd(self, s):
        ret_val = False
        try:
            ret_val = cmd.Cmd.onecmd(self, s)
        except Exception as e:
            print(e)
            LOG.error(e)
            LOG.debug('Exception info', exc_info=True)

        return ret_val

    def create_allow_ace(self, sid):
        nace = ldaptypes.ACE()
        nace['AceType'] = ldaptypes.ACCESS_ALLOWED_ACE.ACE_TYPE
        nace['AceFlags'] = 0x00
        acedata = ldaptypes.ACCESS_ALLOWED_ACE()
        acedata['Mask'] = ldaptypes.ACCESS_MASK()
        acedata['Mask']['Mask'] = 983551 # Full control
        acedata['Sid'] = ldaptypes.LDAP_SID()
        acedata['Sid'].fromCanonical(sid)
        nace['Ace'] = acedata
        return nace

    def do_write_gpo_dacl(self,line):
        args = shlex.split(line)
        print ("Adding %s to GPO with GUID %s" % (args[0], args[1]))
        if len(args) != 2:
            raise Exception("A samaccountname and GPO sid are required.")

        tgtUser = args[0]
        gposid = args[1]
        self.client.search(self.domain_dumper.root, '(&(objectclass=person)(sAMAccountName=%s))' % tgtUser, attributes=['objectSid'])
        if len( self.client.entries) <= 0:
            raise Exception("Didnt find the given user")

        user = self.client.entries[0]

        controls = security_descriptor_control(sdflags=0x04)
        self.client.search(self.domain_dumper.root, '(&(objectclass=groupPolicyContainer)(name=%s))' % gposid, attributes=['objectSid','nTSecurityDescriptor'], controls=controls)

        if len( self.client.entries) <= 0:
            raise Exception("Didnt find the given gpo")
        gpo = self.client.entries[0]

        secDescData = gpo['nTSecurityDescriptor'].raw_values[0]
        secDesc = ldaptypes.SR_SECURITY_DESCRIPTOR(data=secDescData)
        newace = self.create_allow_ace(str(user['objectSid']))
        secDesc['Dacl']['Data'].append(newace)
        data = secDesc.getData()

        self.client.modify(gpo.entry_dn, {'nTSecurityDescriptor':(ldap3.MODIFY_REPLACE, [data])}, controls=controls)
        if self.client.result["result"] == 0:
            print('LDAP server claims to have taken the secdescriptor. Have fun')
        else:
            raise Exception("Something wasnt right: %s" %str(self.client.result['description']))

    def do_add_user(self, line):
        args = shlex.split(line)
        if len(args) == 0:
            raise Exception("A username is required.")

        new_user = args[0]
        if len(args) == 1:
            parent_dn = 'CN=Users,%s' % self.domain_dumper.root
        else:
            parent_dn = args[1]

        new_password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(15))

        new_user_dn = 'CN=%s,%s' % (new_user, parent_dn)
        ucd = {
            'objectCategory': 'CN=Person,CN=Schema,CN=Configuration,%s' % self.domain_dumper.root,
            'distinguishedName': new_user_dn,
            'cn': new_user,
            'sn': new_user,
            'givenName': new_user,
            'displayName': new_user,
            'name': new_user,
            'userAccountControl': 512,
            'accountExpires': '0',
            'sAMAccountName': new_user,
            'unicodePwd': '"{}"'.format(new_password).encode('utf-16-le')
        }

        print('Attempting to create user in: %s', parent_dn)
        res = self.client.add(new_user_dn, ['top', 'person', 'organizationalPerson', 'user'], ucd)
        if not res:
            if self.client.result['result'] == RESULT_UNWILLING_TO_PERFORM and not self.client.server.ssl:
                raise Exception('Failed to add a new user. The server denied the operation. Try relaying to LDAP with TLS enabled (ldaps) or escalating an existing user.')
            else:
                raise Exception('Failed to add a new user: %s' % str(self.client.result['description']))
        else:
            print('Adding new user with username: %s and password: %s result: OK' % (new_user, new_password))

    def do_add_user_to_group(self, line):
        user_name, group_name = shlex.split(line)

        user_dn = self.get_dn(user_name)
        if not user_dn:
            raise Exception("User not found in LDAP: %s" % user_name)

        group_dn = self.get_dn(group_name)
        if not group_dn:
            raise Exception("Group not found in LDAP: %s" % group_name)

        user_name = user_dn.split(',')[0][3:]
        group_name = group_dn.split(',')[0][3:]

        res = self.client.modify(group_dn, {'member': [(ldap3.MODIFY_ADD, [user_dn])]})
        if res:
            print('Adding user: %s to group %s result: OK' % (user_name, group_name))
        else:
            raise Exception('Failed to add user to %s group: %s' % (group_name, str(self.client.result['description'])))

    def do_dump(self, line):
        print('Dumping domain info...')
        self.stdout.flush()
        self.domain_dumper.domainDump()
        print('Domain info dumped into lootdir!')

    def do_search(self, line):
        arguments = shlex.split(line)
        if len(arguments) == 0:
            raise Exception("A query is required.")

        filter_attributes = ['name', 'distinguishedName', 'sAMAccountName']
        attributes = filter_attributes[:]
        attributes.append('objectSid')
        for argument in arguments[1:]:
            attributes.append(argument)

        search_query = "".join("(%s=*%s*)" % (attribute, escape_filter_chars(arguments[0])) for attribute in filter_attributes)
        self.search('(|%s)' % search_query, *attributes)

    def do_get_user_groups(self, user_name):
        user_dn = self.get_dn(user_name)
        if not user_dn:
            raise Exception("User not found in LDAP: %s" % user_name)

        self.search('(member:%s:=%s)' % (LdapShell.LDAP_MATCHING_RULE_IN_CHAIN, escape_filter_chars(user_dn)))

    def do_get_group_users(self, group_name):
        group_dn = self.get_dn(group_name)
        if not group_dn:
            raise Exception("Group not found in LDAP: %s" % group_name)

        self.search('(memberof:%s:=%s)' % (LdapShell.LDAP_MATCHING_RULE_IN_CHAIN, escape_filter_chars(group_dn)), "sAMAccountName", "name")

    def search(self, query, *attributes):
        self.client.search(self.domain_dumper.root, query, attributes=attributes)
        for entry in self.client.entries:
            print(entry.entry_dn)
            for attribute in attributes:
                value = entry[attribute].value
                if value:
                    print("%s: %s" % (attribute, entry[attribute].value))
            if any(attributes):
                print("---")

    def get_dn(self, sam_name):
        if "," in sam_name:
            return sam_name

        try:
            self.client.search(self.domain_dumper.root, '(sAMAccountName=%s)' % escape_filter_chars(sam_name), attributes=['objectSid'])
            return self.client.entries[0].entry_dn
        except IndexError:
            return None

    def do_exit(self, line):
        if self.shell is not None:
            self.shell.close()
        return True

    def do_help(self, line):
        print("""
 add_user new_user [parent] - Creates a new user.
 add_user_to_group user group - Adds a user to a group.
 dump - Dumps the domain.
 search query [attributes,] - Search users and groups by name, distinguishedName and sAMAccountName.
 get_user_groups user - Retrieves all groups this user is a member of.
 get_group_users group - Retrieves all members of a group.
 write_gpo_dacl user gpoSID - Write a full control ACE to the gpo for the given user. The gpoSID must be entered surrounding by {}.
 exit - Terminates this session.""")

    def do_EOF(self, line):
        print('Bye!\n')
        return True
