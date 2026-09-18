from fastmcp import Client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from google import genai

class ChatRequest(BaseModel):
    prompt: str

app = FastAPI()
client = Client("http://mcp-server:8000/mcp/")
gemini_client = genai.Client()

@app.on_event("startup")
async def startup_event():
    await client.__aenter__()

@app.on_event("shutdown")
async def shutdown_event():
    await client.__aexit__()

@app.post("/ask")
async def ask(payload: ChatRequest):
    try:
        response = await asyncio.wait_for(
            gemini_client.aio.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=payload.prompt,
                    config=genai.types.GenerateContentConfig(
                        temperature=0,
                        tools=[client.session],
                    ),
                    ),
            timeout=60.0
        ) 
        return {"response": response.text}
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Request to Gemini timed out")
    except Exception as e:
        error_text = str(e)
        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            raise HTTPException(status_code=429, detail=error_text)
        raise HTTPException(status_code=500, detail=str(e))
