from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat_llm import service_provider, service_register


app = FastAPI(openapi_url="/openapi.json", docs_url="/docs")
users = {}


class User:
    def __init__(self, is_provider: bool):
        if is_provider:
            self.agent = service_register()
        else:
            self.agent = service_provider()
        self.llm = self.agent.create_llm()


class ChatInput(BaseModel):
    text: str


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, you can specify domains instead
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.post('/start/{user_id}')
def start_chat(user_id: str, is_provider: bool = False):
    if user_id not in users:
        users[user_id] = User(is_provider)
        return {"message": "Chat started", "user_id": user_id}
    else:
        raise HTTPException(status_code=400, detail="User already exists")


@app.post('/chat/{user_id}')
def chat(user_id: str, input_data: ChatInput):
    if user_id in users:
        user = users[user_id]
        response = user.llm.run(input_data.text)
        print("Person Input: ", input_data.text)
        print("GPT Response: ", response)
        return {"response": response}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.post('/stop/{user_id}')
def stop_chat(user_id: str):
    if user_id in users:
        del users[user_id]
        return {"message": "Chat stopped", "user_id": user_id}
    else:
        raise HTTPException(status_code=404, detail="User not found")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000)
