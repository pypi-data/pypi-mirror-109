# Database connection

import mysql.connector


def setCursor(user, password, host):

    cnx = mysql.connector.connect(
        user=user,
        password=password,
        host=host
        # user="db-admin", password="db-password", host="127.0.0.1"
    )

    cursor = cnx.cursor()

    return cnx, cursor
