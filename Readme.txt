How did I test it?
- From Terminal python3 API.py
- The Uvicorn web server runs
- Opened the http://127.0.0.1:8000/docs localhost
- Used the RESTful API Methods from the localhost

Methods:
1. on_event(startup)
- On Startup, a BGManager.run_main is ran asynchronously with asyncio in the background.
- On Startup, the Database is checked for results = null. All these table rows are putted into the queue,
computed and updated in the Database with the computed result.

2. POST
- I used the pydantic BaseModel to guarantee the types and pass the how Polynomial-object aka. the cubic equation
- After invoking the put method of the BGManager, the model is written directly to the Database.
- The BGManager has an instance of the DBManager to put and retrieve polynomials to and from the Database.
- The class holds an SQLite wrapper and manages the connection and statements for the Database.
- After the model is inserted into the DB, an ID is retrieved and returned to the POST method.
- Before returning the ID to the POST method, the model and its DB-ID are passed to a queue as a pair for calculation.
- To ensure that there is not a linear calculation time for the polynomials entering the queue, 
every polynomial has a random calculation time.
- The queue worker method is invoked in X threads to accelerate the calculation in the queue. 
- The self.calc_queue.get() blocks the worker until a new item can be retrieved from the queue
- The C++ shared library is invoked in the worker method. For the bindings, I've used ctypes.
- After the compute, the object is updated in the DB over its ID, which is passed to the queue with the model. 

3. GET{ID}
- Invokes the get method of the BGManager and passes the entered ID to it, 
which is invoking the get_polynomial method of the instance of the DBManager.
- The Database is opened and the row with the respective ID is retrieved. 
- If there is a polynomial behind the ID, the polynomial with its result, computed or not, are returned. 
- If there is no polynomial-data behind the ID, Code 204 "No Content" is returned. 
- The retrieved data is prepared in a dictionary and returned to the API GET method. 
- The FastAPI converts the data directly into JSON.

4. GET
- Invokes the get method of the BGManager, but this time no ID is passed.
- The GET works in the same way as the GET{ID}, but the invoked method get without an ID
retrieves all polynomials from the Database and it returns a list of polynomial dictionaries. 

