1. **Create EC2 instance** we will use t2.meduim since it has the capacity to host a airflow instance
2. **Install git** on the Ec2 instance to clone my repo
`sudo yum install git -y`
3. **clone my repo** from [github](https://github.com/marchodl/premier-league-etl)
`git clone <link>`
4. **Build and run** the Docker container using the Dockerfile from your GitHub repository
`cd <repository_name>`
`docker build -t airflow:latest .`
`sudo docker run -u root -p 8080:8080 -v $(pwd):/opt/airflow airflow:latest standalone`
5. **setup airflow**
enter variable, connections
6. Run your DAG from airflow UI