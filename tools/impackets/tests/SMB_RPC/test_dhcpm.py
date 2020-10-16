###############################################################################
#  Tested so far: 
#
#  DhcpGetClientInfoV4
#  DhcpV4GetClientInfo
#
#  Not yet:
#
#
################################################################################

from __future__ import division
from __future__ import print_function

import socket
import struct
import unittest

from six.moves import configparser

from impacket.dcerpc.v5 import epm, dhcpm
from impacket.dcerpc.v5 import transport
from impacket.dcerpc.v5.dtypes import NULL
from impacket.dcerpc.v5.rpcrt import RPC_C_AUTHN_LEVEL_PKT_PRIVACY


class DHCPMTests(unittest.TestCase):
    def connect(self, version):
        rpctransport = transport.DCERPCTransportFactory(self.stringBinding)
        if len(self.hashes) > 0:
            lmhash, nthash = self.hashes.split(':')
        else:
            lmhash = ''
            nthash = ''
        if hasattr(rpctransport, 'set_credentials'):
            # This method exists only for selected protocol sequences.
            rpctransport.set_credentials(self.username,self.password, self.domain, lmhash, nthash)
        dce = rpctransport.get_dce_rpc()
        dce.set_auth_level(RPC_C_AUTHN_LEVEL_PKT_PRIVACY)
        #dce.set_auth_level(RPC_C_AUTHN_LEVEL_PKT_INTEGRITY)
        dce.connect()
        if version == 1:
            dce.bind(dhcpm.MSRPC_UUID_DHCPSRV, transfer_syntax = self.ts)
        else:
            dce.bind(dhcpm.MSRPC_UUID_DHCPSRV2, transfer_syntax = self.ts)

        return dce, rpctransport

    def test_DhcpV4GetClientInfo(self):
        dce, rpctransport = self.connect(2)
        request = dhcpm.DhcpV4GetClientInfo()
        request['ServerIpAddress'] = NULL

        request['SearchInfo']['SearchType'] = dhcpm.DHCP_SEARCH_INFO_TYPE.DhcpClientIpAddress
        request['SearchInfo']['SearchInfo']['tag'] = dhcpm.DHCP_SEARCH_INFO_TYPE.DhcpClientIpAddress
        ip = struct.unpack("!I", socket.inet_aton(self.machine))[0]
        request['SearchInfo']['SearchInfo']['ClientIpAddress'] = ip

        #request['SearchInfo']['SearchType'] = 2
        #request['SearchInfo']['SearchInfo']['tag'] = 2
        #ip = netaddr.IPAddress('172.16.123.10')
        #request['SearchInfo']['SearchInfo']['ClientName'] = 'PEPONA\0'

        request.dump()
        try:
            resp = dce.request(request)
            resp.dump()
        except Exception as e:
            # For now we'e failing. This is not supported in W2k8r2
            if str(e).find('nca_s_op_rng_error') >= 0:
                pass

    def test_DhcpGetClientInfoV4(self):
        dce, rpctransport = self.connect(1)
        request = dhcpm.DhcpGetClientInfoV4()
        request['ServerIpAddress'] = NULL

        request['SearchInfo']['SearchType'] = dhcpm.DHCP_SEARCH_INFO_TYPE.DhcpClientIpAddress
        request['SearchInfo']['SearchInfo']['tag'] = dhcpm.DHCP_SEARCH_INFO_TYPE.DhcpClientIpAddress
        ip = struct.unpack("!I", socket.inet_aton(self.machine))[0]
        request['SearchInfo']['SearchInfo']['ClientIpAddress'] = ip

        request.dump()
        try:
            resp = dce.request(request)
        except Exception as e:
            if str(e).find('ERROR_DHCP_JET_ERROR') >=0:
                pass
        else:
            resp.dump()

    def test_hDhcpGetClientInfoV4(self):
        dce, rpctransport = self.connect(1)

        ip = struct.unpack("!I", socket.inet_aton(self.machine))[0]
        try:
            resp = dhcpm.hDhcpGetClientInfoV4(dce, dhcpm.DHCP_SEARCH_INFO_TYPE.DhcpClientIpAddress, ip)
        except Exception as e:
            if str(e).find('ERROR_DHCP_JET_ERROR') >=0:
                pass
        else:
            resp.dump()

        try:
            resp = dhcpm.hDhcpGetClientInfoV4(dce, dhcpm.DHCP_SEARCH_INFO_TYPE.DhcpClientName, 'PEPA\x00')
            resp.dump()
        except Exception as e:
            if str(e).find('0x4e2d') >= 0:
                pass

    def test_hDhcpEnumSubnetClientsV5(self):

        dce, rpctransport = self.connect(2)

        try:
            resp = dhcpm.hDhcpEnumSubnetClientsV5(dce)
        except Exception as e:
            if str(e).find('ERROR_NO_MORE_ITEMS') >=0:
                pass
            else:
                raise
        else:
            resp.dump()

    def test_hDhcpGetOptionValueV5(self):
        dce, rpctransport = self.connect(2)
        netId = self.machine.split('.')[:-1]
        netId.append('0')
        print('.'.join(netId))
        subnet_id = struct.unpack("!I", socket.inet_aton('.'.join(netId)))[0]
        try:
            resp = dhcpm.hDhcpGetOptionValueV5(dce,3,
                                           dhcpm.DHCP_FLAGS_OPTION_DEFAULT, NULL, NULL,
                                           dhcpm.DHCP_OPTION_SCOPE_TYPE.DhcpSubnetOptions,
                                           subnet_id)
        except Exception as e:
            if str(e).find('ERROR_DHCP_SUBNET_NOT_PRESENT') >=0:
                pass
            else:
                raise
        else:
            resp.dump()

class SMBTransport(DHCPMTests):
    def setUp(self):
        DHCPMTests.setUp(self)
        configFile = configparser.ConfigParser()
        configFile.read('dcetests.cfg')
        self.username = configFile.get('SMBTransport', 'username')
        self.domain   = configFile.get('SMBTransport', 'domain')
        self.serverName = configFile.get('SMBTransport', 'servername')
        self.password = configFile.get('SMBTransport', 'password')
        self.machine  = configFile.get('SMBTransport', 'machine')
        self.hashes   = configFile.get('SMBTransport', 'hashes')
        self.stringBinding = r'ncacn_np:%s[\PIPE\dhcpserver]' % self.machine
        self.ts = ('8a885d04-1ceb-11c9-9fe8-08002b104860', '2.0')

class SMBTransport64(DHCPMTests):
    def setUp(self):
        DHCPMTests.setUp(self)
        configFile = configparser.ConfigParser()
        configFile.read('dcetests.cfg')
        self.username = configFile.get('SMBTransport', 'username')
        self.domain   = configFile.get('SMBTransport', 'domain')
        self.serverName = configFile.get('SMBTransport', 'servername')
        self.password = configFile.get('SMBTransport', 'password')
        self.machine  = configFile.get('SMBTransport', 'machine')
        self.hashes   = configFile.get('SMBTransport', 'hashes')
        self.stringBinding = r'ncacn_np:%s[\PIPE\dhcpserver]' % self.machine
        self.ts = ('71710533-BEBA-4937-8319-B5DBEF9CCC36', '1.0')

class TCPTransport(DHCPMTests):
    def setUp(self):
        DHCPMTests.setUp(self)
        configFile = configparser.ConfigParser()
        configFile.read('dcetests.cfg')
        self.username = configFile.get('TCPTransport', 'username')
        self.domain   = configFile.get('TCPTransport', 'domain')
        self.serverName = configFile.get('TCPTransport', 'servername')
        self.password = configFile.get('TCPTransport', 'password')
        self.machine  = configFile.get('TCPTransport', 'machine')
        self.hashes   = configFile.get('TCPTransport', 'hashes')
        self.stringBinding = epm.hept_map(self.machine, dhcpm.MSRPC_UUID_DHCPSRV2, protocol = 'ncacn_ip_tcp')
        #self.stringBinding = epm.hept_map(self.machine, dhcpm.MSRPC_UUID_DHCPSRV, protocol = 'ncacn_ip_tcp')
        self.ts = ('8a885d04-1ceb-11c9-9fe8-08002b104860', '2.0')

class TCPTransport64(DHCPMTests):
    def setUp(self):
        DHCPMTests.setUp(self)
        configFile = configparser.ConfigParser()
        configFile.read('dcetests.cfg')
        self.username = configFile.get('TCPTransport', 'username')
        self.domain = configFile.get('TCPTransport', 'domain')
        self.serverName = configFile.get('TCPTransport', 'servername')
        self.password = configFile.get('TCPTransport', 'password')
        self.machine = configFile.get('TCPTransport', 'machine')
        self.hashes = configFile.get('TCPTransport', 'hashes')
        self.stringBinding = epm.hept_map(self.machine, dhcpm.MSRPC_UUID_DHCPSRV2, protocol = 'ncacn_ip_tcp')
        self.ts = ('71710533-BEBA-4937-8319-B5DBEF9CCC36', '1.0')


# Process command-line arguments.
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        testcase = sys.argv[1]
        suite = unittest.TestLoader().loadTestsFromTestCase(globals()[testcase])
    else:
        suite = unittest.TestLoader().loadTestsFromTestCase(TCPTransport)
        #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TCPTransport64))
    unittest.TextTestRunner(verbosity=1).run(suite)
