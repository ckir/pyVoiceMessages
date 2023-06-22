#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root or with sudo" 
   exit 1
fi

SCRIPT_DIR="$(dirname "$(realpath -P "$0")")"
cd $SCRIPT_DIR
set -x
cat <<EOF > /etc/systemd/system/pyVoiceMessagesServer.service
[Unit]
Description=pyVoiceMessagesServer daemon

[Service]
ExecStart=runuser -u $SUDO_USER -- $SCRIPT_DIR/dist/pyVoiceMessagesServer
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl enable pyVoiceMessagesServer
systemctl daemon-reload
