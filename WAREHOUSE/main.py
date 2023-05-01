import dotenv
dotenv.load_dotenv()

from fastapi import FastAPI
import geopandas as gpd
import pandas as pd
import json
from connections import connections
from fastapi.middleware.cors import CORSMiddleware


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
    if redis.get(f"agg_{size}") is None:
        aggregate_data(size)
    ret = dict()
    if data:
        ret["agg_data"] = json.loads(redis.get(f"agg_{size}"))
    if map:
        gdf_geometry = gpd.read_file(f'../geojson/hexgrid_{size}.geojson')
        gdf_geometry["partition"] = gdf_geometry.index
        gdf_geometry_json = json.loads(gdf_geometry.to_json())
        ret["geojson_data"] = gdf_geometry_json
    return ret

#post aggregate data
@app.post("/heatmaps/aggregate/{size}")
async def aggregate_data(size:int=1):
    #load geojson of hex bin data from json
    gdf_geometry = gpd.read_file(f'../geojson/hexgrid_{size}.geojson')
    gdf_geometry["partition"] = gdf_geometry.index
    # load data from a certain lat/long range
    # must be replaced with database query
    data = pd.read_csv("../DATA/coords.csv")
    gdf_data = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.lon, data.lat))
    gdf_join = gpd.sjoin(gdf_data, gdf_geometry, how="inner", op="within")
    gdf_agg = gdf_join.groupby("partition").agg({"value": "sum"})
    redis.set(f"agg_{size}", gdf_agg.to_json())
    return {"message": "success"}