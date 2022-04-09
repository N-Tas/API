from sql_functions import SQLite
from polynomial_components import CubicEQN, PolynomialDict
import re

# -------------------------------------------------------------------
# Wraper for the SQLite class
# -------------------------------------------------------------------
class DBManager:
# -------------------------------------------------------------------
# PRIVATE 
# ------------------------------------------------------------------- 
    # Create the DB and its table
    def __init__(self, conn_name="Polynomial.db"):
        self.database = SQLite(conn_name)
        self.COLUMNS = 7
        self.__SQLite_create_table()
        
    # Create the DB if doesn't exist on object creation
    def __SQLite_create_table(self):  
        self.database.connect()     
        self.database.execute("""CREATE TABLE IF NOT EXISTS POLYNOMIAL(
                    ID        INTEGER NOT NULL UNIQUE NOT NULL, 
                    x         REAL NOT NULL, 
                    a0        REAL NOT NULL, 
                    a1        REAL NOT NULL, 
                    a2        REAL NOT NULL, 
                    a3        REAL NOT NULL,
                    result    REAL,
                    PRIMARY KEY(ID AUTOINCREMENT))"""
        )
        self.database.disconnect()  
        
    # Get polynomials from the DB
    # id!=None single polynomial else all polynomials 
    def __SQLite_get(self, statement, id=None):
        self.database.connect()
        if id != None:
            table_content = self.database.execute(statement,(id,), fetch= True)
        else:
            table_content = self.database.execute(statement, fetch= True)
        self.database.disconnect()
        return table_content 
    
    # Extract all the values from the columns in the given table row
    def __prep_dict(self,table_row):
        table_column = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", str(table_row))
        cubic_dict = PolynomialDict()
        cubic_dict.add('ID', table_column[0])
        cubic_dict.add('x', table_column[1])
        cubic_dict.add('polynomial', [table_column[2],table_column[3],table_column[4],table_column[5]])
        if len(table_column) != self.COLUMNS:
            cubic_dict.add('result',None)
        else:
            cubic_dict.add('result',table_column[6])
        return cubic_dict
# -------------------------------------------------------------------
# PUBLIC 
# ------------------------------------------------------------------- 
    # Insert the polynomial after POST into the DB
    # Returns the ID of the inserted polynomial    
    def put_polynomial(self, model_ce: CubicEQN):    
        self.database.connect()
        self.database.execute("INSERT INTO POLYNOMIAL (x, a0, a1, a2, a3, result) VALUES(?,?,?,?,?,?)", 
                    (model_ce.x,model_ce.polynomial[0],model_ce.polynomial[1],model_ce.polynomial[2],
                    model_ce.polynomial[3],None)
        )
        row_id = self.database.get_id()
        self.database.disconnect()
        return row_id
    
    # Update the result of the selected polyomial after the heavy calc
    def update_polynomial(self, id, result):
        self.database.connect()
        self.database.execute("UPDATE POLYNOMIAL SET result = ? WHERE ID=?",(result,id)) 
        self.database.disconnect()
       
    # Extract a list or single elem. from the DB
    # Prep. the data to be returned
    def get_polynomial(self, statement, id=None):
        if id != None:
            single_polynomial = self.__SQLite_get(statement,id)
            if single_polynomial:
                return self.__prep_dict(single_polynomial)
            else:
                return None  
        else:
            table_content = self.__SQLite_get(statement) 
            if table_content:
                lst_polynomials = []
                for row in table_content:
                    lst_polynomials.append(self.__prep_dict(row))
                return lst_polynomials
            else:
                return None