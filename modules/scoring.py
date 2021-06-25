from database.database_functions import Database
from utilities.normalization import *
from database.database_functions import *


async def tabulate_message_score(message):
    score_addition = 0
    if message.content.startswith("!"):
        return
    no_punct_list, lowered_message = tidying_caps_punct(message)
    if len(no_punct_list) > 1:
        score_addition = len(no_punct_list) * .5

    user_id = message.author.id
    amount_to_add = score_addition
    await add_to_score(user_id, amount_to_add)
    return


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