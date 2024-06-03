import pandas as pd
from sqlalchemy import create_engine, inspect

def document_database(db_url):
    # Create a database engine
    engine = create_engine(db_url)
    
    # Create an inspector to gather metadata
    inspector = inspect(engine)
    
    # List of all tables in the database
    tables = inspector.get_table_names()
    
    # DataFrame to store schema information
    schema_info = []

    for table in tables:
        columns = inspector.get_columns(table)
        for column in columns:
            schema_info.append({
                "Table": table,
                "Column": column['name'],
                "Type": column['type'],
                "Nullable": column['nullable'],
                "Default": column['default']
            })
    
    # Convert to DataFrame
    schema_df = pd.DataFrame(schema_info)
    
    # Save to CSV file
    schema_df.to_csv('systemintegration_db_schema.csv', index=False)
    
    return schema_df

# Example usage
db_url = 'mysql+pymysql://root:Monkey171195!@localhost:3306/systemintegration-db'
schema_df = document_database(db_url)
print("Database schema documented successfully!")
