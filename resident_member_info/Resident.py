from database.database_functions import Database
from utilities.json_tokens import JsonConfig


class Resident:
    def __init__(self, name, id_number, score=0, monthly=False, weekly=False, daily=False, count_number=0):
        self.name = name
        self.id_number = id_number
        self.score = score
        self.monthly = monthly
        self.weekly = weekly
        self.daily = daily
        self.count_number = count_number

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
        count_number = self.count_number
        create_new_user_row = """INSERT OR IGNORE INTO residents (id_number, name, score, monthly, weekly, daily, count_number) 
                                            values (?, ?, ?, ?, ?, ?, ?)"""
        Database.cursor.execute(create_new_user_row, (res_id, res_name, score, monthly, weekly, daily, count_number))
        Database.res_db_conn.commit()

        print_new_resident = """SELECT id_number, name, score, monthly, weekly, daily, count_number
                                        FROM residents
                                        WHERE id_number == (?)"""
        Database.cursor.execute(print_new_resident, (res_id,))
        new_res_row = Database.cursor.fetchone()
        print("New Residents Added", new_res_row)


async def accept_new_resident(member, resident_roster):
    """
    Greets a new member of the server, and adds them to the database

    :param resident_roster: a list of all resident-objects
    :param member: the discord provided member object
    :return: None
    """

    #   Greets member
    await JsonConfig.channel.audits.send(f"New User: {member}!")
    await JsonConfig.channel.lounge.send(f"You have arrived at Anja's House!  Welcome to the family <3.  "
                                          f"Please mind the rules, found in {JsonConfig.channel.rules.mention}."
                                          f" The following roles are available to be given by a mod/admin:"
                                          f" Fuel Rat, RPGs(usually tabletops), Warframe, Star Citizen, Book Club(we try every year or so)")

    #   Adds to DB
    new_res = Resident(member.name, member.id)
    resident_roster.append(new_res)
    new_res.create_database_entry()