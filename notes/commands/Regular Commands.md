### Post \ Pre Exploitation

- ls
- Grep 
- AWK
- Compression and decompression of files
- Find
- xclip
- Misc


#### ls
```bash
# list files
ls

# list hidden files
ls -la

# list files with human readable size
la -sh
```

#### Grep
```bash
# search for the files that contains the phrase password in it
grep -ir password

# exclude multiple strings
grep -Ev 'exclude1 | exclude 2' filename.txt

# obtain only lines starting with small letters
grep -v '[A-Z]' users.txt
```


#### AWK
```bash
# simple grab based on spaces, damnedsec cyberwr3nch hackthebox
awk '{print $1}' # output damnedsec

# multiple field seperator, obtain things only with in the delimeter
# contents of the file-> user: cyberwr3nch: damnedsec;123
awk -F: '{print $3}' users.txt # output damnedsec;123

# contents of users.txt -> user:[BLACKFIELD764430] rid:[0x451], 
awk -F"[][]" '{print $2}' users.txt # output: BLACKFIELD764430

# obtain contents from a specific line
# where x is the line number	
awk 'NR==x {print $1}'

```

#### SED
```bash
# search and replace strings
cat username.txt | sed s/{stringToBeChanged}/{replacementString}/g

# replace the last ',' with a null character
cat usernames.txt | sed s/,$//
```

#### tr
```bash
# translate new lines '\n' into ','; used in HTB nmap
cat usernames.txt | tr '\n' ','
```


#### Find
```bash
# find with file names
find . -name user.txt 

# find and execute
find . -name '*.txt' -exec cat "{}" \;

# {} is used as the place holder and tells the follwing to as an argument
# find directories with the specified name and execute the command
find . -type d -name uploads -exec rm -rf "{}" ';'
# find and copy files 
find -name 'file.ext' -exec cp "{}" <copy_path>  \;
```

#### Compressing and Decompressing
```bash
# zip a folder with its contents
zip -r -9 html.zip /var/www/html

# unzip a zip file
unzip html.zip

# tar a file
tar cvf html.tar html/

# extract a .tar file
tar -xvf html.tar 

# tar.gz a folder
tar cvfz html.tar.gz html/

# unzip a *.tar.gz file
tar -xzvf html.tar.gz

# unzip rar file
unrar x html.rar
```

#### Xclip
```bash
# installation
sudo apt-get install xclip

# copying contents from a file and pasting it with 'mouse scroll button'
cat user.txt | xclip

# copying file and using cttl + v for pasting
cat user.txt | xclip -sel clip
cat user.txt | xclip -selection clipboard
```

#### Misc
```bash
# monitor, repeat the same command for a period of time
# ls -la every 1 sec on a dir
watch -n 1 'ls -la'
```
