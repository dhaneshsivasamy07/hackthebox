import unittest
import os
import socket
import select
import errno

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

from binascii import unhexlify
from impacket.smbconnection import SMBConnection, smb
from impacket.smb3structs import SMB2_DIALECT_002,SMB2_DIALECT_21, SMB2_DIALECT_30
from impacket import nt_errors, nmb

# IMPORTANT NOTE:
# For some reason, under Windows 8, you cannot switch between
# dialects 002, 2_1 and 3_0 (it will throw STATUS_USER_SESSION_DELETED),
# but you can with SMB1.
# So, you can't run all test cases against the same machine.
# Usually running all the tests against a Windows 7 except SMB3
# would do the trick.
# ToDo:
# [ ] Add the rest of SMBConnection public methods

class SMBTests(unittest.TestCase):
    def create_connection(self):
        if self.dialects == smb.SMB_DIALECT:
            # Only for SMB1 let's do manualNego
            s = SMBConnection(self.serverName, self.machine, preferredDialect = self.dialects, sess_port = self.sessPort, manualNegotiate=True)
            s.negotiateSession(self.dialects, flags2=self.flags2)
        else:
            s = SMBConnection(self.serverName, self.machine, preferredDialect = self.dialects, sess_port = self.sessPort)
        return s

    def test_aliasconnection(self):
        smb = SMBConnection('*SMBSERVER', self.machine, preferredDialect=self.dialects, sess_port=self.sessPort)
        smb.login(self.username, self.password, self.domain)
        smb.listPath(self.share, '*')
        smb.logoff()

    def test_reconnect(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        smb.listPath(self.share, '*')
        smb.logoff()
        smb.reconnect()
        smb.listPath(self.share, '*')
        smb.logoff()

    def test_reconnectKerberosHashes(self):
        lmhash, nthash = self.hashes.split(':')
        smb = self.create_connection()
        smb.kerberosLogin(self.username, '', self.domain, lmhash, nthash, '')
        credentials = smb.getCredentials()
        self.assertTrue( credentials == (self.username, '', self.domain, unhexlify(lmhash), unhexlify(nthash), '', None, None) )
        UNC = '\\\\%s\\%s' % (self.machine, self.share)
        smb.connectTree(UNC)
        smb.logoff()
        smb.reconnect()
        credentials = smb.getCredentials()
        self.assertTrue(
            credentials == (self.username, '', self.domain, unhexlify(lmhash), unhexlify(nthash), '', None, None))
        UNC = '\\\\%s\\%s' % (self.machine, self.share)
        smb.connectTree(UNC)
        smb.logoff()

    def test_connectTree(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        smb.connectTree(self.share)
        UNC = '\\\\%s\\%s' % (self.machine, self.share)
        smb.connectTree(UNC)

    def test_connection(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        credentials = smb.getCredentials()
        self.assertTrue( credentials == (self.username, self.password, self.domain, '','','', None, None))
        smb.logoff()
        del(smb)
        
    def test_close_connection(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        smb_connection_socket = smb.getSMBServer().get_socket()
        self.assertTrue(self.__is_socket_opened(smb_connection_socket) == True)
        smb.close()
        self.assertTrue(self.__is_socket_opened(smb_connection_socket) == False)
        del(smb)

    def test_manualNego(self):
        smb = self.create_connection()
        smb.negotiateSession(self.dialects)
        smb.login(self.username, self.password, self.domain)
        credentials = smb.getCredentials()
        self.assertTrue( credentials == (self.username, self.password, self.domain, '','','', None, None))
        smb.logoff()
        del(smb)

    def test_loginHashes(self):
        lmhash, nthash = self.hashes.split(':')
        smb = self.create_connection()
        smb.login(self.username, '', self.domain, lmhash, nthash)
        credentials = smb.getCredentials()
        self.assertTrue( credentials == (self.username, '', self.domain, unhexlify(lmhash), unhexlify(nthash), '', None, None) )
        smb.logoff()

    def test_loginKerberosHashes(self):
        lmhash, nthash = self.hashes.split(':')
        smb = self.create_connection()
        smb.kerberosLogin(self.username, '', self.domain, lmhash, nthash, '')
        credentials = smb.getCredentials()
        self.assertTrue( credentials == (self.username, '', self.domain, unhexlify(lmhash), unhexlify(nthash), '', None, None) )
        UNC = '\\\\%s\\%s' % (self.machine, self.share)
        smb.connectTree(UNC)
        smb.logoff()

    def test_loginKerberos(self):
        smb = self.create_connection()
        smb.kerberosLogin(self.username, self.password, self.domain, '', '', '')
        credentials = smb.getCredentials()
        self.assertTrue( credentials == (self.username, self.password, self.domain, '','','', None, None) )
        UNC = '\\\\%s\\%s' % (self.machine, self.share)
        smb.connectTree(UNC)
        smb.logoff()

    def test_loginKerberosAES(self):
        smb = self.create_connection()
        smb.kerberosLogin(self.username, '', self.domain, '', '', self.aesKey)
        credentials = smb.getCredentials()
        self.assertTrue( credentials == (self.username, '', self.domain, '','',self.aesKey, None, None) )
        UNC = '\\\\%s\\%s' % (self.machine, self.share)
        smb.connectTree(UNC)
        smb.logoff()

    def test_listPath(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        smb.listPath(self.share, '*')
        smb.logoff()

    def test_createFile(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        tid = smb.connectTree(self.share)
        fid = smb.createFile(tid, self.file)
        smb.closeFile(tid,fid)
        smb.rename(self.share, self.file, self.file + '.bak')
        smb.deleteFile(self.share, self.file + '.bak')
        smb.disconnectTree(tid)
        smb.logoff()
        
    def test_readwriteFile(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        tid = smb.connectTree(self.share)
        fid = smb.createFile(tid, self.file)
        smb.writeFile(tid, fid, "A"*65535)
        data = b''
        offset = 0
        remaining = 65535
        while remaining>0:
            data += smb.readFile(tid,fid, offset, remaining)
            remaining = 65535 - len(data)
        self.assertTrue(len(data) == 65535)
        self.assertTrue(data == b"A"*65535)
        smb.closeFile(tid,fid)
        fid = smb.openFile(tid, self.file)
        smb.closeFile(tid, fid)
        smb.deleteFile(self.share, self.file)
        smb.disconnectTree(tid)
        
        smb.logoff()
         
    def test_createdeleteDirectory(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        smb.createDirectory(self.share, self.directory)
        smb.deleteDirectory(self.share, self.directory)
        smb.createDirectory(self.share, self.directory)
        nested_dir = "%s\\%s" %(self.directory, self.directory)
        smb.createDirectory(self.share, nested_dir)
        try:
            smb.deleteDirectory(self.share, self.directory)
        except Exception as e:
            if e.error == nt_errors.STATUS_DIRECTORY_NOT_EMPTY:
                smb.deleteDirectory(self.share, nested_dir)
                smb.deleteDirectory(self.share, self.directory)
        smb.logoff()
 
    def test_getData(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        smb.getDialect()
        smb.getServerName()
        smb.getRemoteHost()
        smb.getServerDomain()
        smb.getServerOS()
        smb.doesSupportNTLMv2()
        smb.isLoginRequired()
        smb.logoff()

    def test_getServerName(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        serverName = smb.getServerName()
        self.assertTrue( serverName.upper() == self.serverName.upper() )
        smb.logoff()

    def test_getServerDNSDomainName(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        serverDomain = smb.getServerDNSDomainName()
        self.assertTrue( serverDomain.upper() == self.domain.upper())
        smb.logoff()

    def test_getServerDomain(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        serverDomain = smb.getServerDomain()
        self.assertTrue( serverDomain.upper() == self.domain.upper().split('.')[0])
        smb.logoff()

    def test_getRemoteHost(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        remoteHost = smb.getRemoteHost()
        self.assertTrue( remoteHost == self.machine)
        smb.logoff()

    def test_getDialect(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        dialect = smb.getDialect()
        self.assertTrue( dialect == self.dialects)
        smb.logoff()

    def test_uploadDownload(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        f = open(self.upload)
        smb.putFile(self.share, self.file, f.read)
        f.close()
        f = open(self.upload + '2', 'wb+')
        smb.getFile(self.share, self.file, f.write)
        f.close()
        os.unlink(self.upload + '2')
        smb.deleteFile(self.share, self.file)
        smb.logoff()

    def test_listShares(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        smb.listShares()
        smb.logoff()

    def test_getSessionKey(self):
        smb = self.create_connection()
        smb.login(self.username, self.password, self.domain)
        smb.getSessionKey()
        smb.logoff
        
    def __is_socket_opened(self, s):
        # We assume that if socket is selectable, it's open; and if it were not, it's closed.
        # Note: this method is accurate as long as the file descriptor used for the socket is not re-used
        is_socket_opened = True 
        try:
            select.select([s], [], [], 0)
        except socket.error as e:
            if e.errno == errno.EBADF:
                is_socket_opened = False
        except ValueError:
            is_socket_opened = False
        return is_socket_opened

class SMB1Tests(SMBTests):
    def setUp(self):
        SMBTests.setUp(self)
        # Put specific configuration for target machine with SMB1
        configFile = ConfigParser.ConfigParser()
        configFile.read('dcetests.cfg')
        self.username = configFile.get('SMBTransport', 'username')
        self.domain   = configFile.get('SMBTransport', 'domain')
        self.serverName = configFile.get('SMBTransport', 'servername')
        self.password = configFile.get('SMBTransport', 'password')
        self.machine  = configFile.get('SMBTransport', 'machine')
        self.hashes   = configFile.get('SMBTransport', 'hashes')
        self.aesKey   = configFile.get('SMBTransport', 'aesKey128')
        self.share    = 'C$'
        self.file     = '/TEST'
        self.directory= '/BETO'
        self.upload   = '../../impacket/nt_errors.py'
        self.flags2   = smb.SMB.FLAGS2_NT_STATUS | smb.SMB.FLAGS2_EXTENDED_SECURITY | smb.SMB.FLAGS2_LONG_NAMES
        self.dialects = smb.SMB_DIALECT
        self.sessPort = nmb.SMB_SESSION_PORT

class SMB1TestsNetBIOS(SMBTests):
    def setUp(self):
        SMBTests.setUp(self)
        # Put specific configuration for target machine with SMB1
        configFile = ConfigParser.ConfigParser()
        configFile.read('dcetests.cfg')
        self.username = configFile.get('SMBTransport', 'username')
        self.domain   = configFile.get('SMBTransport', 'domain')
        self.serverName = configFile.get('SMBTransport', 'servername')
        self.password = configFile.get('SMBTransport', 'password')
        self.machine  = configFile.get('SMBTransport', 'machine')
        self.hashes   = configFile.get('SMBTransport', 'hashes')
        self.aesKey   = configFile.get('SMBTransport', 'aesKey128')
        self.share    = 'C$'
        self.file     = '/TEST'
        self.directory= '/BETO'
        self.upload   = '../../impacket/nt_errors.py'
        self.flags2   = smb.SMB.FLAGS2_NT_STATUS | smb.SMB.FLAGS2_EXTENDED_SECURITY | smb.SMB.FLAGS2_LONG_NAMES
        self.dialects = smb.SMB_DIALECT
        self.sessPort = nmb.NETBIOS_SESSION_PORT

class SMB1TestsUnicode(SMBTests):
    def setUp(self):
        SMBTests.setUp(self)
        # Put specific configuration for target machine with SMB1
        configFile = ConfigParser.ConfigParser()
        configFile.read('dcetests.cfg')
        self.username = configFile.get('SMBTransport', 'username')
        self.domain   = configFile.get('SMBTransport', 'domain')
        self.serverName = configFile.get('SMBTransport', 'servername')
        self.password = configFile.get('SMBTransport', 'password')
        self.machine  = configFile.get('SMBTransport', 'machine')
        self.hashes   = configFile.get('SMBTransport', 'hashes')
        self.aesKey   = configFile.get('SMBTransport', 'aesKey128')
        self.share    = 'C$'
        self.file     = '/TEST'
        self.directory= '/BETO'
        self.upload   = '../../impacket/nt_errors.py'
        self.flags2   = smb.SMB.FLAGS2_UNICODE | smb.SMB.FLAGS2_NT_STATUS | smb.SMB.FLAGS2_EXTENDED_SECURITY | smb.SMB.FLAGS2_LONG_NAMES
        self.dialects = smb.SMB_DIALECT
        self.sessPort = nmb.SMB_SESSION_PORT

class SMB002Tests(SMBTests):
    def setUp(self):
        # Put specific configuration for target machine with SMB_002
        SMBTests.setUp(self)
        configFile = ConfigParser.ConfigParser()
        configFile.read('dcetests.cfg')
        self.username = configFile.get('SMBTransport', 'username')
        self.domain   = configFile.get('SMBTransport', 'domain')
        self.serverName = configFile.get('SMBTransport', 'servername')
        self.password = configFile.get('SMBTransport', 'password')
        self.machine  = configFile.get('SMBTransport', 'machine')
        self.hashes   = configFile.get('SMBTransport', 'hashes')
        self.aesKey   = configFile.get('SMBTransport', 'aesKey128')
        self.share    = 'C$'
        self.file     = '/TEST'
        self.directory= '/BETO'
        self.upload   = '../../impacket/nt_errors.py'
        self.dialects = SMB2_DIALECT_002
        self.sessPort = nmb.SMB_SESSION_PORT

class SMB21Tests(SMBTests):
    def setUp(self):
        # Put specific configuration for target machine with SMB 2.1
        SMBTests.setUp(self)
        configFile = ConfigParser.ConfigParser()
        configFile.read('dcetests.cfg')
        self.username = configFile.get('SMBTransport', 'username')
        self.domain   = configFile.get('SMBTransport', 'domain')
        self.serverName = configFile.get('SMBTransport', 'servername')
        self.password = configFile.get('SMBTransport', 'password')
        self.machine  = configFile.get('SMBTransport', 'machine')
        self.hashes   = configFile.get('SMBTransport', 'hashes')
        self.aesKey   = configFile.get('SMBTransport', 'aesKey128')
        self.share    = 'C$'
        self.file     = '/TEST'
        self.directory= '/BETO'
        self.upload   = '../../impacket/nt_errors.py'
        self.dialects = SMB2_DIALECT_21
        self.sessPort = nmb.SMB_SESSION_PORT

class SMB3Tests(SMBTests):
    def setUp(self):
        # Put specific configuration for target machine with SMB3
        SMBTests.setUp(self)
        configFile = ConfigParser.ConfigParser()
        configFile.read('dcetests.cfg')
        self.username = configFile.get('SMBTransport', 'username')
        self.domain   = configFile.get('SMBTransport', 'domain')
        self.serverName = configFile.get('SMBTransport', 'servername')
        self.password = configFile.get('SMBTransport', 'password')
        self.machine  = configFile.get('SMBTransport', 'machine')
        self.hashes   = configFile.get('SMBTransport', 'hashes')
        self.aesKey   = configFile.get('SMBTransport', 'aesKey128')
        self.share    = 'C$'
        self.file     = '/TEST'
        self.directory= '/BETO'
        self.upload   = '../../impacket/nt_errors.py'
        self.dialects = SMB2_DIALECT_30
        self.sessPort = nmb.SMB_SESSION_PORT

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(SMB1Tests)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SMB1TestsNetBIOS))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SMB1TestsUnicode))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SMB002Tests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SMB21Tests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SMB3Tests))
    unittest.TextTestRunner(verbosity=1).run(suite)
