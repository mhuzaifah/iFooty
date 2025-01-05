import psycopg2
import os
from TeamPlayerDataScrape import getTeamAndPlayerData

# Function to update PostgreSQL database with input dataframe
def updateDB(df, tableName, pk):
    
    # Connecting to database
    db = os.environ['DB_NAME']
    user = os.environ['DB_USER']
    host = os.environ['DB_HOST']
    port = os.environ['DB_PORT']
    dbPass = os.environ['DB_PASSWORD']
    conn = psycopg2.connect(database = db, 
                            user = user, 
                            host = host,
                            password = dbPass,
                            port = port)
    curr = conn.cursor()  
    
    columns = df.columns.tolist()  
    setClause = ', '.join([f"{col} = %s" for col in columns[1:]]) #Splice 1st elem since we don't want to include PK
    
    # Loop through the rows in the DataFrame and update each row based on the primary key
    for _, row in df.iterrows():
        
        # Generate the UPDATE query for each row
        updateQuery = f"""
        UPDATE {tableName}
        SET {setClause}
        WHERE {pk} = %s
        """
        
        values = row.iloc[1:].tolist() + [row.iloc[0]] # Collect all values in list to dynamically add to query
        curr.execute(updateQuery, values) # Execute the query with the column values from the CSV
    conn.commit()
    
    curr.close()
    conn.close()


def main(request):

    """
    Main function to scrape data and update the PostgreSQL database.
    """

    try:
        playersDf, teamsDf = getTeamAndPlayerData()
        updateDB(playersDf, 'pl_players', 'id') 
        updateDB(teamsDf, 'pl_teams', 'name') 
        print("PL Team and Player DB updates successful!")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(1) # Exit with a non-zero status for GitHub Actions to register a failure
        
if __name__ == "__main__":
    main()