import sqlite3
import os
import pandas as pd
from pandas.core.frame import DataFrame
import namegenerator

class SQLiteManager:
    '''
        a Manager class to help with SQL queries
    '''

    def __init__(self) -> None:
        self.store_location = os.path.join(os.path.expanduser('~'), '.gsql', 'databases')
        os.makedirs(self.store_location, exist_ok=True)
        self.common_db_path = os.path.join( self.store_location ,  'common.db')

    def _write_to_common(self, resultset):

        # convert the resultset dictionary into a set of tuples
        insert_list = []
               
        con = sqlite3.connect(self.common_db_path)
        curr = con.cursor()
        curr.execute("create table if not exists common (title varchar(50), id varchar(50) primary key, \
             nickname varchar(50))")
        
        table = pd.read_sql_query("select * from common", con)
        for content in resultset:
            if content['id'] not in table['id'].tolist():
                insert_list.append((content['title'], content['id'], namegenerator.gen()))


        
        curr.executemany("replace into common values(?, ?, ?);", insert_list)

        con.commit()
        con.close()

    def _read_from_common(self) -> pd.DataFrame:

        con = sqlite3.connect(self.common_db_path)
        table = pd.read_sql_query("select * from common", con)        
        con.close()
        return table


    def read_generic_select_statement(self, table_name, statement ) -> pd.DataFrame:
        '''
            reads content from the database corresponding to a table name
            and wraps it in a dataframe

            params
            -------
            table_name : Name of the table (str)            
            statement : raw SQL statement to be passed on to SQLite
        '''
        db_path = os.path.join(self.store_location, table_name + '.db')
        con = sqlite3.connect(db_path)
        table = pd.read_sql_query(statement, con)
        con.close()
        return table

    
    def write_metadata(self, metadata) -> None:
        
        # preparing the metadata into tuple
        insert_list = []
        db_id = metadata["spreadsheetId"]
        db_name = metadata["title"]

        for sheet in metadata['sheets']:
            properties = sheet['properties']
            insert_list.append((db_id, db_name, properties['sheetId'], properties['title'], 
                properties['gridProperties']['rowCount'], properties['gridProperties']['columnCount']))

        
        metadata_path = os.path.join( self.store_location , 'metadata_{}.db'.format(db_id))
        con = sqlite3.connect(metadata_path)
        curr = con.cursor()        
        curr.execute("create table if not exists metadata (db_id varchar(50), db_name varchar(50), \
             sheet_id varchar(20) primary key, sheet_title varchar(50), row_count integer, col_count integer)")
        curr.executemany("replace into metadata values(?, ?, ?, ?, ?, ?)" , insert_list)
        con.commit()
        con.close()

    def read_metadata(self, db_id) -> pd.DataFrame: 
        '''
            reads out the data corresponding to a particular ID
        '''

        metadata_path = os.path.join( self.store_location , 'metadata_{}.db'.format(db_id))
        con = sqlite3.connect(metadata_path)
        table = pd.read_sql_query("select * from metadata", con)
        con.close()
        return table
        
        
        





            
