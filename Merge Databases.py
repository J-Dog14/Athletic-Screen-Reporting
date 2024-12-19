import sqlite3
import os

# Paths and filenames
input_folder = "D:/Athletic Screen 2.0/Output Files/"
input_databases = ["Athletic_Screen_College_data.db", "Athletic_Screen_HS_data.db", "Athletic_Screen_Pro_data.db"]
output_database = "Athletic_Screen_All_data.db"
table_names = ["CMJ", "DJ", "SLV", "NMT"]

# Create a connection to the output database
output_conn = sqlite3.connect(os.path.join(input_folder, output_database))
output_cursor = output_conn.cursor()

# Iterate over each input database
for db_name in input_databases:
    db_path = os.path.join(input_folder, db_name)
    with sqlite3.connect(db_path) as input_conn:
        input_cursor = input_conn.cursor()

        # For each table in the list, copy data to the output database
        for table in table_names:
            # Create table in the output database if it doesn't exist
            input_cursor.execute(f"PRAGMA table_info({table})")
            columns = input_cursor.fetchall()
            column_defs = ", ".join([f"{col[1]} {col[2]}" for col in columns])  # e.g., "col_name col_type"
            output_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({column_defs})")

            # Insert data from input database to the output database
            input_cursor.execute(f"SELECT * FROM {table}")
            rows = input_cursor.fetchall()
            placeholders = ", ".join(["?" for _ in columns])
            output_cursor.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)
            output_conn.commit()

# Close the output connection
output_conn.close()

print("Databases have been successfully merged into Athletic_Screen_All_data.db.")
