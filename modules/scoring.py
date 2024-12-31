from database.database_functions import Database
from utilities.normalization import *
from database.database_functions import *
from utilities.user_identification import *


async def tabulate_message_score(message):
    """
    tabulates the score value of the message sent, providing it is not a command

    :param message: Raw user inputted message object
    :return: None
    """

    #   sets the base values for the variables score addition, and sets embeds/attachments to a default of false
    score_addition = 0
    embed_attach_status = False

    #   rejects any bot commands as not relevant to points score tabulation
    if message.content.startswith("!"):
        return

    #   creates a list that identifies each word in the message
    no_punct_list, lowered_message = tidying_caps_punct(message)

    #   checks to see if there are any embeds or attachments and changes the variable accordingly
    if len(message.embeds) == 1 or len(message.attachments) == 1:
        embed_attach_status = True

    #   assigns a score to the user based on the number of words in their message (or whether their message is an embed)
    if embed_attach_status is True:
        score_addition = 5
    elif len (no_punct_list) >= 80:
        score_addition = 0
    elif len(no_punct_list) in range(20-80):
        score_addition = 20
    elif len(no_punct_list) in range(10, 20):
        score_addition = len(no_punct_list) * 1
    elif len(no_punct_list) <= 9:
        score_addition = len(no_punct_list) * .5

    #   halves a user's assigned score if the have the role "Naughty Corner"
    nc_status = await user_is_naughty(message)
    if nc_status:
        score_addition = score_addition / 2

    #   sets a user's assigned score to zero if the have the role "Very Naughty Corner"
    vnc_status = await user_is_very_naughty(message)
    if vnc_status:
        score_addition = score_addition / 4

    #   fetches the info of the resident who sent the message, and adds the score via the db
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
    raw_score, = Database.cursor.fetchone()
    score = int(round(raw_score, 0))
    return score


async def add_to_score(user_id, amount_to_add):
    """
    adds the designated amount to the user's score

    :param user_id: the id of the user whose information will change
    :param amount_to_add: the number of points to be added
    :return: None
    """

    change_it = "UPDATE residents SET score = score + ? WHERE id_number = ?"
    Database.cursor.execute(change_it, (amount_to_add, user_id))
    Database.res_db_conn.commit()


async def deduct_from_score(user_id, amount_to_deduct):
    """
    deducts the designated amount from the users score

    :param user_id: the id of the user whose information will change
    :param amount_to_deduct: the number of points to be added
    :return: None
    """

    change_it = "UPDATE residents SET score = score - ? WHERE id_number = ?"
    Database.cursor.execute(change_it, (amount_to_deduct, user_id))
    Database.res_db_conn.commit()


async def add_count_score(user_id, amount_to_add):
    """
    adds the designated amount to the user's count score

    :param user_id: the id of the user whose information will change
    :param amount_to_add: the id of the user whose information will change
    :return: None
    """

    change_it = "UPDATE residents SET count_number = count_number + ? WHERE id_number = ?"
    Database.cursor.execute(change_it, (amount_to_add, user_id))
    Database.res_db_conn.commit()


async def count_score_query(user_id):
    """
    Retrieves the count score of the requested user

    :param user_id: the id of the requested user
    :return: count_score
    """

    retrieve_count_score = """SELECT count_number
                        FROM residents
                        WHERE id_number == (?)"""

    Database.cursor.execute(retrieve_count_score, (user_id,))
    raw_score, = Database.cursor.fetchone()
    score = int(round(raw_score, 0))
    return score
