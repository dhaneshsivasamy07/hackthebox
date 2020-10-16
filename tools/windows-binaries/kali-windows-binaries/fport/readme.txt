Readme for fport v2.0

fport supports Windows NT4, Windows 2000 and Windows XP

fport reports all open TCP/IP and UDP ports and maps them to the owning application.
This is the same information you would see using the 'netstat -an' command, but it also
maps those ports to running processes with the PID, process name and path.  Fport can be
used to quickly identify unknown open ports and their associated applications.

Usage:  
C:\>fport
FPort v2.0 - TCP/IP Process to Port Mapper
Copyright 2000 by Foundstone, Inc.
http://www.foundstone.com
Pid   Process            Port  Proto Path
392   svchost        ->  135   TCP   C:\WINNT\system32\svchost.exe
8     System         ->  139   TCP
8     System         ->  445   TCP
508   MSTask         ->  1025  TCP   C:\WINNT\system32\MSTask.exe

392   svchost        ->  135   UDP   C:\WINNT\system32\svchost.exe
8     System         ->  137   UDP
8     System         ->  138   UDP
8     System         ->  445   UDP
224   lsass          ->  500   UDP   C:\WINNT\system32\lsass.exe
212   services       ->  1026  UDP   C:\WINNT\system32\services.exe

The program contains five (5) switches.  The switches may be utilized using either a '/' 
or a '-' preceding the switch.  The switches are;

Usage:
	/?	 usage help
        /p       sort by port
        /a       sort by application
        /i       sort by pid
        /ap      sort by application path

For updates visit:  www.foundstone.com
