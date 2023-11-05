import sqlite3
from exceptionHandler import DuplicateError

class SQLiteDAO:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            print(f'Connected to {self.db_name} successfully.')
        except sqlite3.Error as e:
            print(f'Error connecting to the database: {e}')

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print('Disconnected successfully.')

    def delete_table(self, table_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"DROP TABLE {table_name}")
            self.conn.commit()
            print(f'Table {table_name} deleted successfully.')
        except sqlite3.Error as e:
            print(f'Error deleting the table: {e}')
        finally:
            cursor.close()

    def create_table(self, table_name, params):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f'CREATE TABLE {table_name} ({params})')
            self.conn.commit()
            print(f'Table {table_name} created successfully.')
        except sqlite3.Error as e:
            print(f'Error creating the table: {e}')
        finally:
            cursor.close()

    def insert_row(self, table_name, row_tuple):
        # Row values are a dictionary representing the row.
        if not isinstance(row_tuple, dict):
            raise ValueError("row_tuple should be a dictionary")

        keys = row_tuple.keys()
        values = list(row_tuple.values())

        str_keys = ",".join(keys)
        str_values = ",".join(["?"] * len(row_tuple))

        query = f"INSERT INTO {table_name} ({str_keys}) VALUES ({str_values})"
        print(query)
        cursor = self.conn.cursor()

        try:
            cursor.execute(query, values)
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            raise DuplicateError("duplicated record")
        finally:
            cursor.close()
    
    def insert_rows(self, table_name, row_tuples):
        # Assert each row tuples have the same length and keys
        keys = row_tuples[0].keys()
        multiple_values = []
        for row_tuple in row_tuples:
            if row_tuple.keys() != keys:
                raise ValueError("batch should have same keys")
            multiple_values.append(list(row_tuple.values()))
        
        str_keys = ",".join(keys)
        str_values = ",".join(["?"] * len(row_tuple))
        
        query = f"INSERT OR IGNORE INTO {table_name} ({str_keys}) VALUES ({str_values})"
        cursor = self.conn.cursor()

        duplicated_records = []
        for values in multiple_values:
            try:
                cursor.execute(query, values)
                self.conn.commit()
            except sqlite3.IntegrityError as e:
                duplicated_records += values
        
        cursor.close()

        if duplicated_records:
            raise DuplicateError(f"{duplicated_records}")

    def get_rows(self, table_name, row_tuple):
        # Row values are a dictionary representing the row.
        if not isinstance(row_tuple, dict):
            raise ValueError("row_tuple should be a dictionary")

        str_where = ", ".join([f"{key}='{value}'" for key, value in row_tuple.items()])

        query = f"SELECT * FROM {table_name} WHERE {str_where}"
        cursor = self.conn.cursor()

        result = []
        try:
            cursor.execute(query)
            result = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing SQL query: {e}")
        finally:
            cursor.close()

        return result

    def delete_rows(self, table_name, row_tuple):
        if not isinstance(row_tuple, dict):
            raise ValueError("row_tuple should be a dictionary")

        str_where = " AND ".join([f"{key}=?" for key in row_tuple.keys()])
        query = f"DELETE FROM {table_name} WHERE {str_where}"
        values = list(row_tuple.values())

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, values)
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            raise Exception(f"Error executing SQL query: {e}")
        finally:
            cursor.close()

    def reset_database(self):
        self.delete_table("songs")
        self.delete_table("artists")
        self.create_table("artists", "artist_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                                      name TEXT NOT NULL UNIQUE")
        self.create_table("songs", "song_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                                    artist_id INTEGER, \
                                    title TEXT NOT NULL, \
                                    UNIQUE (artist_id, title), \
                                    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)")
