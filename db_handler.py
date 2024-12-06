import oracledb
from datetime import datetime
import os

class DatabaseHandler:
    def __init__(self, username, password, dsn, wallet_location, wallet_password):
        self.username = username
        self.password = password
        self.dsn = dsn
        self.wallet_location = wallet_location
        self.wallet_password = wallet_password
        self.connection = None
        
    def connect(self):
        try:
            # Initialize Oracle Client library for thick mode with specific config directory
            oracledb.init_oracle_client(config_dir=self.wallet_location, lib_dir=os.getenv("ORACLE_CLIENT_PATH", "C:\\oracle\\instantclient"))
            
            # Configure the wallet location
            self.connection = oracledb.connect(
                user=self.username,
                password=self.password,
                dsn=self.dsn,
                wallet_location=self.wallet_location,
                wallet_password=self.wallet_password
            )
            print("Successfully connected to Oracle Database using thick mode")
            self._create_table()
        except Exception as e:
            print(f"Error connecting to database: {str(e)}")
            raise

    def _table_exists(self, table_name):
        check_sql = """
        SELECT COUNT(*) 
        FROM user_tables 
        WHERE table_name = :1
        """
        with self.connection.cursor() as cursor:
            cursor.execute(check_sql, [table_name.upper()])
            count = cursor.fetchone()[0]
            return count > 0

    def _create_table(self):
        if not self._table_exists('repository_summaries'):
            create_table_sql = """
            CREATE TABLE repository_summaries (
                id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                summary_text CLOB,
                created_date DATE,
                daily_position NUMBER,
                file_path VARCHAR2(255)
            )
            """
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(create_table_sql)
                    self.connection.commit()
                print("Table repository_summaries created successfully")
            except Exception as e:
                print(f"Error creating table: {str(e)}")
                raise

    def insert_summary(self, summary_text: str, daily_position: int, file_path: str):
        print(f"\nInserting summary into database:")
        print(f"- Position: {daily_position}")
        print(f"- File: {file_path}")
        print(f"- Summary length: {len(summary_text)} characters")
        
        insert_sql = """
        INSERT INTO repository_summaries 
        (summary_text, created_date, daily_position, file_path)
        VALUES (:1, :2, :3, :4)
        """
        try:
            current_time = datetime.now()
            with self.connection.cursor() as cursor:
                cursor.execute(insert_sql, [
                    summary_text,
                    current_time,
                    daily_position,
                    file_path
                ])
                self.connection.commit()
                
                # Verify the insertion by fetching the latest record
                verify_sql = """
                SELECT id, daily_position, created_date, file_path 
                FROM repository_summaries 
                WHERE daily_position = :1 
                AND created_date = :2
                """
                cursor.execute(verify_sql, [daily_position, current_time])
                result = cursor.fetchone()
                
                if result:
                    print(f"✓ Successfully inserted summary:")
                    print(f"  - Database ID: {result[0]}")
                    print(f"  - Position: {result[1]}")
                    print(f"  - Timestamp: {result[2]}")
                    print(f"  - File: {result[3]}")
                else:
                    print("! Warning: Insertion succeeded but verification failed")
                    
        except Exception as e:
            print(f"✗ Error inserting summary: {str(e)}")
            raise

    def close(self):
        if self.connection:
            self.connection.close()
            print("\nDatabase connection closed successfully") 