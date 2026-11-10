
import sqlite3
# for python database
import os
# interaction with operating system

class NetworkAnalyzer:
    # vvv initializes the network server and sets up database
    def __init__(self, db_name="network_metrics.db"):
        self.db_name = db_name
        # saves database file name
        self.init_db()


    # vvv creates table to hold the transfer metrics
    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        # connects to database file
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transfer_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT NOT NULL,
                filename TEXT NOT NULL,
                file_size_mb REAL NOT NULL,
                transfer_time_sec REAL NOT NULL,
                data_rate_mbps REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

# testing parts 1-3
if __name__ == "__main__":
    test_analyzer = NetworkAnalyzer()
    print("success")