wrapper=$1
if /bin/bash "$wrapper"; then
    exit_code=0
else
    exit_code=$?
fi
set -- "$wrapper" "$exit_code" ""
set -eu
wrapper=$1
exit_code=${2:-}
error_number=${3:-}
receipt_dir="$HOME/Library/Logs/memit-gdrive-backup"
/bin/mkdir -p "$receipt_dir"
temporary=$(/usr/bin/mktemp "$receipt_dir/.launch-receipt.XXXXXX")
trap '/bin/rm -f "$temporary"' EXIT
trap 'exit 1' HUP INT TERM
/usr/bin/perl -MJSON::PP -MTime::HiRes=gettimeofday -MPOSIX=strftime -e '
    my ($sec, $micro) = gettimeofday();
    print encode_json({schema => 1,
        utc => strftime("%Y-%m-%dT%H:%M:%S", gmtime($sec)) . sprintf(".%06dZ", $micro),
        wrapper_path => $ARGV[0],
        exit_code => length($ARGV[1]) ? int($ARGV[1]) : undef,
        error_number => length($ARGV[2]) ? int($ARGV[2]) : undef}), "\n";
' "$wrapper" "$exit_code" "$error_number" > "$temporary"
/bin/mv -f "$temporary" "$receipt_dir/launch_receipt.json"
