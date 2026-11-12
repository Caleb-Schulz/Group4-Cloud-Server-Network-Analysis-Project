
# for python database
import sqlite3
# interaction with operating system
import os

class NetworkAnalyzer:
    # vvv initializes the network server and sets up database
    def __init__(self, db_name="network_metrics.db"):
        # saves database file name
        self.db_name = db_name
        self.init_db()


    # vvv creates table to hold the transfer metrics
    def init_db(self):
        # connects to database file
        conn = sqlite3.connect(self.db_name)
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

    # vvv saves metrics in database
    def save_transfer_metrics(self, operation, filename, file_size_bytes, transfer_time_sec):
        # b -> Mb
        file_size_mb = file_size_bytes / (1024 * 1024)

        # find data rate
        if transfer_time_sec > 0:
            data_rate_mbps = file_size_mb / transfer_time_sec
        else:
            data_rate_mbps = file_size_mb
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # adds row of data into table using placeholders
        cursor.execute('''
            INSERT INTO transfer_metrics (operation, filename, file_size_mb, transfer_time_sec, data_rate_mbps)
            VALUES (?, ?, ?, ?, ?)
            ''', (operation, filename, file_size_mb, transfer_time_sec, data_rate_mbps))
        conn.commit()
        conn.close()

        # print metrics (for immediate visual feedback)
        print(f"[NetworkAnalyzer] Operation: {operation} | File: {filename} | Size {file_size_mb:.2f} Mb | Time: {transfer_time_sec:.4f}s | Rate: {data_rate_mbps:.2f} Mb/s")

    # gets stored transfer metrics from database for analysis
    def get_metrics(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.excute('''
            SELECT * FROM transfer_metrics
        ''')
        rows = cursor.fetchall()
        conn.close()
        return rows


'''
# testing parts 1-3
if __name__ == "__main__":
    test_analyzer = NetworkAnalyzer()
    print("success")
'''
