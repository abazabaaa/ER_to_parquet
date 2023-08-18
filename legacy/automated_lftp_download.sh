#!/bin/bash
PROTOCOL="ftp"
URL="ftp-rdb-fr.chem-space.com:21"
USER="XXXXX"
PASS="XXXXXX"
REGEX="*CXSMILES.cxsmiles.bz2"
LOG="XXXXXXX"
LOCAL_DIR="XXXXX"
#REMOTE_DIR="dir/remote/server/file_directory"
#REMOTE_BACKUP_DIR="dir/remote/server/backup_directory"

cd $LOCAL_DIR
if [  ! $? -eq 0 ]; then
    echo "$(date "+%d/%m/%Y-%T") Cant cd to $LOCAL_DIR. Please make sure this local directory is valid" >> $LOG
fi

lftp  $PROTOCOL://$URL <<- DOWNLOAD
    user $USER "$PASS"
    mget $REGEX
DOWNLOAD

if [ ! $? -eq 0 ]; then
    echo "$(date "+%d/%m/%Y-%T") Cant download files. Make sure the credentials and server information are correct" >> $LOG
fi
