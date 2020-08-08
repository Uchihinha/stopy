import mysql.connector

def setupCon():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="stop"
    )

    return con

def getAllWords():
    cursor = con.cursor(dictionary=True)
    cursor.execute("select * from word")
    return cursor.fetchall()

def insertWords(data):
    cursor = con.cursor(dictionary=True)

    currentLetter = data[0]['word'].split()[0]

    insertQuery = "insert into word (word, category) values "
    comma = ""
    for word in data:
        obj = {
            'category': word['category'],
            'letter': currentLetter
        }

        if (getWordByLetter(obj) == ''):
            insertQuery += f"{comma}('{word['word']}', '{word['category']}')"
            comma = ","
    
    cursor.execute(insertQuery)
    con.commit()
    cursor.close()
    return True

def getWordByLetter(obj):
    try:
        cursor = con.cursor(dictionary=True, buffered=True)

        cursor.execute(f"select * from word where category = '{obj['category']}' and word like '{obj['letter']}%'")

        word = cursor.fetchone()
        if word:
            word = word['word']
        else:
            word = ''
    except mysql.connector.errors.InterfaceError as ie:
        print(ie.msg)
        print('DEU MERDA AQUI')
        word = ''
    return word
    
global con
con = setupCon()
