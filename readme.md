## Premier League ETL Pipeline

In this project I will extract data provided from [rapid-API](https://rapidapi.com/hub) for the premier league (highest level of the English football competition).
The goal is to generate insightful reports based on the Premier League data to better understand the dynamics of the league.

### Motivation
This project was inspired by an interest in data engineering and the latest concept used in the field, such as idempotence. It also an opportunity to develop skills and gain experience with a range of tools, such as Snowflake for creating infrastructure and deploying Airflow on an EC2 instances. The project is more complex than required, utilizing dbt, Snowflake, Airflow, Docker, AWS, and CI.

### Architecture 

![Image description](images/architecture_plot_initial.png)
1. Extract data using the [football API](https://rapidapi.com/api-sports/api/API-FOOTBALL)
2. Load into [AWS S3](https://aws.amazon.com/s3/)
3. Copy into [snowflake](https://www.snowflake.com/en/)
4. Transform using [dbt](https://www.getdbt.com/)
5. Create [docker](https://www.docker.com/) image and deploy it on AWS [ECS](https://aws.amazon.com/ecs/)
6. Create [PowerBI](https://powerbi.microsoft.com/en-gb/) Dashboard
7. Orchestrate with [Airflow](https://airflow.apache.org/) on [EC2](https://aws.amazon.com/ec2/)

## output
![Final dashboard](images/output.png)

### setup:

Follow below steps to setup pipeline. I've tried to explain steps where I can. 

All the services I am using are on an AWS Free Tier account, and I am also utilizing Snowflake's 30-day trial period. The only expenses I incurred were for running Airflow on an EC2 t2.medium instance ($0.04 per hour) and storing my image on ECR ($0.10 per month). Additional costs may arise if you maintain your infrastructure for an extended period of time.

1. [Get airflow locally](instructions/airflow_local.md) 
2. [Rapid-API configuration](instructions/Rapid_API_configuration.md)
3. [Set up your AWS account](/instructions/AWS_account.md)
4. [S3 bucket](/instructions/S3_bucket.md)
5. [Snowflake configuration](/instructions/snowflake.md)
6. [Dbt](/instructions/dbt.md)
7. [Run airflow on EC2](/instructions/airlfow_ec2.md)
8. [BI tool dashboard](/instructions/BI_tool_dashboard.md)
9. CI
10. [Improvements](/instructions/improvement.md)
