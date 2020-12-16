# Git Commands

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

- View working tree status
```bash
git status
```

- Upload the git to github
```bash
git push -u origin master --force
```

- Looking at the commits
```bash
git log
git log --pretty=oneline
```

- Searching for deleted file/ the commit ID when deleting an object
```bash
git log --diff-filter=D --summary
```

- Checkout at a specific commit
```bash
git checkout <commit id>
```
