-- Shell failures are recorded by the wrapper; applet errors must never wait on a dialog.
try
    do shell script "/bin/bash /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/tools/backup_gdrive.sh"
end try
