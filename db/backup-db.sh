#!/bin/bash

# Konfigurasi Database
USER="root"
PASSWORD="Infovesta20203"
DB_NAME="django"

# Folder Backup
BACKUP_DIR="/home/dj/ai-evaluator/db"
DATE=$(date +"%B-%d-%H%M")   # format: NamaBulan-Tanggal-JamMenit
FILE_NAME="backup-${DATE}.sql"

# Jalankan backup
mysqldump -u $USER -p$PASSWORD $DB_NAME > $BACKUP_DIR/$FILE_NAME

# Opsional: hapus backup lebih dari 30 hari biar hemat storage
find $BACKUP_DIR -type f -name "backup-*.sql" -mtime +30 -exec rm {} \;
