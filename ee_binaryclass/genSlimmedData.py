import json
import random

print 'loading data'
location = 'data/data_by_cookie_slim.json'
fh=open(location)
data=json.load(fh)

pickN = 50000
newData = {k: data[k] for k in random.sample(data, pickN)}


#json.dump(newData, open('data_by_cookie_slim.json','w'),indent=1)
