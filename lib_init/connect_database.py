import pyodbc


def connect_db(db_driver, db_server, db_database):
    # подключение к базе данных и выдача курсора
    cnxn = pyodbc.connect("Driver={" + db_driver + "};"
                          "Server=" + db_server + ";"
                          "Database=" + db_database + ";"
                          "Trusted_Connection=yes;")
    return cnxn.cursor()