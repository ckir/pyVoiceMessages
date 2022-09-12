#!/bin/bash
source color_print.sh
me="$(basename "$(test -L "$0" && readlink "$0" || echo "$0")")"

printWhite "Cleaning Old"
Folders=('pyVoiceMessagesServer.build' 'pyVoiceMessagesServer.dist' 'pyVoiceMessagesServer.onefile-build' 
  'pyVoiceMessagesClient.build' 'pyVoiceMessagesClient.dist' 'pyVoiceMessagesClient.onefile-build' 
  'dist  build')

for i in "${Folders[@]}"
do 
  if [ -d "$i" ]; then rm -Rf "$i"; fi
done

pyinstaller --clean --noconfirm --onefile --console pyVoiceMessagesClient.py
ExitClient=$?
pyinstaller --clean --noconfirm --onefile --console pyVoiceMessagesServer.py
ExitServer=$?

[ $ExitClient -eq 0 ] && printGreen "Client build was successful" || printRed "Client build failed"
[ $ExitServer -eq 0 ] && printGreen "Server build was successful" || printRed "Server build failed"
