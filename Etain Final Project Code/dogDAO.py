import mysql.connector

class DogDAO:
    def __init__(self): 
        self.db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="dogDB"
        )

    def createTable(self):
        cursor = self.db.cursor()
        sql="CREATE TABLE dogs (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), owner VARCHAR(255), value INT)"
        cursor.execute(sql)
        self.db.commit()
        print("Table Created")

    def populateTable(self):
        dogs=[
            {"Name":"Fluffy", "Owner":"John Doe", "Value": 10000},
            {"Name":"Bob", "Owner":"Jane Doe", "Value": 20000},
            {"Name":"Rex", "Owner":"Jim Doe", "Value": 30000}
        ]

        cursor = self.db.cursor()
        cursor.executemany("insert into dogs (name, owner, value) values (%(Name)s,%(Owner)s,%(Value)s)", dogs)
        self.db.commit()
      
    def create(self, values):
        cursor = self.db.cursor()
        sql="insert into dog (name,owner,value) values (%s,%s,%s)"
        cursor.execute(sql, values)

        self.db.commit()
        return cursor.lastrowid

    def getAll(self):
        cursor = self.db.cursor()
        sql="select * from dog"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))

        return returnArray

    def findByID(self, id):
        cursor = self.db.cursor()
        sql="select * from dog where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        return self.convertToDictionary(result)

    def update(self, values):
        cursor = self.db.cursor()
        sql="update dog set name= %s,owner=%s, value=%s  where id = %s"
        cursor.execute(sql, values)
        self.db.commit()
    def delete(self, id):
        cursor = self.db.cursor()
        sql="delete from dog where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.db.commit()
        print("delete done")

    def convertToDictionary(self, result):
        colnames=['id','Name','Owner', "Value"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
dogDAO = DogDAO()