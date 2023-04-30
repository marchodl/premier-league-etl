to start your project,
1. use the docker image in airflow/Dockerfile
2. build this  image. 
`docker build -t <image_name> .`
3. Start the Docker container:
`docker run -d --name my_airflow_container my-airflow:latest`


add ![variable](../images/variable_airflow.png) and ![Image description](../images/airflow_snowflake_conn.png) using the UI.

start the extraction in python.
define your ![dag interval](../images/dag_airflow.png)
