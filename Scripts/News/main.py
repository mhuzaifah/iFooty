import psycopg2
import os
from dotenv import load_dotenv
from NewsDataScrape import getNews

# if os.path.exists('.env'):
load_dotenv()  # Only load .env file if it exists (local development)
db = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbPass = os.getenv("DB_PASS")


# Function to update PostgreSQL database's News Table
def updateNewsTable(df):
    
    # Connecting to database
    conn = psycopg2.connect(
        database=db,
        user=user,
        host=host,
        password=dbPass,
        port=port
    )
    curr = conn.cursor()
    
    # Get Max id from table
    maxIdQuery = "SELECT MAX(id) FROM pl_news"
    curr.execute(maxIdQuery)
    maxId = curr.fetchone()[0]
    id = 0 if maxId is None else maxId+1 
    
    columns = df.columns.tolist() # Get columns of table
    setClause = ', '.join(['id'] + columns) # Dynamically use column names to generate list for insert query
    valuesClausePlaceholder = ', '.join(['%s'] * (len(columns)+1))
    
    # Loop through the rows in the DataFrame and insert
    for _, row in df.iterrows():
        
        # Generate the INSERT query for each row
        insertQuery = f"""
        INSERT INTO pl_news ({setClause})
        VALUES ({valuesClausePlaceholder})
        """
                
        values = [id] + row.tolist() # Collect all values in list to dynamically add to query
        curr.execute(insertQuery, values) # Execute the query with the column values from the CSV
        
        id+=1 #increment id 
        
    conn.commit()
    curr.close()
    conn.close()

def main():

    """
    Main function to scrape data and update the PostgreSQL database.
    """

    try:
        newsDf = getNews()
        updateNewsTable(newsDf) 
        print("PL News DB updates successful!")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(1) # Exit with a non-zero status for GitHub Actions to register a failure
        
if __name__ == "__main__":
    main()