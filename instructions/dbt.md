## DBT

we will use dbt to perform transformation on our data in snowflake,
dbt (data build tool) is a transformation tools that sits on top of our data warehouse.

We don't actually require any real transformation on our data; this is only for practice.

### Setup

1. create a dbt ![user to connect to snowflake](../images/dbt_user.png)
2. 
3.    create a source.yml file in models
    singular test,
    I make sure I only have 20 rows also
    dbt seed for my image 
    change column name 
    extract latest value for today
    
    built the image EC2, we need to create a docker file