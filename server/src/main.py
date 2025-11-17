from fastapi import FastAPI
from dotenv import load_dotenv
import os


load_dotenv()
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "backend api is online. (:"}

'''
# example on how to grab key: value loads at serverip/debug-key
# dont keep this for security reasons
@app.get("/debug-key")
def check_key():
    key = os.getenv("EBIRD_API_KEY")
    return {"key-status": "loaded" if key else "missing"}
'''