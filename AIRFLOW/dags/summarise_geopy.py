import os
from airflow import DAG
from datetime import datetime
from airflow.operators.python_operator import PythonOperator,BranchPythonOperator


import pandas as pd
from glob import glob
import json
import geopandas as gpd
from datetime import datetime, timedelta



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
}
def load_data(**kwargs):
    for k, v in kwargs.items():
        print('keyword argument: {} = {}'.format(k, v))

    
    input_path = kwargs.get('data_path')
    output_path = kwargs.get('output_path')
    if input_path is None:
        input_path =  "/app/data/lake/mockdata/coords.csv"
    if output_path is None:
        output_path = "/app/data/warehouse/"

    coords_df =pd.read_csv(input_path)
    
    result = coords_df.describe()
    result.to_csv(output_path+"coords_summary.csv")


    ti = kwargs['ti']
    ti.xcom_push(key='dataframe', value=coords_df.to_json())
    
def load_geojson(**kwargs):
    input_path = kwargs.get('data_path')
    output_path = kwargs.get('output_path')

    if input_path is None:
        input_path =  "/app/data/lake/geojson/"
    if output_path is None:
        output_path = "/app/data/warehouse/"

    hexmaps_paths = glob(input_path+"*.geojson")

    ti = kwargs['ti']
    ti.xcom_push(key='hexmaps_paths', value=hexmaps_paths)

def transform(**kwargs):

    input_path = kwargs.get('data_path')
    output_path = kwargs.get('output_path')
    if input_path is None:
        input_path =  "/app/data/lake/mockdata/coords.csv"
    if output_path is None:
        output_path = "/app/data/warehouse/"


    ti = kwargs['ti']
    coords_df = ti.xcom_pull(key='dataframe', task_ids='run_etl')
    coords_df = pd.read_json(coords_df)

    hexmaps_paths = ti.xcom_pull(key='hexmaps_paths', task_ids='load_geojson')
    for hexmap_path in hexmaps_paths:
    
        gdf_geometry = gpd.read_file(hexmap_path)
        gdf_geometry["partition"] = gdf_geometry.index


        gdf_data = gpd.GeoDataFrame(coords_df, geometry=gpd.points_from_xy(coords_df.lon, coords_df.lat))

        gdf_join = gpd.sjoin(gdf_data, gdf_geometry, how="inner", op="within")
        gdf_agg = gdf_join.groupby("partition").agg({"value": "sum"})

        gdf_geometry.set_index("partition", inplace=True)
        gdf_geometry = gdf_geometry.join(gdf_agg)
        gdf_geometry.fillna(0, inplace=True)
        gdf_geometry = gdf_geometry[gdf_geometry["value"] > 0]

        gdf_geometry.to_file(output_path+os.path.basename(hexmap_path), driver="GeoJSON")



with DAG('agg_hexmap', default_args=default_args, schedule_interval=timedelta(minutes=15)) as dag:
    
    load_data_task = PythonOperator(
        task_id='run_etl',
        python_callable=load_data,
        op_kwargs={
            'data_path': '/app/data/lake/mockdata/coords.csv',
            'output_path': '/app/data/warehouse/'
        }
    )

    load_geojson_task = PythonOperator(
        task_id='load_geojson',
        python_callable=load_geojson,
        op_kwargs={
            'data_path': '/app/data/lake/geojson/',
            'output_path': '/app/data/warehouse/'
        }
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
        op_kwargs={
            'data_path': '/app/data/lake/mockdata/coords.csv',
            'output_path': '/app/data/warehouse/'
        }
    )

    [load_data_task, load_geojson_task] >> transform_task

