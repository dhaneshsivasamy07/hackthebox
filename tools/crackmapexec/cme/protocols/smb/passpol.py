#Stolen from https://github.com/Wh1t3Fox/polenum

import logging
from impacket.dcerpc.v5.rpcrt import DCERPC_v5
from impacket.dcerpc.v5 import transport, samr 
from impacket.dcerpc.v5.samr import DCERPCSessionError
from impacket.dcerpc.v5.rpcrt import DCERPCException
from impacket import ntlm
from time import strftime, gmtime

def d2b(a):
    tbin = []
    while a:
        tbin.append(a % 2)
        a //= 2

    t2bin = tbin[::-1]
    if len(t2bin) != 8:
        for x in range(6 - len(t2bin)):
            t2bin.insert(0, 0)
    return ''.join([str(g) for g in t2bin])


def convert(low, high, lockout=False):
    time = ""
    tmp = 0

    if low == 0 and hex(high) == "-0x80000000":
        return "Not Set"
    if low == 0 and high == 0:
        return "None"

    if not lockout:
        if (low != 0):
            high = abs(high+1)
        else:
            high = abs(high)
            low = abs(low)

            tmp = low + (high)*16**8  # convert to 64bit int
            tmp *= (1e-7)  # convert to seconds
    else:
        tmp = abs(high) * (1e-7)

    try:
        minutes = int(strftime("%M", gmtime(tmp)))
        hours = int(strftime("%H", gmtime(tmp)))
        days = int(strftime("%j", gmtime(tmp)))-1
    except ValueError as e:
        return "[-] Invalid TIME"

    if days > 1:
        time += "{0} days ".format(days)
    elif days == 1:
        time += "{0} day ".format(days)
    if hours > 1:
        time += "{0} hours ".format(hours)
    elif hours == 1:
        time += "{0} hour ".format(hours)
    if minutes > 1:
        time += "{0} minutes ".format(minutes)
    elif minutes == 1:
        time += "{0} minute ".format(minutes)
    return time

class PassPolDump:

    KNOWN_PROTOCOLS = {
        '139/SMB': (r'ncacn_np:%s[\pipe\samr]', 139),
        '445/SMB': (r'ncacn_np:%s[\pipe\samr]', 445),
    }

    def __init__(self, connection):
        self.logger = connection.logger
        self.addr = connection.host
        self.protocol = connection.args.port
        self.username = connection.username
        self.password = connection.password
        self.domain = connection.domain
        self.hash = connection.hash
        self.lmhash = ''
        self.nthash = ''
        self.aesKey = None
        self.doKerberos = False
        self.protocols = PassPolDump.KNOWN_PROTOCOLS.keys()
        self.pass_pol = {}

        if self.hash is not None:
            if self.hash.find(':') != -1:
                self.lmhash, self.nthash = self.hash.split(':')
            else:
                self.nthash = self.hash
        
        if self.password is None:
            self.password = ''

    def dump(self):

        # Try all requested protocols until one works.
        for protocol in self.protocols:
            try:
                protodef = PassPolDump.KNOWN_PROTOCOLS[protocol]
                port = protodef[1]
            except KeyError:
                logging.debug("Invalid Protocol '{}'".format(protocol))
            logging.debug("Trying protocol {}".format(protocol))
            rpctransport = transport.SMBTransport(self.addr, port, r'\samr', self.username, self.password, self.domain, 
                                                  self.lmhash, self.nthash, self.aesKey, doKerberos = self.doKerberos)
            try:
                self.fetchList(rpctransport)
            except Exception as e:
                logging.debug('Protocol failed: {}'.format(e))
            else:
                # Got a response. No need for further iterations.
                self.pretty_print()
                break

        return self.pass_pol

    def fetchList(self, rpctransport):
        dce = DCERPC_v5(rpctransport)
        dce.connect()
        dce.bind(samr.MSRPC_UUID_SAMR)

        # Setup Connection
        resp = samr.hSamrConnect2(dce)
        if resp['ErrorCode'] != 0:
            raise Exception('Connect error')

        resp2 = samr.hSamrEnumerateDomainsInSamServer(dce, serverHandle=resp['ServerHandle'],
                                                      enumerationContext=0,
                                                      preferedMaximumLength=500)
        if resp2['ErrorCode'] != 0:
            raise Exception('Connect error')

        resp3 = samr.hSamrLookupDomainInSamServer(dce, serverHandle=resp['ServerHandle'],
                                                  name=resp2['Buffer']['Buffer'][0]['Name'])
        if resp3['ErrorCode'] != 0:
            raise Exception('Connect error')

        resp4 = samr.hSamrOpenDomain(dce, serverHandle=resp['ServerHandle'],
                                     desiredAccess=samr.MAXIMUM_ALLOWED,
                                     domainId=resp3['DomainId'])
        if resp4['ErrorCode'] != 0:
            raise Exception('Connect error')

        self.__domains = resp2['Buffer']['Buffer']
        domainHandle = resp4['DomainHandle']
        # End Setup

        re = samr.hSamrQueryInformationDomain2(dce, domainHandle=domainHandle,
                                               domainInformationClass=samr.DOMAIN_INFORMATION_CLASS.DomainPasswordInformation)
        self.__min_pass_len = re['Buffer']['Password']['MinPasswordLength'] or "None"
        self.__pass_hist_len = re['Buffer']['Password']['PasswordHistoryLength'] or "None"
        self.__max_pass_age = convert(int(re['Buffer']['Password']['MaxPasswordAge']['LowPart']), int(re['Buffer']['Password']['MaxPasswordAge']['HighPart']))
        self.__min_pass_age = convert(int(re['Buffer']['Password']['MinPasswordAge']['LowPart']), int(re['Buffer']['Password']['MinPasswordAge']['HighPart']))
        self.__pass_prop = d2b(re['Buffer']['Password']['PasswordProperties'])

        re = samr.hSamrQueryInformationDomain2(dce, domainHandle=domainHandle,
                                               domainInformationClass=samr.DOMAIN_INFORMATION_CLASS.DomainLockoutInformation)
        self.__rst_accnt_lock_counter = convert(0, re['Buffer']['Lockout']['LockoutObservationWindow'], lockout=True)
        self.__lock_accnt_dur = convert(0, re['Buffer']['Lockout']['LockoutDuration'], lockout=True)
        self.__accnt_lock_thres = re['Buffer']['Lockout']['LockoutThreshold'] or "None"

        re = samr.hSamrQueryInformationDomain2(dce, domainHandle=domainHandle,
                                               domainInformationClass=samr.DOMAIN_INFORMATION_CLASS.DomainLogoffInformation)
        self.__force_logoff_time = convert(re['Buffer']['Logoff']['ForceLogoff']['LowPart'], re['Buffer']['Logoff']['ForceLogoff']['HighPart'])

        self.pass_pol = {'min_pass_len': self.__min_pass_len, 'pass_hist_len': self.__pass_hist_len, 
                         'max_pass_age': self.__max_pass_age, 'min_pass_age': self.__min_pass_age, 
                         'pass_prop': self.__pass_prop, 'rst_accnt_lock_counter': self.__rst_accnt_lock_counter,
                         'lock_accnt_dur': self.__lock_accnt_dur, 'accnt_lock_thres': self.__accnt_lock_thres,
                         'force_logoff_time': self.__force_logoff_time}

    def pretty_print(self):

        PASSCOMPLEX = {
            5: 'Domain Password Complex:',
            4: 'Domain Password No Anon Change:',
            3: 'Domain Password No Clear Change:',
            2: 'Domain Password Lockout Admins:',
            1: 'Domain Password Store Cleartext:',
            0: 'Domain Refuse Password Change:'
        }

        logging.debug('Found domain(s):')
        for domain in self.__domains:
            logging.debug('{}'.format(domain['Name']))

        self.logger.success("Dumping password info for domain: {}".format(self.__domains[0]['Name']))

        self.logger.highlight("Minimum password length: {}".format(self.__min_pass_len))
        self.logger.highlight("Password history length: {}".format(self.__pass_hist_len))
        self.logger.highlight("Maximum password age: {}".format(self.__max_pass_age))
        self.logger.highlight('')
        self.logger.highlight("Password Complexity Flags: {}".format(self.__pass_prop or "None"))

        for i, a in enumerate(self.__pass_prop):
            self.logger.highlight("\t{} {}".format(PASSCOMPLEX[i], str(a)))

        self.logger.highlight('')
        self.logger.highlight("Minimum password age: {}".format(self.__min_pass_age))
        self.logger.highlight("Reset Account Lockout Counter: {}".format(self.__rst_accnt_lock_counter))
        self.logger.highlight("Locked Account Duration: {}".format(self.__lock_accnt_dur))
        self.logger.highlight("Account Lockout Threshold: {}".format(self.__accnt_lock_thres))
        self.logger.highlight("Forced Log off Time: {}".format(self.__force_logoff_time))