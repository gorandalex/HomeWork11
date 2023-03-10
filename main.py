import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request 
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.routes import contacts, auth
from src.database.db import get_db

app = FastAPI(title='Contacts')

app.include_router(contacts.router)
app.include_router(auth.router)


@app.get('/')
async def root():
    return {'message': 'Contacts'}

@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error connecting to the database")



if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
