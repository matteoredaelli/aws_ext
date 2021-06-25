# AWS EXT

The aws_ext python package contains some useful functions (built on top of boto3)
for managing some aws services. At the moment only some utilities for the Aws Glue Data catalog

## Installation

```bash
pip install aws_ext
```

## Usage

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
