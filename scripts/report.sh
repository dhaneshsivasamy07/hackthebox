#!/bin/bash

################################################################################################
# start the markdown with a frontmatter
# ---                                                                                                                                                                
# title: "Attacktive Directory [TryHackMe]"                                                                                                                          
# author: cyberwr3nch                                                                                                                                                
# date: "2021-02-21"                                                                                                                                                 
# subject: "Active Directory Basics"                                                                                                                                 
# keywords: [ad, enum4linux, domain, domain controller, internal PT]                                                                                                 
# subtitle: "Basics of Active Directory Exploitation"                                                                                                                
# lang: "en"                                                                                                                                                         
# titlepage: true                                                                                                                                                    
# titlepage-color: "1E90FF"                                                                                                                                          
# titlepage-text-color: "000000"                                                                                                                                     
# titlepage-rule-color: "FFFFFF"                                                                                                                                     
# titlepage-rule-height: 1                                                                                                                                           
# book: true                                                                                                                                                         
# classoption: oneside                                                                                                                                               
# code-block-font-size: \scriptsize                                                                                                                                  
#---   
################################################################################################



# variables
RED='\033[0;31m'
NC='\033[0m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'

# main usage
if [ "$#" -ne 2 ]; then
    echo -e "[${YELLOW}*${NC}] Usage: $0 <input.md> <output.pdf>"
    # echo "Themes: pygments, kate, monochrome, breezeDark, espresso, zenburn, haddock, tango"
    # change line 73 to one of these themes
    exit
fi

# pandoc check
echo -e "[${YELLOW}-${NC}] Checking for availability of pandoc.."
if ! command -v pandoc &> /dev/null
then 
    echo -e "[${RED}+${NC}] Pandoc not installed \n"
    read -p "Do you want to install pandoc (Y/n) ?" -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo -e "\n[${BLUE}+${NC}] Installing Pandoc..."
        sudo apt-get install pandoc
    else
        echo -e "\n[${RED}*${NC}] pandoc not found "
        exit
    fi
else
     echo -e "[${BLUE}+${NC}]Pandoc seems to be installed"
fi


# texlive checking
echo -e "[${YELLOW}-${NC}] Checking for latex installation ..."
if ! command -v latex &> /dev/null
then 
    echo -e "[${RED}+${NC}] latex is not installed \n"
    read -p "Do you want to install texlive-full (Y/n) ? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo -e "\n[${BLUE}+${NC}] Installing texlive-full"
        sudo apt-get install texlive-full
    else
        echo -e "\n[${RED}*${NC}] Latex Not found"
        exit
    fi
else
     echo -e "[${BLUE}+${NC}] latex is installed"
fi

# esivogel check
echo -e "[${YELLOW}-${NC}] Checking for the availability of esivogel.latex..."

if [ ! -e /usr/share/pandoc/data/templates/eisvogel.latex ];then
    read -p "eisvogel.latex is not want to download and intstall it (Y/n) ? " -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        cd /tmp/; wget https://github.com/Wandmalfarbe/pandoc-latex-template/releases/download/v2.0.0/Eisvogel-2.0.0.tar.gz; tar -zxvf Eisvogel-2.0.0.tar.gz; sudo cp eisvogel.latex /usr/share/pandoc/data/templates/eisvogel.latex;
        echo -e "\n[${BLUE}+${NC}] eisvogel.latex added"
    else
        echo -e "\n[${RED}*${NC}] eisvogel.latex is not found"
        exit
    fi
else
    echo -e "[${BLUE}+${NC}] eisvogel.latex is found in /usr/share/pandoc/data/templates"    
fi

# file generate
pandoc $1 -o $2 \
--from markdown+yaml_metadata_block+raw_html \
--template eisvogel \
--table-of-contents \
--toc-depth 6 \
--number-sections \
--top-level-division=chapter \
--highlight-style breezeDark 

# output open
if [ $? -eq 0 ];then
    echo "Process finished"
    read -p "Do you want to open the PDF ? (Y/n) " -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]];then
        echo
        xdg-open $2
    else
        echo
        echo "Bye Bye"
        echo
        exit
    fi
else
    echo "Bye Bye"
fi
