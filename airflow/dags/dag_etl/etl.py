import datetime
import pendulum
from function.extract_load_ranking import extract_ranking
from function.extract_load_yellow_cards import extract_yellow_cards
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.transfers.s3_to_snowflake import S3ToSnowflakeOperator
from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator


with DAG(
        dag_id='football-pipeline',
        schedule_interval='0 0 * * *',
        description='Perform end to end using airflow',
        start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
        catchup=False,
        dagrun_timeout=datetime.timedelta(minutes=5),
        tags=['football-pipeline'],
) as dag:
    aws_conn_id = "aws_conn"
    s3_bucket =  "{{ var.value.S3_BUCKET }}"  
    football_api_key = "{{ var.value.FOOTBALL_API_KEY }}"
    data_interval_end = "{{ data_interval_end.format('YYYYMMDDHHmmss') }}" 
    
    standing_url = "{{ var.value.STANDING_URL }}"
    yellow_cards_url = "{{ var.value.YELLOW_CARDS_URL }}"
    premier_league_season = "{{ var.value.PREMIER_LEAGUE_SEASON }}"
    league_id = "{{ var.value.LEAGUE_ID }}"
    snowflake_conn = "snowflake_conn"

    RANKING_SNOWFLAKE_TABLE = "RANKING"
    YELLOW_CARDS_SNOWFLAKE_TABLE = "YELLOW_CARDS"
    SNOWFLAKE_STAGE = "S3_FOOTBALL_STAGE"
    SNOWFLAKE_SCHEMA = "PUBLIC"
    SNOWFLAKE_ROLE = "ACCOUNTADMIN"

    extract_ranking_task = PythonOperator(
    task_id="extract_ranking",
    python_callable=extract_ranking,
    op_kwargs={
        "s3_conn_id": aws_conn_id,
        "s3_bucket": s3_bucket,
        "api_key": football_api_key,
        "data_interval_end": data_interval_end,
        "standing_url": standing_url,
        "premier_league_season": premier_league_season,  
        "league_id": league_id,
    }
)
    extract_yellow_cards_task = PythonOperator(
    task_id="extract_yellow_cards",
    python_callable=extract_yellow_cards,
    op_kwargs={
        "s3_conn_id": aws_conn_id,
        "s3_bucket": s3_bucket,
        "api_key": football_api_key,
        "data_interval_end": data_interval_end,
        "yellow_cards_url": yellow_cards_url,
        "premier_league_season": premier_league_season,  
        "league_id": league_id,
    }
)

    copy_ranking_table = S3ToSnowflakeOperator(
    task_id="copy_ranking_table",
    snowflake_conn_id=snowflake_conn,
    s3_keys= ["{{ ti.xcom_pull(task_ids='extract_ranking') }}"],
    table=RANKING_SNOWFLAKE_TABLE,
    stage=SNOWFLAKE_STAGE,
    schema= SNOWFLAKE_SCHEMA,
    role = SNOWFLAKE_ROLE,
    file_format="(type = 'CSV', field_delimiter = ',')",
    pattern=".*[.]csv",
) 
 
    copy_yellow_cards_table = S3ToSnowflakeOperator(
    task_id="copy_yellow_cards_table",
    snowflake_conn_id=snowflake_conn,
    s3_keys= ["{{ ti.xcom_pull(task_ids='extract_yellow_cards') }}"],
    table=YELLOW_CARDS_SNOWFLAKE_TABLE,
    schema= SNOWFLAKE_SCHEMA,
    role = SNOWFLAKE_ROLE,
    stage = SNOWFLAKE_STAGE,
    file_format="(type = 'CSV', field_delimiter = ',')", 
    pattern=".*[.]csv",
)
    
    dbt_sync = EcsRunTaskOperator(
        task_id="dbt_transform",
        aws_conn_id= aws_conn_id,
        cluster = "premierleague2",
        launch_type = "EC2",
        task_definition = "premierleague2",
        region = "us-east-1",
        overrides = {},
    )
    
    


    #[extract_ranking_task, extract_yellow_cards_task] >> [copy_ranking_table, copy_yellow_cards_table]
    extract_ranking_task >> extract_yellow_cards_task >> [copy_ranking_table, copy_yellow_cards_table] >> dbt_sync
    
