import pymysql
import os


class Connection:
    def __init__(self):
        self.db_name = os.getenv('DB_HOST')
        self.password = os.getenv('DB_PASSWORD')
        self.conn = self.connection()
        
    def connection(self):
        conn = pymysql.connect(
            host=self.db_name,
            port=3306,
            user='root',
            password=self.password,
            database='dc'
        )
        return conn
    
    def create_table(self):
        sql = """
            create table sponge(id int auto_increment primary key, name varchar(255), url varchar(255))
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
        
    def get_data(self, name):
        cursor = self.conn.cursor()
        sql = f"""
            select * from sponge where name like '%{name}%'
        """
        cursor.execute(sql)
        data = cursor.fetchone()
        self.conn.commit()
        self.conn.close()
        return data
    
    def get_all_data(self, name):
        cursor = self.conn.cursor()
        sql = f"""
            select * from sponge where name like '%{name}%'
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        self.conn.commit()
        self.conn.close()
        return data
    
    def insert(self):
        sql = '''
            insert into sponge(name, url) values (%s, %s)
        '''
        cursor = self.conn.cursor()
        for file in os.listdir(r'sponge'):
            data = (file, '')
            cursor.execute(sql, data)      
        self.conn.commit()
        self.conn.close()
        

if __name__ == '__main__':
    conn = Connection()
    # conn.create_table()
    conn.insert()