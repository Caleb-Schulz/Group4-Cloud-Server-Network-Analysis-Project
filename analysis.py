
import sqlite3
import os

class NetworkAnalyzer:
    def __init__(self, db_name="network_metrics.db"):
        self.db_name = db_name
        self.init.db()

    