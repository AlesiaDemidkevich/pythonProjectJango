# pip install psycopg2
import sqlite3

import pandas
import psycopg2
from abc import ABC, abstractmethod
from psycopg2 import Error
from sqlite3 import Error


class DataClient(ABC):
    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def create_mebel_table(self, conn):
        pass

    @abstractmethod
    def get_items(self, conn, price_from=0, price_to=100000):
        pass

    @abstractmethod
    def insert(self, conn, link, price, description):
        pass

    def print_items(self, items):
        print(f'\tLink\tPrice\tDescription\n{'=' * 200}')
        if items:
            for item in items:
                try:
                    print(f'\t{item[0]}\t{item[1]}\t{item[2]}')
                except:
                    pass

            print(f'\tВСЕГО {len(items)} ЗАПИСЕЙ')


class PostgresClient(DataClient):
    USER = "postgres"
    PASSWORD = "postgres"
    HOST = "localhost"
    PORT = "5432"

    def get_connection(self):
        try:
            connection = psycopg2.connect(
                user=self.USER,
                password=self.PASSWORD,
                host=self.HOST,
                port=self.PORT
            )
            return connection
        except psycopg2.Error:
            print(psycopg2.Error)

    def create_mebel_table(self, conn):
        cursor_object = conn.cursor()
        cursor_object.execute(
            """
                CREATE TABLE IF NOT EXISTS mebel
                (
                    id serial PRIMARY KEY, 
                    link text UNIQUE, 
                    price integer, 
                    description text
                )
            """
        )
        conn.commit()

    def get_items(self, conn, price_from=0, price_to=100000):
        cursor = conn.cursor()
        cursor.execute(
            f'SELECT link, price, description FROM app_1_mebel WHERE price >= {price_from} and price <= {price_to}')
        return cursor.fetchall()

    def insert(self, conn, link, price, description):
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"INSERT INTO app_1_mebel (link, price, description) VALUES ('{link.split('?')[0]}', '{price}', '{description}')")
        except psycopg2.Error:
            pass
        finally:
            conn.commit()


class Sqlite3Client(DataClient):
    DB_NAME = "Kufar.db"

    def get_connection(self):
        try:
            conn = sqlite3.connect(self.DB_NAME)
            return conn
        except sqlite3.Error:
            print(sqlite3.Error)

    def create_mebel_table(self, conn):
        cursor_object = conn.cursor()
        cursor_object.execute(
            """
                CREATE TABLE IF NOT EXISTS app_1_mebel
                (
                    id integer PRIMARY KEY autoincrement, 
                    link text UNIQUE, 
                    price integer, 
                    description text
                )
            """
        )
        conn.commit()

    def get_items(self, conn, price_from=0, price_to=100000):
        cursor = conn.cursor()
        cursor.execute(
            f'SELECT link, price, description FROM app_1_mebel WHERE price >= {price_from} and price <= {price_to}')
        return cursor.fetchall()

    def insert(self, conn, link, price, description):
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"INSERT INTO app_1_mebel (link, price, description) VALUES ('{link.split('?')[0]}', '{price}', '{description}')")
        except sqlite3.Error:
            pass
        finally:
            conn.commit()


class CSVClient(DataClient):
    def get_connection(self):
        return None

    def create_mebel_table(self, conn):
        return None

    def get_items(self, conn, price_from=0, price_to=100000):
        try:
            df = pandas.read_csv('mebel.csv')
            df_filtered = df.query('price >= @price_from and price <= @price_to')
        except:
            return None
        return df_filtered.values.tolist()

    def insert(self, conn, link, price, description):
        link = link.split('?')[0]
        try:
            df = pandas.read_csv('mebel.csv')
            unique = link not in df['link'].tolist()
            header = False
        except:
            header = True
            unique = True

        if unique:
            item = {
                'link': [link],
                'price': [price],
                'description': [description]
            }

            pandas.DataFrame(item).to_csv('mebel.csv', mode='a', index=False, header=header)
