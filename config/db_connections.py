import psycopg2
from config.data import Data

class DatabaseHelper:
    @staticmethod
    def get_db_connection(db_name):
        db_config = {
            'Dev': {
                'host': Data.bd_host,
                'database': 'dev_base',
                'user': Data.bd_login,
                'password': Data.bd_pwd,
                'port': '5433'
            },
            'Voice': {
                'host': Data.bd_st_vs_host,
                'database': 'voice_base',
                'user': Data.bd_st_vs_login,
                'password': Data.bd_st_vs_pwd,
                'port': '5433'
            },
            'Steos': {
                'host': Data.bd_st_vs_host,
                'database': 'steos_id',
                'user': Data.bd_st_vs_login,
                'password': Data.bd_st_vs_pwd,
                'port': '5433'
            }
        }
        return psycopg2.connect(**db_config[db_name])

