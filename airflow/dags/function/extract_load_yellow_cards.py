import logging 
import os 
import requests
import json
import pandas as pd
import tempfile
from datetime import datetime
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def extract_yellow_cards(s3_conn_id,s3_bucket,api_key,yellow_cards_url,premier_league_season,league_id,data_interval_end) -> list:
    """
    download data from API key
    save data to a CSV file
    """
    headers = {"X-RapidAPI-Key" : api_key}
    params = {"season":premier_league_season, "league":league_id}
    
    try:
        response = requests.get(yellow_cards_url, headers=headers, params=params)
        data = response.json()
        logging.info(f'Raw API data: {data}')
        players = []
        for player in data['response']:
            player_data = player['player']
            statistics = player['statistics'][0]
            name = player_data['name']
            age = player_data['age']
            nationality = player_data['nationality']
            team =  statistics['team']['name']
            minutes_played = statistics['games']['minutes']
            total_yellow_cards = statistics['cards']['yellow']
            total_red_cards = statistics['cards']['red']
            photo = player_data['photo']
            logo = statistics['team']['logo']

            players.append({'name': name, 'age': age, 'nationality': nationality,
                            'team': team, 'minutes_played': minutes_played,
                            'total_yellow_cards': total_yellow_cards, 'total_red_cards': total_red_cards,
                            'photo': photo, 'logo': logo})

        df = pd.DataFrame(players)
        df['current_ts '] = datetime.now()
        logging.info('successfully downloaded data, cols:')
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_csv_file:
            df.to_csv(temp_csv_file, index=False, header=False)
            temp_csv_file_path = temp_csv_file.name
        expected_new_key = f'yellow_cards/{data_interval_end}/{data_interval_end}.csv'
        logging.info(f'Uploading file to S3 with key: {expected_new_key}')
        s3_hook = S3Hook(aws_conn_id=s3_conn_id)
        s3_hook.load_file(filename=temp_csv_file_path, bucket_name=s3_bucket, key=expected_new_key, replace=True)
        os.remove(temp_csv_file_path)
        return expected_new_key
        #return f's3://{s3_bucket}/{expected_new_key}'

    except Exception as e:
        logging.error(f'failed to load data into s3 {e}')
        raise e

