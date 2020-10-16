NBTEnum 3.3 - NetBIOS Enumeration Utility

Written by Reed Arvin <reedarvin@gmail.com>. Comments and suggestions are
always appreciated.

==========================================================================

Usage:
nbtenum [-v]
nbtenum [-h]
nbtenum [-q] [ip address | ip input file] [username] [password]
nbtenum [-a] [ip address | ip input file] [dictionary file]
nbtenum [-s] [ip address | ip input file] [dictionary file]

-v - (version) Displays version information.

-h - (help) Displays this screen.

-q - (query) Enumerates NetBIOS information on the specified host or
     range of IP addresses. If a username and password is not specified
     the utility is run under the context of the null user. If a username
     and password is specified the utility is run under the context of
     the given username.

-a - (attack) Enumerates NetBIOS information on the specified host or
     range of IP addresses and also performs password checking. If a
     dictionary file is not specified the utility will check each user
     account for blank passwords and passwords the same as the username
     in lower case. If a dictionary file is specified the utility will
     check each user account for blank passwords and passwords the same as
     the username in lower case and all passwords specified in the
     dictionary file.

-s - (smart attack) Enumerates NetBIOS information on the specified host
     or range of IP addresses and performs password checking only if the
     account lockout threshold on the current host is set to 0. If a
     dictionary file is not specified the utility will check each user
     account for blank passwords and passwords the same as the username
     in lower case. If a dictionary file is specified the utility will
     check each user account for blank passwords and passwords the same as
     the username in lower case and all passwords specified in the
     dictionary file.


WARNING! Using the -a (attack) switch may lockout user accounts if the
account lockout threshold is greater than 0 on the target host.

==========================================================================

Examples:
nbtenum -q 192.168.1.1
Enumerates NetBIOS information on host 192.168.1.1 as the null user.

nbtenum -q 192.168.1.1 johndoe ""
Enumerates NetBIOS information on host 192.168.1.1 as user "johndoe" with
a blank password.

nbtenum -a iprange.txt
Enumerates NetBIOS information on all hosts specified in the iprange.txt
input file as the null user and checks each user account for blank
passwords and passwords the same as the username in lower case.

nbtenum -s iprange.txt dict.txt
Enumerates NetBIOS information on all hosts specified in the iprange.txt
input file as the null user and checks each user account for blank
passwords and passwords the same as the username in lower case and all
passwords specified in dict.txt if the account lockout threshold is 0.
