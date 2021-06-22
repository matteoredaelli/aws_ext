"""tables module

This module contains some useful functionsl like delete_old_table_versions

"""
import logging
from botocore.exceptions import ClientError


def delete_table_version(glue_client, database_name, table_name, version_ids, dryrun=False):
    """delete_table_version"""
    try:
        logging.warning(f"Deleting version {version_ids} for table {database_name}.{table_name}")
        if dryrun:
            logging.warning(f"Dryrun: nothing will be changed")
            response = 1
        else:
            version_ids_str = list(map(lambda t: str(t), version_ids))
            response = glue_client.batch_delete_table_version(
                DatabaseName=database_name, TableName=table_name, VersionIds=version_ids_str
            )
        return response
    except ClientError as e:
        raise Exception(
            "boto3 client error in delete_table_version: " + e.__str__()
        )
    except Exception as e:
        raise Exception(
            "Unexpected error in delete_table_version: " + e.__str__()
        )


def get_table_version_ids(glue_client, database_name, table_name):

    resp = glue_client.get_table_versions(
        DatabaseName=database_name, TableName=table_name
    )
    alist = list(map(lambda t: int(t["VersionId"]), resp["TableVersions"]))
    alist.sort(reverse=True)
    return alist


def delete_old_table_versions(glue_client, database_name, table_name, keep, dryrun=False):
    if int(keep) < 1:
        logging.error(f"cannot delete all table versions: keep={keep} must be greater than 0")
        return 1
    versions = get_table_version_ids(glue_client, database_name, table_name)
    logging.warning(f"Deleting old versions for table {table_name} keeping {keep} versions")
    version_ids = versions[keep:]
    return delete_table_version(glue_client, database_name, table_name, version_ids, dryrun=dryrun)


def count_table_versions(glue_client, database_name, table_name):
    resp = get_table_version_ids(glue_client, database_name, table_name)
    return len(resp)
