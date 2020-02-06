import pymysql
import hashlib
import os
import codecs

# connect to database
connection = pymysql.connect(host='mrbartucz.com',
                             user='xg6856vd',
                             password='DB2020class',
                             db='xg6856vd_SaltHash',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:

        # Get user input
        user_input = input("Create a password: ")

        # add salt to password and encrypt
        salt = codecs.encode(os.urandom(20), 'hex').decode()
        password = (user_input + salt).encode()
        m = hashlib.sha512()
        m.update(password)
        newHash = m.hexdigest()

        # store password hash and salt in database
        sql = "INSERT INTO Authentication (hash, salt) VALUES (%s, %s)"
        cursor.execute(sql, (newHash, salt))
        connection.commit()

        # prompt user to confirm password
        user_input = input("Confirm password: ")

        # Select last record from authentication table
        sql = "SELECT * FROM Authentication ORDER BY ID DESC LIMIT 1"
        # execute the SQL command
        cursor.execute(sql)

        # get the results
        for result in cursor:
            savedHash = result.get("hash")
            savedSalt = result.get("salt")

    #add salt to user input and run hashing algorithm
    password = (user_input + savedSalt).encode()
    m = hashlib.sha512()
    m.update(password)
    newHash = m.hexdigest()

    #compare hashes
    if newHash == savedHash:
        print("The passwords match.")
    else:
        print("The passwords did not match.")
        
finally:
    connection.close()
