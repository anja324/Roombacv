import sqlite3


class Database:
    cursor = None
    res_db_conn = None


def connect_andor_create_resident_database():
    """
    connects to the database if one exists, creates a database and connects if one does not

    :return: cursor
    """

    #   creates a connection with the database
    res_db_conn = sqlite3.connect("resident_member_info/resident_database.db")

    #   creates a cursor object for accessing and altering pieces of the database
    cursor = res_db_conn.cursor()

    #   creates a database for residents if one does not already exist
    cursor.execute("""CREATE TABLE IF NOT EXISTS residents 
                        (id_number INTEGER NOT NULL PRIMARY KEY, name TEXT, score INTEGER, monthly INTEGER, weekly INTEGER, daily INTEGER, raincoat INTEGER, raincoat_die_roll INTEGER)""")
    res_db_conn.commit()

    Database.cursor = cursor
    Database.res_db_conn = res_db_conn

    return res_db_conn, cursor


def population_of_resident_database(resident_roster):
    """
    populates the database with initial residents and data OR populates any *new* residents and data since bot last connected

    :param resident_roster: list of all resident objects
    :return: None
    """

    for resident in resident_roster:
        resident.create_database_entry()


async def score_query(user_id):
    """
    Retrieves the score of the requested user
    :param user_id: the id of the requested user
    :return: score
    """
    retrieve_score = """SELECT score
                        FROM residents
                        WHERE id_number == (?)"""

    Database.cursor.execute(retrieve_score, (user_id,))
    score, = Database.cursor.fetchone()
    return score
    #   TODO Make timestamp function


async def add_to_score(user_id, amount_to_add):
    """
    adds the designated amount to the user's score
    :param user_id: the id of the user whose information will change
    :param amount_to_add: the number of points to be added
    :return:
    """
    change_it = "UPDATE residents SET score = score + ? WHERE id_number = ?"
    Database.cursor.execute(change_it, (amount_to_add, user_id))
    Database.res_db_conn.commit()


async def deduct_from_score(user_id, amount_to_deduct):
    """
    deducts the designated amount from the users score
    :param user_id: the id of the user whose information will change
    :param amount_to_deduct: the number of points to be added
    :return:
    """
    change_it = "UPDATE residents SET score = score - ? WHERE id_number = ?"
    Database.cursor.execute(change_it, (amount_to_deduct, user_id))
    Database.res_db_conn.commit()


async def retrieve_leaderboard():
    """
    gets name, score from the database

    :return:list of tuples (id, score)
    """

    retrieve_all_scores = "SELECT score, name FROM residents ORDER BY score DESC"
    Database.cursor.execute(retrieve_all_scores)
    score_name_list = Database.cursor.fetchall()
    return score_name_list


async def retrieve_raincoat(user_id):

    retrieve_raincoat_status = "SELECT raincoat FROM residents WHERE id_number == (?)"
    Database.cursor.execute(retrieve_raincoat_status, (user_id,))
    raincoat_status, = Database.cursor.fetchone()
    return raincoat_status


async def raincoat_db_add(user_id):

    change_it = "UPDATE residents SET raincoat = 1 WHERE id_number = ?"
    Database.cursor.execute(change_it, (user_id,))
    die_roll_set = "UPDATE residents SET raincoat_die_roll = 10"
    Database.cursor.execute(die_roll_set)
    Database.res_db_conn.commit()


async def retrieve_raincoat_die_roll(user_id):

    retrieve_die_roll = "SELECT raincoat_die_roll FROM residents WHERE id_number == (?)"
    Database.cursor.execute(retrieve_die_roll, (user_id,))
    raincoat_die_roll, = Database.cursor.fetchone()
    return raincoat_die_roll


async def remove_raincoat(user_id):
    change_it = "UPDATE residents SET raincoat = 0 WHERE id_number = ?"
    Database.cursor.execute(change_it, (user_id,))
    die_roll_reset = "UPDATE residents SET raincoat_die_roll = 0"
    Database.cursor.execute(die_roll_reset)
    Database.res_db_conn.commit()


async def increase_raincoat_break_prob(user_id):
    change_it = "UPDATE residents SET raincoat_die_roll = raincoat_die_roll - 1 WHERE id_number = (?)"
    Database.cursor.execute(change_it, (user_id,))
    Database.res_db_conn.commit()
