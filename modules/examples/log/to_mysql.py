import pymysql
import os
import json
from core.service.base_service import BaseServicePlugin
from dotenv import load_dotenv
import pandas as pd


class LogMySQLService(BaseServicePlugin):
    def __init__(self, name, config=None, log_queue=None, mode='live'):
        super().__init__(name, config=config, log_queue=log_queue, mode=mode)
        load_dotenv()
        self.connection = None
        self.db_host = os.environ.get("DB_HOST", "localhost")
        self.db_user = os.environ.get("DB_USER", "root")
        self.db_password = os.environ.get("DB_PASSWORD", "")
        self.db_name = os.environ.get("DB_NAME", "tempusone")
        self.db_port = int(os.environ.get("DB_PORT", 3306))

    def setup(self):
        try:
            self.connection = pymysql.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name,
                port=self.db_port,
                cursorclass=pymysql.cursors.DictCursor
            )
            self._create_table_syxtrade_logs_if_not_exists()
        except Exception as e:
            print(f"[ERROR] Failed to connect to MySQL: {e}")

    def _create_table_syxtrade_logs_if_not_exists(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS syxtrade_logs (
            log_id VARCHAR(255) PRIMARY KEY,
            status int,
            log_data text
        )
        """
        with self.connection.cursor() as cursor:
            cursor.execute(create_table_sql)
        self.connection.commit()

    def run(self, data=None):
        logs = self.log_queue.get_all()
        if not logs or not self.connection:
            return

        log_insert_sql = """
        INSERT INTO syxtrade_logs (log_id, status, log_data)
        VALUES (%s, %s, %s)
        """
        log_data_to_insert = []
        for log in logs:
            log_content = log['log_data']  # The dictionary
            log_json_str = json.dumps(log_content, ensure_ascii=False) # The string for storage
            log_data_to_insert.append((
                log['ID'],
                log['status'],
                log_json_str
            ))
        try:
            with self.connection.cursor() as cursor:
                cursor.executemany(log_insert_sql, log_data_to_insert)
            self.connection.commit()
        except Exception as e:
            print(f"[ERROR] Failed to insert logs into MySQL: {e}")
