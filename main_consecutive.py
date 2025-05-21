from datetime import datetime, timedelta

from collections import defaultdict

def three_consecutive_within_30_minutes(timestamps):
    # Ensure there are at least 3 timestamps
    if len(timestamps) < 3:
        return False

    new_dict = defaultdict(list)

    # Loop over every group of 3 consecutive timestamps
    for i in range(len(timestamps) - 2):
        # Calculate the time difference between the first and third timestamp
        if timestamps[i+2] - timestamps[i] <= timedelta(minutes=30):
            new_dict[i].append([timestamps[i+2],
                                timestamps[i+1],
                                timestamps[i]])
    return new_dict

# Example usage:
timestamps = [
    datetime(2025, 1, 12, 9, 0),
    datetime(2025, 1, 12, 9, 10),
    datetime(2025, 1, 13, 9, 50),
    datetime(2025, 1, 13, 10, 0),
    datetime(2025, 1, 13, 10, 5),
    datetime(2025, 1, 15, 10, 0),
    datetime(2025, 1, 15, 10, 30),
    datetime(2025, 1, 17, 10, 0),
    datetime(2025, 1, 17, 10, 5),
    datetime(2025, 1, 17, 10, 22),
    datetime(2025, 1, 17, 10, 30)
]

if three_consecutive_within_30_minutes(timestamps):
    print("There are three consecutive timestamps within 30 minutes.")
else:
    print("No three consecutive timestamps are within 30 minutes.")
