from fastapi import FastAPI
import uvicorn
from backgroud_manager import BGManager, asyncio, CubicEQN

background_manager = BGManager()
app = FastAPI()

# Run main on startup. 
# Create a new asynchronous task
@app.on_event('startup')
async def app_startup():
        asyncio.create_task(background_manager.run_main())
        
# Add new polynomial to the db and queue
# Return an ID of the newly inserted polynomial
@app.post("/polynomial")
def add(model_ce: CubicEQN):
    return background_manager.put(model_ce)

# Get a single polynomial with the passed id        
@app.get("/polynomial/{id}")
def get_single(id:int):
    return background_manager.get_elem(id)

# Get all polynomials 
@app.get("/polynomial")
def get_list():
    return background_manager.get_lst()

# Run uvicorn 
if __name__ == "__main__":
    uvicorn.run("API:app", host="127.0.0.1", 
                port=8000, reload=True, 
                access_log=False)