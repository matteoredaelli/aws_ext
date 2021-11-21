# AWS EXT

The aws_ext python package contains some useful functions (built on top of boto3)
for managing some aws services. At the moment only some utilities for the Aws Glue Data catalog

## Installation

```bash
pip install aws_ext
```

## Usage (command line)

export LOGLEVEL=INFO

AWS_PROFILE=prd aws_ext get_tables_with_many_versions [] 10

aws_ext get_tables_with_many_versions "[db1,db2]" 20

aws_ext delete_old_tables_versions [] 10 False

## Usage (python library)

```python
import boto3
import aws_ext

session = boto3.session.Session()
```

## GLUE

```python
from aws_ext import glue_databases
glue_client = session.client("glue")
```
Extracting tables with (too) many versions
```python
glue_databases.get_tables_with_many_versions(glue_client, database_name="mydb", threshold=1)
```
Deleting old tables versions
```python
glue_databases.delete_old_tables_versions(glue_client, database_name="mydb", keep=1, dryrun=True)

```
