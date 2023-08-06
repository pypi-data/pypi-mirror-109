"""A module with a class called OpenSqlite3db that handles sqlite 3 db with the "with" statement """

import sqlite3


class OpenSqlite3db:
    """
    The classe that you can with the open statement to open SQLite databases

    Examples:
        with OpenSqlite3db(db_path="database.db", throw_error=True) as (conn, cursor):
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users
            ''')

        NOTE:
            It will automatically commit, close cursor and connection

    Documentation:
        You shouldn't forget about the parentisis after the "as"

        Arguments:
            "db_path" Path to the database (can be Pathlib path) (default to "database.db")

            "throw_error" Weather you want to throw an error or not (default to True)

        Note:
            None of these arguments are required

    """
    def __init__(self, db_path="database.db", throw_error=True):
        self.db = str(db_path)
        self.throw_error = throw_error

    def __enter__(self):
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()
        return self.connection, self.cursor

    def __exit__(self, ex_type, exc_val, exc_tb):
        # Commiting and closing cursors
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        # The boolean that __exit__ returns is weather or not it'll catch errors
        return not self.throw_error
