from .database import actions as db

def connectDatabase(user = "root", password = "", host="127.0.0.1"):
    """ Connects to database """
    return db.connect(user, password, host)
    

#If you create a database it will use it automatically
def createDatabase(params={"dbName": "defaultDb"}):
    """
    CREATES NEW DATABASE
    Required params: dbName = Database Name
    """
    return db.execute(params, sqlFilename="createDB")

def dropDatabase(params={"dbName": "defaultDb"}):
    """
    DROPS DATABASE
    Required params: dbName = Database Name
    """
    return db.execute(params, sqlFilename="dropDB")

def useDatabase(params = {"dbName" : "defaultDb"}):
    """
    USES DATABASE
    Required params: dbName = Database Name
    """
    return db.execute(params, sqlFilename="useDB")

def createTable():
    """
    CREATES TABLE
    Required state: Using Database
    Required params: name = Database name, fields = List of Field Object
    """
    return True

def selectFromTable():

    """
    SELECT COLUMNS FROM TABLE
    Required state: Using Database
    Required params: columns = list of columns, table = table name
    """
    return True
    

def ExecuteRaw(params = "rawFile"):

    """
    EXECUTES .SQL FILE
    Required params: filename
    """
    return True
