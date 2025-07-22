from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from langchain_openai import ChatOpenAI 
from .testStream import chain
from .database.model import add_user, get_all_users
from pydantic import BaseModel
from typing import List, Tuple

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,    
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# Pydantic models for API
class UserCreate(BaseModel):
    user_id: str
    user_name: str
    user_password: str

class UserResponse(BaseModel):
    user_id: str
    user_name: str
    user_password: str

# User API endpoints
@app.post("/users/add_user", response_model=dict, tags=["users"])
async def create_user(user: UserCreate):
    """Add a new user to the database."""
    try:
        add_user(user.user_id, user.user_name, user.user_password)
        return {"message": "User added successfully", "user_id": user.user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding user: {str(e)}")

@app.get("/users/get_all", response_model=list, tags=["users"])
async def get_users():
    """Retrieve all users from the database."""
    try:
        users = get_all_users()
        if users is None:
            return []
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {str(e)}")

add_routes(
    app,
    ChatOpenAI(model='gpt-3.5-turbo'),
    path="/openai"
)

add_routes(
    app,
    chain,
    path="/chain"
)



# Edit this to add the chain you want to add

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
