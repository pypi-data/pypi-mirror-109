# import database.connection as conn

from . import connection as conn

import mysql.connector
import pkgutil

cnx, cur = False, False


def connect(user, password, host):
    global cnx, cur
    cnx, cur = conn.setCursor(user, password, host)


    


# Read and execute file
def execute(params, sqlFilename):
    """
    params = dictionary with required values

    sqlFilename = name of the .SQL
    """


    sqlFile = pkgutil.get_data(__name__, f"../sql/{sqlFilename}.sql").decode()

    # Replace key values into values
    for k, v in params.items():
        sqlFile = sqlFile.replace(k, v)

    # Split SQL Commands
    sqlCommands = sqlFile.split(";")

    # Start with no errors
    error = False

    # Iterate over each command in the SQL file
    for command in sqlCommands:
        try:
            print(cur)
            cur.execute(command)
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            error = True
    return "error" if error else "ok"
