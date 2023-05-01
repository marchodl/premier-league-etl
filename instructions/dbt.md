## DBT

we will use dbt to perform transformation on our data in snowflake,
dbt (data build tool) is a transformation tools that sits on top of our data warehouse.

We don't actually require any real transformation on our data; this is only for practice.

### Setup

1. create a dbt user in snowflake ![user to connect to snowflake](../images/dbt_user.png)
2. ...
3.  create sources.yml ![source.yml](../images/dbt_sources.png)
4.  I am adding a basic singular test to check I will have erroneous data in my dashboard
5.  Also I am adding an additional sources of data, the staduim capacity 
`dbt seed`
6.  My transformation is basic such as extracting as join, change column name, extract latest value for ranking
7.   ... built the image EC2, we need to create a docker file