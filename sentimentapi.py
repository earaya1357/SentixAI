from fastapi import FastAPI
from geminiapi import askgemini
import json
from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/basicsentiment/company/product')
async def basicsentiment(comment:str):
    data = askgemini(comment)
    data = json.loads(data.replace('`','').replace('json', ''))
    #print(f'Sentiment: {data['sentiment']}\nStrength: {data['strength']}\nVader Score: {data['vader_score']}')
    return {'answer': data}

