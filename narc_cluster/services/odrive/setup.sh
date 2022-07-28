#! /bin/env bash 

# **Script must be run as sudo on Linux system only**


# Download and install the odrive agent/CLI tool
od="$HOME/.odrive-agent/bin" && curl -L "https://dl.odrive.com/odrive-py" --create-dirs -o "$od/odrive.py" && curl -L "https://dl.odrive.com/odriveagent-lnx-64" | tar -xvzf- -C "$od/" && curl -L "https://dl.odrive.com/odrivecli-lnx-64" | tar -xvzf- -C "$od/"

# add odrive command to path
echo "export PATH=${PATH}:${HOME}/.odrive-agent/bin" >> $HOME/.profile

## (Optional) Run O-Drive Sync Agent in the background with nohup
# nohup "$HOME/.odrive-agent/bin/odriveagent" > /dev/null 2>&1 &

echo "Installing odrive agent service"

# create dirs for user service
mkdir -p $HOME/.config/systemd/user

# create systemd user service to run odrive agent
echo "# systemd user service to run odrive agent
#
# Use loginctl enable-linger to create a user manager for the user at boot and kept around after logouts. This will allow auto-starting of the odrive agent for that user
# https://www.freedesktop.org/software/systemd/man/loginctl.html#enable-linger%20USER%E2%80%A6
#
# save this file as:
# ~/.config/systemd/user/odrive.service
#
# enable: $ systemctl --user enable odrive.service 
# start:  $ systemctl --user start odrive.service 
# status: $ systemctl --user status odrive.service
# 

[Unit]
Description=Run odrive-agent as a user service
Wants=network-online.target
After=network.target network-online.target

[Service]
Type=simple
ExecStart=%h/.odrive-agent/bin/odriveagent
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
# https://www.freedesktop.org/software/systemd/man/systemd.special.html#Units%20managed%20by%20the%20user%20service%20manager" \
> $HOME/config/systemd/user/odrive.service

# Enable the service
echo "Enabling service"
systemctl --user enable odrive.service
# Start the service
echo "Starting odrive service"
systemctl --user start odrive.service
# Return the status of the service
systemctl --user status odrive.service
# return status from odrive cli
odrive status

# log into odrive and create auth key for agent, prompt user for secure input
printf "Log into o-drive and generate Auth Key, then enter it here: "
trap 'stty echo' INT EXIT
stty -echo
read ODRIVE_KEY
printf "\n"


odrive authenticate ${ODRIVE_KEY}

# mount the root of odrive to local system
mkdir "$HOME/odrive-agent-mount"
odrive mount $HOME/odrive-agent-mount /

# If you haven't yet, link your cloud services through the O-Drive web interface

# to sync a file using CLI, you must pass the .cloudf file referencing the folder to sync function

# odrive sync [local path] --recursive
