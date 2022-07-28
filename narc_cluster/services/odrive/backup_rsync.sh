# backup / update
rsync --update -va --progress --info=progress2 $HOME/narc_odrive/Google\ Drive $HOME/narc_odrive/Backup/Google_drive

# clean up empty directories after autoremoving synced files
# find source -depth -type d -empty -delete