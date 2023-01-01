from database.database_functions import Database
from utilities.normalization import *
from database.database_functions import *
from utilities.user_identification import user_is_mod


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
        await user_is_mod(message)
        return

    #   creates a list that identifies each word in the message
    no_punct_list, lowered_message = tidying_caps_punct(message)

    #   checks to see if there are any embeds or attachments and changes the variable accordingly
    if len(message.embeds) == 1 or len(message.attachments) == 1:
        embed_attach_status = True

    #   assigns point value to embeds/attachments, messages longer than 10 words, and messages shorter than 10 words
    if embed_attach_status is True:
        score_addition = 5
    elif len(no_punct_list) > 10:
        score_addition = len(no_punct_list) * 1
    elif len(no_punct_list) < 10:
        score_addition = len(no_punct_list) * .5

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
    score, = Database.cursor.fetchone()
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