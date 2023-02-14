import uvicorn
from fastapi import FastAPI

from src.routes import contacts

app = FastAPI(title='Contacts')

app.include_router(contacts.router)


@app.get('/')
async def root():
    return {'message': 'Contacts'}


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
