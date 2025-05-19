#!/bin/bash

# Script to set the timezone on macOS
# Usage: sudo ./set_timezone.sh "TimeZone"

# Function to display usage instructions
usage() {
    echo "Usage: sudo $0 \"TimeZone\""
    echo "Example TimeZone: America/New_York"
    echo "To list all available time zones, run:"
    echo "  sudo systemsetup -listtimezones"
    exit 1
}

# Ensure the script is run as root
if [[ $(id -u) -ne 0 ]]; then
    echo "Error: This script must be run with sudo or as root."
    usage
fi

# Check if a timezone argument is provided
if [ -z "$1" ]; then
    echo "Error: No timezone specified."
    usage
fi

TIMEZONE="$1"

# Check if the specified timezone is valid
VALID_TIMEZONE=$(systemsetup -listtimezones | grep -Fx "$TIMEZONE")

if [ -z "$VALID_TIMEZONE" ]; then
    echo "Error: Invalid timezone specified."
    echo "Use 'sudo systemsetup -listtimezones' to see valid options."
    exit 1
fi

# Set the timezone
echo "Setting timezone to '$TIMEZONE'..."
systemsetup -settimezone "$TIMEZONE" >/dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Timezone successfully set to '$TIMEZONE'."
else
    echo "Error: Failed to set timezone."
    exit 1
fi
