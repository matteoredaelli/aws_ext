"""databases module

This module contains some useful functionsl like delete_old_table_versions

"""

import logging
from . import glue_tables


def get_all_tables(glue_client, database_name):
    ## responseGetTables = glue_client.get_tables(DatabaseName=database_name)
    paginator = glue_client.get_paginator("get_tables")
    page_iterator = paginator.paginate(DatabaseName=database_name)
    result = []
    for page in page_iterator:
        tablenames = list(map(lambda t: t["Name"], page["TableList"]))
        result = result + tablenames
    logging.debug(f"Found tables {result}")
    return result


def get_tables_with_many_versions(glue_client, database_name, threshold):
    result = {}
    tablenames = get_all_tables(glue_client, database_name)
    for t in tablenames:
        tot = glue_tables.count_table_versions(glue_client, database_name, t)
        if tot >= threshold:
            result[t] = tot

    ##sorted_dict = dict(sorted(result.items(), key=operator.itemgetter(1), reverse=True))
    return result  ## sorted_dict


def delete_all_tables(glue_client, database_name, dryrun=False):
    tablenames = get_all_tables(glue_client, database_name)
    logging.warning(f"Deleting tables {tablenames}")
    if dryrun:
        logging.warning(f"Dryrun: nothing will be changed")
        return 1
    return glue_client.batch_delete_table(
        DatabaseName=database_name, TablesToDelete=tablenames
    )

def delete_old_tables_versions(glue_client, database_name, keep, dryrun=False):
    if int(keep) < 1:
        logging.error(f"cannot delete all table versions: keep={keep} must be greater than 0")
        return 1
    tablenames = get_all_tables(glue_client, database_name)
    logging.warning(f"Deleting table versions fro tables {tablenames}")
    for table_name in tablenames:
        glue_tables.delete_old_table_versions(glue_client, database_name, table_name, keep, dryrun=dryrun)
    return 0
