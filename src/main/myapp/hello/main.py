import mysql.connector

from myapp.utilities.config import load_config

def connect(**connection_parameters):
    return mysql.connector.connect(**connection_parameters)

def print_columns(connection):
    sql = """
        SELECT
            *
        FROM
            information_schema.COLUMNS
        ORDER BY
            ORDINAL_POSITION
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    for row in cursor.fetchall():
        print(row)

def main():
    database_config = load_config("config/database.yml").development
    connection = connect(**database_config)
    print_columns(connection)
    connection.close()

if __name__ == "__main__":
    main()

