from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import database, model, schema, auth



app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message":"auth service is running"}


@app.post('/register', response_model=schema.UserOut)
def register_user(user: schema.UserCreate , db: Session = Depends(get_db)):
    db_user = db.query(model.User).filter(model.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400 , detail= "Email already registered")
    
    hashed_password = auth.hash_password(user.password)
    new_user = model.User(full_name = user.full_name , email= user.email , hashed_password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

if __name__ =="__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)