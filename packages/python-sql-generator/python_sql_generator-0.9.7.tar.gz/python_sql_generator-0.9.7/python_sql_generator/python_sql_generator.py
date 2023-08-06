import re


def insert(table, fields):
    """ Function for generating an SQL insert from a dict structure
    Args:
        table (str): The name of the table to be inserted into
        fields (dict): A dict that contains column names and the values to be inserted
    Returns:
        dictionary: returns a complete SQL string that can then be executed with parameter formatting.

        For example you can return the string and run a db execute.
        qry = PythonSQLGenerator.insert('my_table_name', my_dict)
        cursor.execute(qry['query'], qry['params'])
    """
    k = ""
    v = ()
    i = 0
    params = ""
    for key, val in fields.iteritems():
        i += 1
        k += "`" + key + "`"
        v = v + (val,)
        params += '%s'
        if i < len(fields):
            k += ", "
            params += ", "
    qry = {
        'query': "Insert Into " + table + " (%s) Values (%s);" % (k, params),
        'params': v
    }
    return qry


def update(table, fields, where={}):
    """ Function for generating an SQL update from a dict structure
    Args:
        table (str): The name of the table to be updated
        fields (dict): A dict that contains column names and the values to be inserted
        where (dict): A dict that contains the where key and values
    Returns:
        string: returns a complete SQL string that can then be executed.

        For example you can return the string and run a db execute.
        qry = PythonSQLGenerator.update('my_table_name', my_dict, my_where_dict)
        cursor.execute(qry)
    """
    qry = ""
    i = 0
    v = ()
    params = ""
    #  loop through fields and set key and value string
    for key, val in fields.iteritems():
        i += 1
        qry += "`" + key + "`=%s"
        v = v + (val,)
        if i < len(fields):
            qry += ", "
    # if a where clause has been passed, loop through the where dict and set the key value string
    if len(where) > 0:
        i = 0
        qry += " where "
        for key, val in where.iteritems():
            i += 1
            qry += key + "=%s"
            v = v + (val,)
            if i < len(where):
                qry += " and "
    qry = {
        'query': "update " + table + " set %s;" % (qry),
        'params': v
    }
    return qry


def delete(table, where={}):
    """ Function for generating an SQL delete from a dict structure
    Args:
        table (str): The name of the table to be deleted from
        where (dict): A dict that contains the where key and values
    Returns:
        string: returns a complete SQL string that can then be executed.

        For example you can return the string and run a db execute.
        qry = PythonSQLGenerator.delete('my_table_name', my_where_dict)
        cursor.execute(qry)
    """
    qry = ""
    # if a where clause has been passed, loop through the where dict and set the key value string
    i = 0
    for key, val in where.iteritems():
        i += 1
        qry += key + "='" + str(val) + "'"
        if i < len(where):
            qry += " and "
    qry = "delete from " + table + " where %s;" % (qry)
    return qry
