MBEnum by patrik@cqure.net
--------------------------

MBEnum queries the master browser for whatever information
it has registered. Windows servers/workstations store information
about what services they run in the MB, eg;

Terminal Services, SQL Server, RAS server

This can be useful to get an overall picture of a Windows
environment.

Syntax
------
mbenum [-s \\server] [-d dom ] [-f filter] -p <mode>

Presentation modes:

1 - by server
2 - by service
3 - by service vertically

eg;
mbenun -s \\192.168.1.1 -p 1


Please report bugs to bugs@cqure.net

