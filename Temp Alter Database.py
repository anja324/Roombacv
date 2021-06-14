from database.database_functions import *

connect_andor_create_resident_database()

Database.cursor.execute("ALTER TABLE residents ADD COLUMN raincoat INTEGER")
Database.res_db_conn.commit()

Database.cursor.execute("ALTER TABLE residents ADD COLUMN raincoat_die_roll")
Database.res_db_conn.commit()
