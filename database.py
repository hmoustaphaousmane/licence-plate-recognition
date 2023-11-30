import mysql.connector

host = "localhost"
user = "Bayta"
pswd = "mot_de_passe"
MyDB, MyCursor = None, None

databaseName = "Novembre"

EnginTableName = "engin_engin"
findTableName = "engin_trouver"


def getDatabase():
    global MyDB
    if MyDB is None:
        try:
            MyDB = mysql.connector.connect(host=host, user=user, password=pswd, database=databaseName)
        except Exception as e:
            print("An error occurred...")
            print(e)
    return MyDB


# Insert les informations signalant une detection d'image d'un engin  volée
def insertImageIntoDatabase(idEngin: int):
    db = getDatabase()
    myCursor = db.cursor()
    statement = f"INSERT INTO {findTableName}(engin_id) VALUES({idEngin})"
    try:
        myCursor.execute(statement)
        db.commit()
    except Exception as e:
        print(e)
        return False
    return True


# Recuperer les informations des engin volés
def getStealEngines():
    db = getDatabase()
    myCursor = db.cursor()
    statement = f"SELECT * FROM {EnginTableName}"
    try:
        myCursor.execute(statement)
        return myCursor.fetchall()
    except Exception as e:
        print(e)
        return []


