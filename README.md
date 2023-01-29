# cool-python
Cool and interesting Python stuff

Resources:
https://blog.pythonlibrary.org/ 


Clone: git@github.com:openskynetwork/opensky-api.git
Run: pip install -e ~/work/git/opensky-api/python/

[//]: # (dumps to json while preventing UnicodeErrors)
json.dumps(file, default=str)

[//]: # (sort case unsensitive)
sorted_list = sorted(unsorted_list, key=str.casefold)

[//]: # (get all keys from list of dictionaries)
all_keys = set().union(*(d.keys() for d in mylist))

