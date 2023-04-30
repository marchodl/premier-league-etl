import logging 
import os 
import requests
import json
import pandas as pd
import tempfile
from datetime import datetime
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def extract_ranking(s3_conn_id,api_key,s3_bucket,standing_url,premier_league_season,league_id,data_interval_end)->list:
    """
    downlaod data from API key 
    push data to S3 bucket
    """
    headers = {"X-RapidAPI-Key" : api_key}
    params = {"season":premier_league_season, "league":league_id}
    try:
        logging.info('extracting data')
        response = requests.get(standing_url, headers=headers, params=params)
        data = json.loads(response.content)
        logging.info(f'Raw API data: {data}')
        ranking = []
        for team in data['response'][0]['league']['standings'][0]:
            name = team['team']['name']
            played = team['all']['played']
            position = team['rank']
            points = team['points']
            goalDiff = team['goalsDiff']
            ranking.append({'name': name,'position': position, 'played': played , 'points': points, 'goalDiff' : goalDiff})
        df = pd.DataFrame(ranking)
        df['current_ts '] = datetime.now()
        logging.info('successfully downloaded data, cols:')
        # load result back to S3
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_csv_file:
            df.to_csv(temp_csv_file, index=False, header=False)
            temp_csv_file_path = temp_csv_file.name

        expected_new_key = f'ranking/{data_interval_end}/{data_interval_end}.csv'
        logging.info(f'Uploading file to S3 with key: {expected_new_key}')
        s3_hook = S3Hook(aws_conn_id=s3_conn_id)
        s3_hook.load_file(filename=temp_csv_file_path, bucket_name=s3_bucket, key=expected_new_key, replace=True)
        os.remove(temp_csv_file_path)
        return expected_new_key
        #return f's3://{s3_bucket}/{expected_new_key}'
    except Exception as e:
            logging.error(f'failed to load data into s3 {e}')
            raise e