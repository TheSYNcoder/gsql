
from gsql.exceptions.sqlparser_exception import SQLStatmentException
import sqlparse
from sqlparse.tokens import Keyword, DML, DDL, Punctuation
import sqlvalidator



class SQLTokens:

    SELECT = 'SELECT'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    INSERT = 'INSERT'
    ALTER = 'ALTER'
    CREATE = 'CREATE'
    ERROR = 'ERROR'


class SQLDTO:

    def __init__(self, raw_statement, table_name='sample table', 
        type_statement: SQLTokens = SQLTokens.SELECT, 
        affected_columns = [],updated_values = {}, deleted_columns = {}, 
        filter_function = None
        ) -> None:
        '''
            raw_statement : The raw SQL statement passed to the GSQL shell
            table_name : The table corresponding to the query
            type_statement : Type of the SQL query determined by SQLTokens
            affected_columns : The name of the columns affected by the query
                        will be [] in case of select queries.
            updated_values : a mapping of table names to the updated values
                    will be empty in all queries except update and insert
            filter_function : A lambda expression to filter rows based on parameters will be None 
                for SQL queries
        '''
        pass


class SQLParser:

    def __init__(self ) -> None:
        self.db_id = None
        self.db_name = None

    @property
    def database(self):
        return self.db_id
    
    @database.setter
    def database(self, db_id):
        self.db_id = db_id
    
    @database.deleter
    def database(self):
        self.db_id = None

    def _validate_statement(self, raw_statement):        
        parsed = sqlvalidator.parse(raw_statement)
        if not parsed.is_valid():
            raise SQLStatmentException("gsql: error: SQL SELECT Query not valid : " + str(parsed.errors))        


    def classify_statement(self, parsed):
        first_token = parsed.tokens[0]
        if first_token.ttype == DML and first_token.value.upper() == SQLTokens.SELECT:
            return SQLTokens.SELECT
        elif first_token.ttype == DML and first_token.value.upper() == SQLTokens.UPDATE:
            return SQLTokens.UPDATE
        elif first_token.ttype == DML and first_token.value.upper() == SQLTokens.INSERT:
            return SQLTokens.INSERT
        elif first_token.ttype == DML and first_token.value.upper() == SQLTokens.DELETE:
            return SQLTokens.DELETE
        elif first_token.ttype == DDL and first_token.value.upper() == SQLTokens.ALTER:
            return SQLTokens.ALTER
        elif first_token.ttype == DDL and first_token.value.upper() == SQLTokens.CREATE:
            return SQLTokens.CREATE
        else:
            return SQLTokens.ERROR
        

    def handle_select_statement(self, statement):
        # self._validate_statement(statement)
        # TODO connect to sqlite to get the result from sqlite 
        print('SELECT' , statement)
    
    def handle_update_statement(self, statement):
        '''
            prepare a DTO based on parsed update statement
            The DTO is to be passed on for making further API calls
        '''
        print('UPDATE' , statement)
    
    def handle_insert_statement(self, statement):
        '''
            prepare a DTO based on parsed insert statement
            The DTO is to be passed on for making further API calls
        '''
        print('INSERT' , statement)
    
    def handle_delete_statement(self, statement):
        '''
            prepare a DTO based on parsed delete statement
            The DTO is to be passed on for making further API calls
        '''
        print('DELETE' , statement)
    
    def handle_alter_statement(self, statement):
        '''
            prepare a DTO based on parsed alter statement
            The DTO is to be passed on for making further API calls
        '''
        print('ALTER' , statement)
    
    def handle_create_statement(self, statement):
        '''
            prepare a DTO based on parsed create statement
            The DTO is to be passed on for making further API calls
        '''
        print('CREATE' , statement)
    

    def handle_statement(self, statement):
        class_token = self.classify_statement(statement)
        if class_token == SQLTokens.ERROR:
            raise SQLStatmentException("gsql: error: invalid statement")
        if class_token == SQLTokens.SELECT:
            self.handle_select_statement(statement)
        if class_token == SQLTokens.UDPATE:
            self.handle_update_statement(statement)
        if class_token == SQLTokens.INSERT:
            self.handle_insert_statement(statement)
        if class_token == SQLTokens.DELETE:
            self.handle_delete_statement(statement)
        if class_token == SQLTokens.ALTER:
            self.handle_alter_statement(statement)
        if class_token == SQLTokens.DELETE:
            self.handle__statement(statement)



    def parse_statement(self, raw_statement: str):
        '''
            raw_statement : raw SQL statement 
        '''
        # get rid of the white spaces
        raw_statement = raw_statement.strip()
        parsed = sqlparse.parse(raw_statement)
        if self.db_id is None:
            raise SQLStatmentException("Please connect to a database before continuing, \
                type help connect for more info")
        
        for statement in parsed:
            tokens = statement.tokens
            if tokens[-1].ttype != Punctuation or tokens[-1].value != ';':
                raise SQLStatmentException("Expected ; at the end of a SQL statement")
            self.handle_statement(statement)            



