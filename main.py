from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
import uvicorn

from src.database.db import get_db

from src.routes import contacts, auth


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Application started"}

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')



@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

if __name__ == "__main__":
    uvicorn.run(app)