# Quick Json

This Package will help you deal with json files more quickly and efficiently.

## How to Install it?

On Windows:
```
pip install quickjson
```

On Linux:
```
sudo pip3 install quickjson
```

## How to Use it?

### Initializing The Package

```
from quickjson.quickjson import QuickJson

jsonhelper = QuickJson('filename.json') # Provide the Name of the Json File while Initializing
```
This will initialize QuickJson Class to jsonhelper variable and now you can use it's all functions using the variable.

### Reading Data From Json Files

```
print(jsonhelper.read_json_file())
```
This will print the contents of json file in the console.

### Writing Data to Json FIles

```
data = {"elite": "john"} # Sample Dictionary

jsohelper.write_json_file(data) # Parsing the dictionary
```
This will write the dictionary parsed in the json file.

### Inserting Element to a List present inside json file

If you want to insert an item to a list present inside json file then use this code
```
jsonhelper.write_list_json_file('listname', 'element')
```
This will insert the element into the specific list

For More Information, Visit [Documentation](https://quickjson.readthedocs.io/).