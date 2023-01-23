import pymysql
import pandas as pd
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
    
    def create_database(self):
        sql = """
            create database dc character set UTF8
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
        
    def create_table(self):
        sql = """
            create table cat(id int auto_increment primary key, image_name varchar(255), image_url varchar(255))
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
    
    def get_data(self, name):
        cursor = self.conn.cursor()
        sql = f"""
            select * from cat where image_name like '%{name}%'
        """
        cursor.execute(sql)
        data = cursor.fetchone()
        self.conn.commit()
        self.conn.close()
        return data
    
    def get_all_data(self, name):
        cursor = self.conn.cursor()
        sql = f"""
            select * from cat where image_name like '%{name}%'
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        self.conn.commit()
        self.conn.close()
        return data
    
    def upload_file(self):
        sql = """
            insert into cat(image_name, image_url) values(%s, %s)
        """
        cursor = self.conn.cursor()
        df = pd.read_csv('cat.csv', keep_default_na=False)
        for data in df.iloc():
            image_name = data['圖片文字']
            image_url = data['圖片連結']
            insert_data = (image_name, image_url)
            cursor.execute(sql, insert_data)

        self.conn.commit()
        self.conn.close()
        
        
if __name__ == '__main__':
    conn = Connection()
    # conn.create_database()
    # conn.create_table()
    conn.upload_file()