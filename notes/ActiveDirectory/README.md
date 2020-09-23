# ACTIVE DIRECTORY

This is an notes collected from everywhere.... literally everywhere..... blogs, posts, paid/free/pirated courses, books etc...
For an easy understanding I have splitted the points and spoke like thinking for understanding, if you feel its not necesarry just look at the defenition on top below the question

<p align="center">
  <img src='https://github.com/cyberwr3nch/hackthebox/blob/master/scripts/files/Directory.png' >
</p>


# TableOfContents:
- [ActiveDirectory Basics](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/ActiveDirectory/README.md#what-is-an-active-directory-)
- [ActiveDirectory Components](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/ActiveDirectory/README.md#ActiveDirectory-Components)

### What is an Active Directory ?

```bash
Directory Services that manage windows network
Strores information about objects on the network and is easily available for users and admins
The Stored objects may be user-accounts(names, passwords, phone numbers etcc.,), these stored info are available for the authorized users on the same network
The ActiveDirectory objects include shared resources such as `servers, printers, volumes, network user and computer accounts etc..`
Security in ActiveDirectory is through LogIn authentication and AccessControl to objects in the directory
In an ActiveDirectory Network, administrators can manage directory data and organisation throughout the network, the authorized users can access these info anywhere in the network
Every Objects in the ActiveDirectory has different attributes and properties
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

### ActiveDirectory Components

- ActiveDirectory is made up of **four** components
    - Schema
    - Query and Indexing
    - Global catalogue
    - Replication Service

- Schema → Defines objects and their attributes

```bash
It defines the objects like user accounts, shared resources such as servers, printers etc.., and holds its attributes like user name, previledge permissions, password policies etc..,
```

- Query and Indexing → Provides Searching and publications of objects and their properties

```bash
As ActiveDirecrtory could span across multiple locations, searching and accessing certain objects and its attributes will be useful
```

- Global Catalogue → Contains information about every objects in the directory

```bash
Its more like a TableOfContents, contains information about every objects in the ActiveDirectory and like inforamtions about all domain controllers in forest which in has the infos about the objects and its attributes
```

- Relication Service → Distributes the stored information accross the domain controllers

```bash
It replicates, the infos accross the network... simple,, what ever the information is available in the root of the forest(administrator's computer) to the rest of the computers in the same network
```


> Crash [here](https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview) for official AD Stuffs by **msdn** !

### Support My contents
<a href="https://www.buymeacoffee.com/cyberwr3nch" target="_blank"><img align="left" alt="Dhanesh Sivasamy's Twitter" width="120px" src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png"></a>
