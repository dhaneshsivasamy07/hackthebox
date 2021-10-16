# Git Commands

- [Ctf / Inspection usage](#ctf)
- [Normal / Dev usage](#dev)

## CTF Usage <a name="ctf"> </a>
- Inspect a .git rep
```bash
git status
```

- Identify the commit ids and the messages
```bash
git log
```

- Get the commit ids and the messages ( without author name and date )
```bash
git log --oneline
```

- Get the log information prettier ( added and deleted infomration )
```bash
git log -p
```

- Get the log information prettier ( without author name and date information )
```bash
git log --pretty=oneline
```

- Inspect a specific commit ID 
```bash
git log -p <commi ID>
```

- Checkout at a speicific commit ID ( retrive files at that specific commit )
```bash
git checkout <commitID>
# when error pops out use --force 
git checkout --force <commitID>
```

- Restore the git to the specific version
```bash
git reset --hard <commitID>
```
 
## Normal Usage <a name="dev"></a>
- Clone a repository
```bash
git clone <repo link>
```

- Initialize the repository
```bash
git init
```

- Update a repository
```bash
git pull
```

- Add the copied files to the git
```bash
git add .
```

- Commit a message
```bash
git commit -m "message"
```

- Upload the git to github
```bash
git push -u origin master --force
```

- Searching for deleted file/ the commit ID when deleting an object
```bash
git log --diff-filter=D --summary
```

- Know the origin / url of a repository
```bash
git config --get remote.origin.url
```
