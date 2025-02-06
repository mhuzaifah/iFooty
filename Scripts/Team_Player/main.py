import psycopg2
import os
from dotenv import load_dotenv
from TeamPlayerDataScrape import getTeamAndPlayerData
import pandas as pd

load_dotenv()  # Only load .env file if it exists (local development)
db = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbPass = os.getenv("DB_PASS")

# Function to update PostgreSQL database's Team Table
def updateTeamTable(df):
    
    conn = psycopg2.connect(
        database=db,
        user=user,
        host=host,
        password=dbPass,
        port=port
    )
    curr = conn.cursor()
    
    # Clean the DataFrame by replacing NaN values with None
    df = df.replace({float('nan'): None})
    
    columns = df.columns.tolist()
    setClause = ', '.join([f"{col} = %s" for col in columns[1:]]) #Splice 1st elem since we don't want to include PK
    whereClause = "name = %s"
    
    # Loop through the rows in the DataFrame and update each row
    for _, row in df.iterrows():
        try:
            updateQuery = f"""
            UPDATE pl_teams
            SET {setClause}
            WHERE {whereClause}
            """
            
            # Convert the row to a list, handling None values
            values = [None if pd.isna(val) else val for val in row.iloc[1:].tolist()]
            values.append(row.iloc[0])  # Add the name (PK) value
            
            # Insert if the record doesn't exist
            insertQuery = f"""
            INSERT INTO pl_teams ({', '.join(columns)})
            SELECT %s
            WHERE NOT EXISTS (
                SELECT 1 FROM pl_teams 
                WHERE name = %s
            );
            """
            
            # First try to update
            curr.execute(updateQuery, values)
            
            # If no rows were updated, insert the new record
            if curr.rowcount == 0:
                all_values = [None if pd.isna(val) else val for val in row]
                curr.execute(insertQuery, 
                           [*all_values] + [row['name']])
            
            conn.commit()
            
        except Exception as e:
            print(f"Error processing team: {row['name']}")
            print(f"Error details: {str(e)}")
            conn.rollback()  # Rollback the transaction on error
            continue  # Continue with the next row
    
    curr.close()
    conn.close()


# Function to update PostgreSQL database's Player Table
def updatePlayerTable(df):
    
    conn = psycopg2.connect(
        database=db,
        user=user,
        host=host,
        password=dbPass,
        port=port
    )
    curr = conn.cursor()
    
    # Clean the DataFrame by replacing NaN values with None
    df = df.replace({float('nan'): None})
    
    columns = df.columns.tolist()
    
    # For updating, use only the non-key columns
    updateColumns = [col for col in columns if col not in ['name', 'team']]
    # Build the SET clause using updateColumns (not all columns)
    setClause = ', '.join([f"{col} = %s" for col in updateColumns])
    whereClause = "name = %s AND team = %s"
    
    # For insert, we still need all the columns
    insertColumns = columns
    placeholders = ', '.join(['%s'] * len(columns))
    
    # Loop through the rows in the DataFrame and update each row
    for _, row in df.iterrows():
                
        try:
            updateQuery = f"""
            UPDATE pl_players
            SET {setClause}
            WHERE {whereClause}
            """
            
            # Build update values for non-PK columns then add the PKs for the WHERE clause
            updateValues = [row[col] if not pd.isna(row[col]) else None for col in updateColumns]
            updateValues += [row['name'], row['team']]
            
            # Try to update first
            curr.execute(updateQuery, updateValues)
            
            # If no rows were updated, insert the new record
            if curr.rowcount == 0:
                insertQuery = f"""
                INSERT INTO pl_players ({', '.join(insertColumns)})
                SELECT {placeholders}
                WHERE NOT EXISTS (
                    SELECT 1 FROM pl_players 
                    WHERE name = %s AND team = %s
                );
                """
                
                # Build insert values for all columns, then add PK values for the subquery
                insertValues = [row[col] if not pd.isna(row[col]) else None for col in insertColumns]
                insertValues += [row['name'], row['team']]
                
                curr.execute(insertQuery, insertValues)
            
            conn.commit()
            
        except Exception as e:
            print(f"Error processing row: {row['name']} - {row['team']}")
            print(f"Error details: {str(e)}")
            conn.rollback()  # Rollback the transaction on error
            continue  # Continue with the next row
    
    curr.close()
    conn.close()



def main():
    """
    Main function to scrape data and update the PostgreSQL database.
    """
    try:
        print("Starting data collection...")
        # playersDf, teamsDf = getTeamAndPlayerData()
        
        #For Testing
        playersDf = pd.read_csv('pl_players.csv')
        teamsDf = pd.read_csv('pl_teams.csv')
        
        print("\nValidating DataFrames...")
        print("Players DataFrame shape:", playersDf.shape if playersDf is not None else "None")
        print("Teams DataFrame shape:", teamsDf.shape if teamsDf is not None else "None")
        
        print("\nFinal DataFrame validation:")
        print("Players DataFrame shape:", playersDf.shape if playersDf is not None else "None")
        print("Teams DataFrame shape:", teamsDf.shape if teamsDf is not None else "None")
        print("\nPlayers DataFrame columns:", playersDf.columns.tolist() if playersDf is not None else "None")
        print("Teams DataFrame columns:", teamsDf.columns.tolist() if teamsDf is not None else "None")
        
        print("\nUpdating Players DB...")
        updatePlayerTable(playersDf)
        print("\nUpdating Teams DB...")
        updateTeamTable(teamsDf)
            
        print("PL Team and Player DB updates successful!")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        exit(1)
        
if __name__ == "__main__":
    main()