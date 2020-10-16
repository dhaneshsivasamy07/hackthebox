Enum+ add Bruce Force crack from enum, -- Bingle@email.com.cn

usage:  J:\enum\enum.exe  [switches]  [hostname|ip]
  -U:  get userlist
  -M:  get machine list
  -N:  get namelist dump (different from -U|-M)
  -S:  get sharelist
  -P:  get password policy information
  -G:  get group and member list
  -L:  get LSA policy information
  -d:  be detailed, applies to -U and -S
  -D:  dictionary crack, needs -u and -f
  -b:  bruce force crack, needs -u for specify user to crack
  -c:  don't cancel sessions
  -u:  specify username to use (default "")
  -p:  specify password to use (default "")
  -f:  specify dictfile to use (wants -D)

 Example:
         To get share of 10.1.1.1 use:J:\enum\enum.exe -S 10.1.1.1
         To use user admin whith password abc to connet, get user of 10.1.1.1 use:
                J:\enum\enum.exe -U -u admin -p abc 10.1.1.1
	 To bruce force crack user 'admin' password use:
                J:\enum\enum.exe -b -u admin 10.1.1.1
	

When bruce force crack password, you can specify the chars to use, you can just write chars in file 'crack.txt'. If you just want to crack all digital numbers, add all digit(0 - 9) into file 'crack.txt'(see example file 'charset-digit.txt'). If not have 'crack.txt' file in current path, enum+ will use all printable chars( !"#$%&'()*+,-./01ABCabc{|}~), all this chars list in file 'charset-all.txt'.

You may wonder 'what use of this function?', ok, that no use, just for...... Hehe, I dont know.

This function is in enum originally, just not implemented. hehe, wish the author not to blame me.


			-- Bingle@email.com.cn