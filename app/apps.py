from django.apps import AppConfig
import MySQLdb
from django.conf import settings

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    # def ready(self):
    #     self.create_database_if_not_exists()

    # def create_database_if_not_exists(self):
    #     db_name = settings.DATABASES['default']['NAME']
    #     db_user = settings.DATABASES['default']['USER']
    #     db_password = settings.DATABASES['default']['PASSWORD']
    #     db_host = settings.DATABASES['default']['HOST']
    #     db_port = 3306  # Ensure this is an integer

    #     try:
    #         # Connect to MySQL server
    #         connection = MySQLdb.connect(
    #             host=db_host,
    #             user=db_user,
    #             passwd=db_password,
    #             port=db_port
    #         )
    #         cursor = connection.cursor()

    #         # Check if the database exists
    #         cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
    #         result = cursor.fetchone()

    #         if result:
    #             print(f"Database '{db_name}' already exists.")
    #         else:
    #             # Create the database if it doesn't exist
    #             cursor.execute(f"CREATE DATABASE {db_name}")
    #             print(f"Database '{db_name}' created successfully.")

    #         cursor.close()
    #         connection.close()

    #     except MySQLdb.Error as e:
    #         print(f"Error: {e}")
