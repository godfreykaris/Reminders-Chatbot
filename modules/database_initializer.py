import json
import os
import psycopg2
import logging

class DatabaseInitializer:
    def __init__(self, credentials_file_path=None, credentials=None):
            self.credentials_file_path = credentials_file_path
            self.credentials = credentials
        
    def get_credentials(self):
        with open(self.credentials_file_path, "r") as config_file:
            config = json.load(config_file)
        return config

    def get_database_connection(self):
        if self.credentials:
            credentials = self.credentials
        else:
            credentials = self.get_credentials()
    
        conn = psycopg2.connect(
            host=credentials["db_host"],
            port=credentials["db_port"],
            database=credentials["db_name"],
            user=credentials["db_user"],
            password=credentials["db_password"]
        )

        
        return conn
