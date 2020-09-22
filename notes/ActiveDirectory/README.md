# ACTIVE DIRECTORY

This is an notes collected from everywhere.... literally everywhere..... blogs, posts, paid/free/pirated courses, books etc...
For an easy understanding I have splitted the points and spoke like thinking for understanding, if you feel its not necesarry just look at the defenition on top below the question

# TableOfContents:
- [ActiveDirectory](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/ActiveDirectory/README.md#

### What is an Active Directory ?

```bash
Directory Services that manage windows network
Strores information about objects on the network and is easily available for users and admins
The Stored objects may be user-accounts(names, passwords, phone numbers etcc.,), these stored info are available for the authorized users on the same network
The ActiveDirectory objects include shared resources such as `servers, printers, volumes, network user and computer accounts etc..`
Security in ActiveDirectory is through LogIn authentication and AccessControl to objects in the directory
In an ActiveDirectory Network, administrators can manage directory data and organisation throughout the network, the authorized users can access these info anywhere in the network
```

- Directory Services that manage windows network

```bash
Believe me I dont get this for the first time too...,
```

- Strores information about objects on the network and is easily available for users and admins

```bash
Ok now ActiveDirectory stores something called objects and that objects can be used by admins and users....hmmm ok some what understandablee
```

- The Stored objects may be user-accounts(names, passwords, phone numbers etcc.,), these stored info are available for the authorized users on the same network

```bash
So the admin stores some objects which is the user account information stuffs and that can be viewed by the authorized users on the same network....Fair Explanation
```

- The ActiveDirectory objects include shared resources such as `servers, printers, volumes, network user and computer accounts etc..`

```bash
So the ActiveDirectory has the some shared resources available, the objects is the structred data store as the basis for logical hierarchical organization of the directory info
```

- Security in ActiveDirectory is through LogIn authentication and AccessControl to objects in the directory

```bash
So in the ActiveDirectory the security for the files/stuffs are provided by the admin via access contron and via logging in/on
```

- In an ActiveDirectory Network, administrators can manage directory data and organisation throughout the network, the authorized users can access these info anywhere in the network

```bash
When the directory data(files, application, ettc..,) is altered by the admin, the authorized users can access anywhere in the network. No need to upload a specific to every computer in the network/ an organization when AD is implemented
```




> Crash [here](https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview) for official AD Stuffs by **msdn** !
