"""tables module

This module contains some useful functionsl like delete_old_table_versions

"""
import logging
from botocore.exceptions import ClientError


def delete_table_version(glue_client, database_name, table_name, version_id):
    """delete_table_version"""
    try:
        logging.warning(f"Deleting version {version_id} for table {tablename}")
        response = glue_client.batch_delete_table_version(
            DatabaseName=database_name, Name=table_name, VersionId=version_id
        )

        return response
    except ClientError as e:
        raise Exception(
            "boto3 client error in delete_table_version_from_database: " + e.__str__()
        )
    except Exception as e:
        raise Exception(
            "Unexpected error in delete_table_version_from_database: " + e.__str__()
        )


def get_table_version_ids(glue_client, database_name, table_name):
    resp = glue_client.get_table_versions(
        DatabaseName=database_name, TableName=table_name
    )
    alist = list(map(lambda t: int(t["VersionId"]), resp["TableVersions"]))
    alist.sort(reverse=True)
    return alist


def delete_old_table_versions(glue_client, database_name, table_name, keep):
    versions = get_table_version_ids(glue_client, database_name, table_name)
    logging.warning(f"Deleting old versions for table {tablename}using keep={keep}")
    for version_id in versions[keep:]:
        delete_table_version(glue_client, database_name, table_name, version_id)


def count_table_versions(glue_client, database_name, table_name):
    resp = get_table_version_ids(glue_client, database_name, table_name)
    return len(resp)
