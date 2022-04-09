import sqlite3
import threading
# -------------------------------------------------------------------
# Class to manege the connection with the DB
# All methods can be packed in one
# -------------------------------------------------------------------
class SQLite:
    # Construct the object
    def __init__(self, conn_name):
        self.conn = None
        self.cursor = None
        self.conn_name = conn_name
        self.lock = threading.Lock()
        
    # Explicit connect 
    # Must complete before every other method is called 
    def connect(self):  
        try:
            self.lock.acquire()
            self.conn = sqlite3.connect(self.conn_name)
            self.cursor = self.conn.cursor()
        except:
            print("SQLite: connect failed")
            if self.lock.locked():
                self.lock.release()
                
    # Execute statement. 
    # Commit will be execute on connection close         
    def execute(self,statement, val=None, fetch=False):
        try:
            if val != None:
                self.cursor.execute(statement,val)     
            else:
                self.cursor.execute(statement)
            # Fetch on demand     
            if fetch:
                return self.cursor.fetchall()
        except:
            print("SQLite: execution failed")   
            
   # Get the ID of the newly imported row   
    def get_id(self):
            try:
                return self.cursor.lastrowid
            except:
                print("SQLite: fetch ID failed")
                
    # Explicit commit and disconnect 
    # Must be called after every connect      
    def disconnect(self):
        try:
            self.conn.commit()
            self.conn.close()
        except:
            print("SQLite: disconnect failed")
        finally:
            if self.lock.locked():
                self.lock.release()
        
 
 

        
       
  