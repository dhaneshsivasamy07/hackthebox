#!/bin/bash

echo Enter the directory name:
read dir_ 
cd $dir_
echo enter the root hash
read hash_
dn=$(basename *.pdf)
echo The found pdf is $dn
dnd=$(echo $dn | cut -d '.' -f 1)
pdftk $dn output $dnd-Protected.pdf userpw $hash_


