### getDB module

This module is used to download comment databases, such as HMDB, KEGG. Now verion0.0.1 only support 
HMDB.


#### Installation

You can install it using pip in python.

```
#in your CMD (windows) or terminal (Linux or Mac)
pthon -m pip install getDB
```

#### Usage and Example

```
from getDB import hmdb
temp = hmdb.getMetabolite(ID = "HMDB0000001")
##check the contents of temp
temp.keys()
temp["name"]
temp["diseases"]
temp['ontology']
temp['normal_concentrations']

```

