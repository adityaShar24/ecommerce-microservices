from fastapi import FastAPI
from .database import engine



app = FastAPI()


@app.get("/")
def read_root():
    return {"message":"auth service is running"}

if __name__ =="__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)