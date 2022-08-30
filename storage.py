import sqlite3
import pandas as pd

class DBStorage():
    def __init__(self):
        self.con = sqlite3.connect('links.db')
        self.setup_tables()

    def setup_tables(self):
        cur = self.con.cursor()
        results_table = r"""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                query TEXT,
                rank INTEGER,
                link TEXT,
                title TEXT,
                snippet TEXT,
                html TEXT,
                created DATETIME,
                relevance INTEGER,
                UNIQUE(query, link)
            );
            """
        cur.execute(results_table)
        self.con.commit()
        cur.close()

    def query_results(self, query):
        '''
        when passing in a query, it returns all of the results that exist in the database
        :param query: input query
        :return: results already stored in database for the input query
        '''
        df = pd.read_sql_query(f"select * from results where query='{query}' order by rank asc;", self.con)
        return df

    def insert_row(self, values):
        '''
        insert a row into the database
        :param values:
        :return:
        '''
        cur = self.con.cursor()
        try:
            cur.execute('INSERT INTO results (query, rank, link, title, snippet, html, created) VALUES(?,?,?,?,?,?,?)', values)
            self.con.commit()
        except sqlite3.IntegrityError:
            pass

        cur.close



