from database.database_functions import Database


class Resident:
    def __init__(self, name, id_number, score=0, monthly=False, weekly=False, daily=False):
        self.name = name
        self.id_number = id_number
        self.score = score
        self.monthly = monthly
        self.weekly = weekly
        self.daily = daily

    def create_database_entry(self):
        """
        creates a database entry for a resident with all scores set to default

        :return: None
        """
        res_name = self.name
        res_id = self.id_number
        score = self.score
        monthly = self.monthly
        weekly = self.weekly
        daily = self.daily
        create_new_user_row = """INSERT OR IGNORE INTO residents (id_number, name, score, monthly, weekly, daily) 
                                            values (?, ?, ?, ?, ?, ?)"""
        Database.cursor.execute(create_new_user_row, (res_id, res_name, score, monthly, weekly, daily))
        Database.res_db_conn.commit()

        print_new_resident = """SELECT id_number, name, score, monthly, weekly, daily
                                        FROM residents
                                        WHERE id_number == (?)"""
        Database.cursor.execute(print_new_resident, (res_id,))
        new_res_row = Database.cursor.fetchone()
        print("New Residents Added", new_res_row)
