'''
No need to use multi thread to connect to 10 databases, that will cause a lot of problems and bad for efficiency.

one connection then use sql query to use multiple table

unless want to use multiple table in different database, then need to use multi thread to connect to multiple databases
'''

import pyodbc

def getCursor(driver, server, database):
    try:
        connection = pyodbc.connect(
            f'DRIVER={driver};'+
            f'Server={server};'+
            f'Database={database};'+
            'Trusted_Connection=yes'
        )
        cursor = connection.cursor()
        return cursor
    except Exception as e:
        print(f'Error: {e}')
        return None
    
def connectSQL(driver, server, database):
    success = 0
    try:
        cursor = getCursor(driver, server, database)
        success = 1
    except Exception as e:
        print(f'Error: {e}')
        success = 0

    if (success == 1):
        return "Connection Successful"
    else:
        return "Connection Unsuccessful"
    
def getTop5Data(Driver, Server, Database, Table):
    # driver = connection_info.get("Driver", "")
    # server = connection_info.get("Server", "")
    # database = connection_info.get("Database", "")
    # table = connection_info.get("Table", "")

    connection = pyodbc.connect(
    f'DRIVER={Driver};'+
    f'Server={Server};'+
    f'Database={Database};'+
    'Trusted_Connection=yes'
    )
    cursor = connection.cursor()
    cursor.execute(f'SELECT TOP 5 * FROM {Table}')
    data = []
    for row in cursor:
        data.append(row)
    column_names = [column.column_name for column in cursor.columns(table=Table)]
    return data, column_names

def getTableName(Driver, Server, Database):
    connection = pyodbc.connect(
    f'DRIVER={Driver};'+
    f'Server={Server};'+
    f'Database={Database};'+
    'Trusted_Connection=yes'
    )
    cursor = connection.cursor()
    cursor.execute(f'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = \'BASE TABLE\'')
    data = cursor.fetchall()
    tableNames = [item[0] for item in data]
    info = [Driver, Server, Database]
    return tableNames, info


