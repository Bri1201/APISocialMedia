from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import Model
from database import engine
from Routers import Auth, Users, vote, Posts

Model.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# path operation
# Decorator makes it act like an API and turns into an actual path operation
# app=fastApi reference and .get is the method that sends the get method to the API
# ("/") is the root path in the url
app.include_router(Posts.router)
app.include_router(Users.router)
app.include_router(Auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    # async for ansynchronous tasks
    # whatever we return gets sent to the user
    # fast api automatically converts the dictionary to json
    return {"message": "Welcome to My API!!!"}
