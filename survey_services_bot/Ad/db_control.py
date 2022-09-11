import mysql.connector
from Ad.config import dbconfig


class DBControl:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def create_connection(self):
        self.connection = mysql.connector.connect(**dbconfig)
        self.cursor = self.connection.cursor()

    def send_data_to_db(self, next_value: str, current_header: str) -> None:
        is_header = next_value == current_header
        if is_header:
            sql = """insert into AvitoServices.service_groups (service_group_name) values (%s);"""
            self.cursor.execute(sql, (current_header,))
            self.connection.commit()
        else:
            sql = """insert into AvitoServices.services 
                  (service_name, group_id)
                  values (%s,
                  (select id from service_groups where service_group_name=%s));"""
            self.cursor.execute(sql, (next_value, current_header))
            self.connection.commit()

    def clean_up_table(self, table_name):
        # Unprotected call because of the CMYSQLCursor feature (inserts strings with '' quotes)
        sql = f"""
            delete from {table_name};
        """
        # execute has an option "multi" (:bool) to run more than 1 command per time
        self.cursor.execute(sql)
        self.connection.commit()
        # Repeated the same instructions because of incomprehensibility in SQL
        sql = f"""
            alter table {table_name} auto_increment=1;
        """
        self.cursor.execute(sql)
        self.connection.commit()

    def commit_and_close_connection(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
