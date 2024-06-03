import pandas as pd
from sqlalchemy import create_engine

def migrate_data(source_db_url, dest_db_url, table_name):
    try:
        # Create engines for source and destination databases
        source_engine = create_engine(source_db_url)
        dest_engine = create_engine(dest_db_url)
        
        print("Successfully created database engines.")
        
        # Read data from the source database
        with source_engine.connect() as source_conn:
            data = pd.read_sql_table(table_name, source_conn)
            print(f"Data from source table {table_name}:\n", data.head())
        
        # Write data to the destination database
        with dest_engine.connect() as dest_conn:
            data.to_sql(table_name, dest_conn, if_exists='append', index=False)
            print(f"Data successfully migrated to destination table {table_name}.")
            
            # Debugging: Read back the data to verify
            migrated_data = pd.read_sql_table(table_name, dest_conn)
            print(f"Data from destination table {table_name} after migration:\n", migrated_data.head())
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
source_db_url = 'mysql+pymysql://root:Monkey171195!@localhost:3306/systemintegration-db'
dest_db_url = 'postgresql+psycopg2://myuser:mypassword@localhost:5432/new_systemintegration-db'
table_name = 'users'  # Replace with the table you want to migrate

migrate_data(source_db_url, dest_db_url, table_name)
