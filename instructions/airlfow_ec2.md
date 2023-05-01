1. **create EC2 instance** we will use t2.meduim since it has the capacity to host a airflow instance
2. **install git to clone my repo**
3. **clone my repo** from [github](https://github.com/marchodl/premier-league-etl)
`git clone <link>`
4. go to docker file from my github
`docker build -t airflow:latest .`
`sudo docker run -u root -p 8080:8080 -v $(pwd):/opt/airflow airflow:latest standalone`
**enter variable** 
**enter conns**
5. run your dag