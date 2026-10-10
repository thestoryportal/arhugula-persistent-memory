-- Embed failure recording: it must remain available when the volume is absent.
property wrapperPath : "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/tools/backup_gdrive.sh"
property launchShell : "wrapper=$1\nif /bin/bash \"$wrapper\"; then\n    exit_code=0\nelse\n    exit_code=$?\nfi\nset -- \"$wrapper\" \"$exit_code\" \"\"\n"
-- This separate literal can run without loading or executing the wrapper.
property receiptShell : "set -eu\nwrapper=$1\nexit_code=${2:-}\nerror_number=${3:-}\nreceipt_dir=\"$HOME/Library/Logs/memit-gdrive-backup\"\n/bin/mkdir -p \"$receipt_dir\"\ntemporary=$(/usr/bin/mktemp \"$receipt_dir/.launch-receipt.XXXXXX\")\ntrap '/bin/rm -f \"$temporary\"' EXIT\ntrap 'exit 1' HUP INT TERM\n/usr/bin/perl -MJSON::PP -MTime::HiRes=gettimeofday -MPOSIX=strftime -e '\n    my ($sec, $micro) = gettimeofday();\n    print encode_json({schema => 1,\n        utc => strftime(\"%Y-%m-%dT%H:%M:%S\", gmtime($sec)) . sprintf(\".%06dZ\", $micro),\n        wrapper_path => $ARGV[0],\n        exit_code => length($ARGV[1]) ? int($ARGV[1]) : undef,\n        error_number => length($ARGV[2]) ? int($ARGV[2]) : undef}), \"\\n\";\n' \"$wrapper\" \"$exit_code\" \"$error_number\" > \"$temporary\"\n/bin/mv -f \"$temporary\" \"$receipt_dir/launch_receipt.json\"\n"

try
    do shell script "/bin/sh -c " & quoted form of (launchShell & receiptShell) & " backup-launch " & quoted form of wrapperPath
on error errorMessage number errorNumber
    try
        do shell script "/bin/sh -c " & quoted form of receiptShell & " backup-receipt " & quoted form of wrapperPath & " '' " & quoted form of (errorNumber as text)
    end try
end try
