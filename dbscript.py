import sqlite3
def createTables(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS User("
              "username TEXT PRIMARY KEY,"
              "password TEXT,"
              "fullname TEXT,"
              "email TEXT,"
              "telno TEXT)")

    c.execute("CREATE TABLE IF NOT EXISTS Category("
              "cid INTEGER PRIMARY KEY,"
              "cname TEXT)")

    c.execute("CREATE TABLE IF NOT EXISTS Advertisement("
              "aid INTEGER PRIMARY KEY AUTOINCREMENT,"
              "title TEXT,"
              "description TEXT,"
              "isactive INTEGER,"
              "username TEXT,"
              "cid INTEGER,"
              "FOREIGN KEY (username) REFERENCES User(username),"
              "FOREIGN KEY (cid) REFERENCES Category(cid))")

    conn.commit()
    conn.close()

def insertRecords(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.executemany("INSERT INTO Category VALUES (?,?)", [(1, "Clothes"), (2, "Technology"), (3, "Cars"), (4, "Food"), (5, "Drink")])

    user_list = [
        ('johndoe', 'john123', 'John Doe', 'john@example.com', '555-1111'),
        ('doejane', 'jane123', 'Jane Doe', 'jane@example.com', '555-2222'),
        ('alice9876', 'alice123', 'Alice Smith', 'alice@example.com', '555-3333'),
        ('bobj55', 'bob123', 'Bob Johnson', 'bob@example.com', '555-4444'),
        ('martineze', 'eva123', 'Eva Martinez', 'eva@example.com', '555-5555')
    ]
    c.executemany("INSERT INTO User VALUES (?,?,?,?,?)", user_list)

    advertisement_list = [
        (1, 'Ad Title 1', 'Description for Ad 1', 1, 'johndoe', 1),
        (2, 'Ad Title 2', 'Description for Ad 2', 1, 'doejane', 2),
        (3, 'Ad Title 3', 'Description for Ad 3', 1, 'alice9876', 3),
        (4, 'Ad Title 4', 'Description for Ad 4', 0, 'bobj55', 4),
        (5, 'Ad Title 5', 'Description for Ad 5', 1, 'martineze', 5)
    ]
    c.executemany("INSERT INTO Advertisement VALUES (?,?,?,?,?,?)", advertisement_list)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    dbname = input("Enter database name: ")
    createTables(dbname)
    insertRecords(dbname)