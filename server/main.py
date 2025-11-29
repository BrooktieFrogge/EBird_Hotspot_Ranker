from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from routes import hotspots,rankings,species

#load environment variables and initialize app
load_dotenv()
app = FastAPI()

# update to include frontend origin/hosting info 
origins = ["http://localhost:5173/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(rankings.router)
app.include_router(hotspots.router)

@app.get("/")
def main():
    return {"messege":"backend online"}
