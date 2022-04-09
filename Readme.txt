How did I test it?
- From Terminal python3 API.py
- Uvicorn runs
- Opened the http://127.0.0.1:8000/docs localhost
- Used the RESTful API Methods from the localhost

Methods:
1. on_event(startup)
- On Startup, a BackgroundManager.run_main is ran asynchronously with asyncio in the background.
- On Startup, the DB is checked for results = null. All these table rows are putted into the queue,
computed and updated in the DB with the result.

2. POST
- I used the pydantic BaseModel to guarantee the types and pass the how Polynomial-object aka. the cubic equation
- After invoking the put method of the BackgroundManager, the model is written directly to the DB.
- The BackgroundManager has an instance of the DBManager Class. 
- The Class wraps SQLite methods and manages the connection and statements for the DB.
- After the model is inserted into the DB, an ID is retrieved and returned to the POST method.
- Before returning the ID to the POST method, the model and its DB-ID are passed to a queue as a pair for calculation.
- The queue worker method is invoked in X threads to accelerate the calculation in the queue. 
- The self.calc_queue.get() blocks the worker until a new item can be retrieved from the queue
- The C++ shared library is invoked in the worker method. For the bindings, I've used ctypes.
- After the compute, the object is updated in the DB over its ID, which is passed to the queue with the model. 

3. GET{ID}
- Invokes the get_elem method of the BackgroundManager, which is invoking the get_data method of the instance of the DB manager.
- The DB is opened and the row with the respective ID is retrieved.
- The retrieved data is prepared in a dictionary and returned to the API GET method. 
- The FastAPI is converting the data directly into JSON.

4. GET
- Invokes the get_list method of the BackgroundManager.
- The GET works in the same way as the GET{ID}, but it returns a list of polynomial dictionaries. 

