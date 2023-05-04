import dotenv
dotenv.load_dotenv()

from fastapi import FastAPI
import geopandas as gpd
import pandas as pd
import json
from connections import connections
from fastapi.middleware.cors import CORSMiddleware
from glob import glob

app = FastAPI()
origins = ["http://localhost:8000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = connections.redis

@app.get("/heatmaps")
async def read_item(size: int=1,data: bool=True,map: bool=True):

    file_path = glob(f'/data/warehouse/hexgrid_{size}.geojson')
    ret = json.load(open(file_path[0]))
    
    
    return ret

