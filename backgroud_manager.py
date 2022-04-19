import asyncio
import threading
import queue

from markupsafe import re
from polynomial_components import CubicEQN, Pair, Bindigns
from database_manager import DBManager

# -------------------------------------------------------------------
# Manages the queue & com. to the DB
# Works in the background
# -------------------------------------------------------------------
class BGManager:
# -------------------------------------------------------------------
# PRIVATE
# -------------------------------------------------------------------  
    def __init__(self):
        self.calc_queue = queue.Queue()
        self.db_manager = DBManager("Polynomial.db")
        self.bindings = Bindigns("lib_heavy_calc.so")
        self.first_call = True 
        self.DECIMAL_POINT = 4
        self.NO_CONTENT = 204
        
    # Call the C++ lib, compute and update the db
    def __worker(self):
        while True:
            # Wait if the q is empty get item from the q 
            item = self.calc_queue.get()
            # INFO LOG
            print("-----------------------------------------------------------")
            print("Computing:")
            print("ID:{id}".format(id= item.id))
            print("Polynomial: {poly}".format(poly= item.model_ce))
            print("-----------------------------------------------------------")
            # Compute with the C++ lib
            result,compute_time = self.bindings.polynomial_calc(item.model_ce) 
            # Round the result 1/10000
            result = round(result,self.DECIMAL_POINT)
            # Update the polynomial with the computed result over its ID
            self.db_manager.update_polynomial(item.id,result)
            # INFO LOG
            print("-----------------------------------------------------------")
            print("Computed in {c_time} sec.:".format(c_time= compute_time))
            print("ID:{id}".format(id= item.id))
            print("Result:{res}".format(res= result))
            print("-----------------------------------------------------------")
            # Pop the computed item from the q
            self.calc_queue.task_done()                  
# -------------------------------------------------------------------
# PUBLIC 
# -------------------------------------------------------------------       
    # Insert the polynomial from the POST
    # Get an ID from the DB return it to the POST
    # Put the Cubical with its ID in the queue
    def put(self, model_ce : CubicEQN):    
        row_id = self.db_manager.put_polynomial(model_ce)
        if row_id:
            self.calc_queue.put(Pair(row_id,model_ce))  
        return row_id  
        
    # Get the polynomial with the selected ID from the DB or a list
    def get(self, id=None):
        response = None
        if id != None:
            response = self.db_manager.get_polynomial(statement="SELECT* FROM POLYNOMIAL WHERE ID=?",id=id)
        else:
            response = self.db_manager.get_polynomial(statement="SELECT * FROM POLYNOMIAL") 
        # Retrurn the result    
        if response:
            return response
        else:
            return self.NO_CONTENT
    
    # Call main
    async def run_main(self):
        # Threads for worker. Added 2 for faster computation 
        threading.Thread(target=self.__worker, daemon=True).start()
        threading.Thread(target=self.__worker, daemon=True).start()   
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
             
        # Retrieve all not computed polynomials from the DB and put those in a queue
        # Run once on object creation
        if self.first_call:
            self.first_call = False
            lst_content = self.db_manager.get_polynomial(statement="SELECT* FROM POLYNOMIAL WHERE result IS NULL")
            if lst_content:
                for elem in lst_content:
                    elem_x = elem.get("x")
                    elem_polynomial = elem.get("polynomial")
                    row_id = int(elem.get("ID"))
                    model_ce = CubicEQN(x= elem_x, polynomial= elem_polynomial)
                    self.calc_queue.put(Pair(row_id,model_ce)) 
             
                    
        while True:
            # await to finish 
            await asyncio.sleep(0.1)
            