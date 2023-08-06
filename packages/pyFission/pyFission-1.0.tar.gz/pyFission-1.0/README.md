# pyFission
<a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_3.6-green.svg"></a>

#### Description
pyFission syncs tables/schemas across databases as defined in the **configs/fission.py** file. 
If *src_table* and *src_schema* args are not provided, it will sync all tables and schemas specified in the 
**fission.py** config file by summoning multiple bash commands in parallel. 

The **pyfission** module has 2 methods of syncing tables -  
1. full: truncate + full sync of table, as name suggests
2. incremental: syncs changes based on primary key and replication key provided in *fission.py* config file

pyFission automatically detects and builds the schema definition for tables, including nested and repeated fields 
for JSON-like schemas e.g:- BigQuery. Also, pyFission patches tables automatically if any new fields are added. 


### Getting started
#### Usage
* Modify **configs/custom_config.py** and **configs/fission.py** with DB creds and sync config respectively
* Add service account private key files/secrets to **secrets_storage** dir if needed

```bash
$ python -m pyfission --src [] --dest [] sync --help
usage: __main__.py pyfission [-h] [--src_table SRC_TABLE]
                          [--src_schema SRC_SCHEMA] [--src_db SRC_DB]
                          [--dest_table DEST_TABLE]
                          [--dest_schema DEST_SCHEMA] [--dest_db DEST_DB]
                          [--method {full,incremental}]
                          [--out_format {csv,json}]

optional arguments:
  -h, --help            show this help message and exit
  --src_table SRC_TABLE
                        Overrides table definition from pyfission configs
  --src_schema SRC_SCHEMA
                        Overrides schema definition from pyfission configs
  --src_db SRC_DB       Overrides database definition from pyfission configs
  --dest_table DEST_TABLE
                        Overrides table definition from pyfission configs
  --dest_schema DEST_SCHEMA
                        Overrides schema definition from pyfission configs
  --dest_db DEST_DB     Overrides database definition from pyfission configs
  --method {full,incremental}
                        Method of Replication
  --out_format {csv,json}
                        Format of output files
```

* Recommended *out_format*:
    * *json* for BigQuery
    * *csv* for others

* To sync a particular table - specify the src_schema and src_table args
    * *dest_table* will have same name as *src_table* unless explicitly specified
    * *dest_schema* will be set from **fission.py** config file's *fission_dest* dict
    * *src_db* and *dest_db* will derived from *src* and *dest*
```bash
python -m pyfission --src [] --dest [] sync --src_table [] --src_schema [] --out_format []
```


* To sync an entire DB - only provide *src* and *dest* args
```bash
python -m pyfission --src [] --dest [] sync --out_format []
```


#### Installation
```bash
pip install pyfission
```

#### Contribution/Local installation
1. Clone the repo
```bash
$ git clone <final repo link to be added here>
```

2. change the working directory to fission
```bash
$ cd pyfission
```

3. install python3 and the requirements if they don't exist
```bash
$ pip install -r requirements.txt
```
