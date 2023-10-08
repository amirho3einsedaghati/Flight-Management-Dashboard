from sqlalchemy import create_engine
import pandas as pd
import os


flights = pd.read_csv(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'flight_data.csv'))   

X_test = pd.read_csv(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'X_test.csv')) 
    
X = pd.read_csv(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'X.csv'))     

def create_table(df, table_name):
    username = 'Enter your username'
    password = 'Enter your password'
    server = 'localhost,1433'
    database = 'Enter your database name'
    driver ='ODBC Driver 18 for SQL Server'

    connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}"
    
    connect_args = {
        "TrustServerCertificate": "yes"
        }

    engine = create_engine(
        connection_string,
        connect_args = connect_args,
        echo=False
    )

    df.to_sql(table_name, engine, if_exists='replace')

create_table(flights, 'flights')
create_table(X_test, 'X_test')
create_table(X, 'X')
