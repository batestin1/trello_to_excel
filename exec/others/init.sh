#!/bin/bash

###################################################################################################
#                                                                                                 #
# SCRIPT FILE: init.sh                                                                            #
# CREATION DATE: 02/02/2023                                                                       #
# HOUR: 10:10                                                                                     #
# DISTRIBUTION USED: Ubuntu                                                                       #
# OPERATIONAL SYSTEM: LINUX                                                                       #
#                                                                             DEVELOPED BY: BATES #
###################################################################################################
#                                                                                                 #
# SUMMARY: Starting the projet on Shell                                                           #
#                                                                                                 #
###################################################################################################


os=`uname -s`

if [ "$os" = "Linux" ]; then
  sudo apt-get update
  sudo apt-get install -y python3 python3-pip
  pip3 install -r pip/requirements.txt
  python3 trello/scripts/main.py
elif [ "$os" = "Darwin" ]; then
  echo "Installing Brew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
  brew install python
  pip install -r pips/requeriments.txt
  python scripts/main.py
else
  cmd /c ./exec/win/init.bat
  exit 1
fi
