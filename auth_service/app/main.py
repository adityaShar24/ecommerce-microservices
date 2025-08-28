from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import database, model, schema, auth
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from .publisher import publish_message

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = auth.verify_access_token(token, credentials_exception)
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

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
    publish_message({
        "action": "create_user",
        "data": {
            "user_id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name
        }
    })
    return new_user

@app.post('/login', response_model=schema.Token)
def login(user_cred: schema.UserLogin, db :  Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == user_cred.email).first()


    if not user:
        raise HTTPException(status_code=400 , detail = "Invalid Credentials")
    
    if not auth.verify_password(user_cred.password, user.hashed_password):
        raise HTTPException(status_code=400 , detail= 'Invalid Credentials')

    access_token = auth.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@app.post('/refresh', response_model=schema.Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    user_id = auth.verify_refresh_token(refresh_token)
    access_token = auth.create_access_token(data={"user_id": user_id})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post('/reset-password')
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    user_id = auth.verify_reset_token(token)
    user = db.query(model.User).filter(model.User.id == user_id).first()
    user.hashed_password = auth.hash_password(new_password)
    db.commit()
    return {"message": "Password reset successful"}


@app.post('/change-password')
def change_password(current_password: str, new_password: str, user: model.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not auth.verify_password(current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    user.hashed_password = auth.hash_password(new_password)
    db.commit()
    return {"message": "Password changed successfully"}


@app.get('/profile', response_model=schema.UserOut)
def get_profile(user: model.User = Depends(get_current_user)):
    return user

if __name__ =="__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)