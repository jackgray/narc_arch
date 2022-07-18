# this script will rsync then remove files from google drive until there is 5 gb remaining, so that it can only be 2/3 full

# add conditional for files created before date x
rm_files=$(find /mnt/google-drive -type f -date +${date_index})
rsync /mnt/google-drive /backup/google-drive

rm $rm_files
