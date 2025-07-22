from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from langchain_openai import ChatOpenAI 
from .testStream import chain
from .recommend import Recommender
from .database.model import add_user, get_all_users, update_history_name_by_id
from .database.model import add_history_info, add_history_content, delete_history_info
from .database.model import get_all_history_info, get_history_content_by_id
from pydantic import BaseModel

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

add_routes(
    app,
    Recommender,
    path="/recommender"
)

# Pydantic models for API
class UserCreate(BaseModel):
    user_id: str
    user_name: str
    user_password: str

class UserResponse(BaseModel):
    user_id: str
    user_name: str
    user_password: str

class HistoryInfoCreate(BaseModel):
    history_id: str
    history_name: str
    user_id: str

class HistoryContentCreate(BaseModel):
    id: str
    index: int 
    role: str
    content: str

class HistoryNameUpdate(BaseModel):
    new_name: str

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

# History API endpoints
@app.get("/history/get_all_info", response_model=list, tags=["history"])
async def get_all_history():
    """Retrieve all history information from the database."""
    try:
        history_info = get_all_history_info()
        if history_info is None:
            return []
        return history_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history info: {str(e)}")

@app.get("/history/get_content/{history_id}", response_model=list, tags=["history"])
async def get_history_content(history_id: str):
    """Retrieve history content by history ID."""
    try:
        history_content = get_history_content_by_id(history_id)
        if history_content is None:
            return []
        return history_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history content: {str(e)}")

@app.post("/history/add_info", response_model=dict, tags=["history"])
async def create_history_info(history_info: HistoryInfoCreate):
    """Add history information to the database."""
    try:
        add_history_info(history_info.history_id, history_info.history_name, history_info.user_id)
        return {"message": "History info added successfully", "history_id": history_info.history_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding history info: {str(e)}")

@app.post("/history/add_content", response_model=dict, tags=["history"])
async def create_history_content(history_content: HistoryContentCreate):
    """Add history content to the database."""
    try:
        add_history_content(history_content.id, history_content.index, history_content.role, history_content.content)
        return {"message": "History content added successfully", "content_id": history_content.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding history content: {str(e)}")

@app.delete("/history/delete/{history_id}", response_model=dict, tags=["history"])
async def delete_history(history_id: str):
    """Delete history information and content by history ID."""
    try:
        delete_history_info(history_id)
        return {"message": "History deleted successfully", "history_id": history_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting history: {str(e)}")

@app.put("/history/update_name/{history_id}", response_model=dict, tags=["history"])
async def update_history_name(history_id: str, history_name_update: HistoryNameUpdate):
    """Update history name by history ID."""
    try:
        update_history_name_by_id(history_id, history_name_update.new_name)
        return {"message": "History name updated successfully", "history_id": history_id, "new_name": history_name_update.new_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating history name: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
