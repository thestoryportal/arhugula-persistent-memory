# Read-only inventory of the Intel Mac. Changes nothing.
echo "## identity"; date -u; whoami; scutil --get ComputerName; sw_vers; uname -m
echo "## hardware"; sysctl -n machdep.cpu.brand_string hw.ncpu hw.memsize
system_profiler SPHardwareDataType | grep -E 'Model (Name|Identifier)|Serial' | sed 's/Serial Number.*/Serial Number: (omitted)/'
echo "## disk"; diskutil info / | grep -E 'Device Node|File System Personality|Container Total Space|Container Free Space|Volume Used Space|Solid State|Media Name|SMART Status|Protocol|Encrypted|FileVault'
df -H / /System/Volumes/Data
diskutil apfs list | grep -E 'Container disk|Size \(Capacity Ceiling\)|Capacity In Use|Capacity Not Allocated|Volume disk|Name:|Role'
echo "## power"; pmset -g | grep -E ' sleep|disksleep|displaysleep|womp|autorestart|powernap|standby'
pmset -g batt | head -2
echo "## network"; ifconfig bridge0 2>&1 | grep -E 'inet |status'; route -n get default 2>&1 | grep -E 'interface|gateway'
echo "## software"; ls -d /usr/local/Homebrew /opt/homebrew 2>&1; command -v brew git python3 java rsync 2>&1; rsync --version 2>&1 | head -1; xcode-select -p 2>&1
echo "## time machine"; tmutil destinationinfo 2>&1 | head -5
