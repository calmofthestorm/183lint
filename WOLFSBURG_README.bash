#!/bin/bash 
set -e # Quit after first error.

# Run or read this script to set up lint183 from source on github.

# To setup on Wolfsburg from git checkout:
##########################################

# Get the source
git clone git://github.com/calmofthestorm/183lint.git $1

# IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!
echo
echo
echo
echo In ${1}/lint183/settings.py change the secret key from the debug value
echo in git to something else YOU MUST DO THIS MANUALLY
echo
echo
echo

virtualenv $1             # Set up a virtualenv wherever you plan to serve from.
cd $1                     # Chdir to the directory
bin/easy_install django   # Install django to the virtualenv


# To run the service:
##################################3

echo
echo
echo
echo To run the service, cd to $1 and:
echo bin/python manage.py runserver 141.212.113.64:15180 # Change to desired IP/port

# To always run the service while server is up
##################################3

# Add the line below to crontab, updating directory as needed.
echo
echo
echo
echo To automatically run the service, add the below line to crontab (edit port, ip as necessary)
echo  Fix the path if $1 is not an absolute path
echo "*/1 * * * * cd /z/eecs183/${1}; /z/eecs183/${1}/bin/python manage.py runserver 141.212.113.64:15180 > /dev/null >> /dev/null # Port binding as lock."
