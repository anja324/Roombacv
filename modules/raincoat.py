import random
from database.database_functions import Database


async def raincoat_db_add(user_id):
    """
    Adds a raincoat to the appropriate column in the database along with a die roll column for breakage.
    :param user_id: user id of the resident who purchased the raincoat
    :return: None
    """

    change_it = "UPDATE residents SET raincoat = 1 WHERE id_number = ?"
    Database.cursor.execute(change_it, (user_id,))
    die_roll_set = "UPDATE residents SET raincoat_die_roll = 7"
    Database.cursor.execute(die_roll_set)
    Database.res_db_conn.commit()


async def raincoat_die_roll(user_id, message):
    """
    Rolls a die to determine whether or not the resident's raincoat breaks
    :param user_id: id of the user wearing the raincoat
    :param message: raw user inputted message
    :return: None
    """

    die_to_roll = await retrieve_raincoat_die_roll(user_id)
    if die_to_roll <= 1:
        await remove_raincoat(user_id)
        await message.channel.send("Your raincoat has broken.  So sad.  Maybe buy a new one?")
    else:
        roll_it = random.randint(1, die_to_roll)
        if roll_it == 1:
            raincoat_flavortext_array = create_raincoat_flavortext_array()
            await remove_raincoat(user_id)
            await notify_user_of_breakage(message, raincoat_flavortext_array)
        else:
            await increase_raincoat_break_prob(user_id)


async def increase_raincoat_break_prob(user_id):
    """
    Decreases the number of sides on the die used to determine whether the raincoat breaks with each usage.
    :param user_id: the id of the user wearing the raincoat
    :return: None
    """

    change_it = "UPDATE residents SET raincoat_die_roll = raincoat_die_roll - 1 WHERE id_number = (?)"
    Database.cursor.execute(change_it, (user_id,))
    Database.res_db_conn.commit()


async def retrieve_raincoat(user_id):
    """
    Determines if the user has a raincoat.
    :param user_id: the id of the user in question
    :return: raincoat status boolean
    """

    retrieve_raincoat_status = "SELECT raincoat FROM residents WHERE id_number == (?)"
    Database.cursor.execute(retrieve_raincoat_status, (user_id,))
    raincoat_status, = Database.cursor.fetchone()
    return raincoat_status


async def retrieve_raincoat_die_roll(user_id):
    """
    Retrieves the current probability of the raincoat breaking.
    :param user_id: the id of the user in question
    :return: raincoat die roll integer
    """

    retrieve_die_roll = "SELECT raincoat_die_roll FROM residents WHERE id_number == (?)"
    Database.cursor.execute(retrieve_die_roll, (user_id,))
    raincoat_die_roll, = Database.cursor.fetchone()
    return raincoat_die_roll


def create_raincoat_flavortext_array():
    """
    creates a dictionary which holds all raincoat breaking responses

    :return:dictionary of all raincoat breaking flavortext
    """

    response_array = open("text_files/raincoat_flavor_text", "r")
    raincoat_flavortext_array = []
    for line in response_array:
        raincoat_flavortext_array.append(line)
    return raincoat_flavortext_array


async def remove_raincoat(user_id):
    """
    Removes the user's raincoat after it breaks.
    :param user_id: the id of the user who has broken their raincoat
    :return: None
    """

    change_it = "UPDATE residents SET raincoat = 0 WHERE id_number = ?"
    Database.cursor.execute(change_it, (user_id,))
    die_roll_reset = "UPDATE residents SET raincoat_die_roll = 0"
    Database.cursor.execute(die_roll_reset)
    Database.res_db_conn.commit()


async def notify_user_of_breakage(message, raincoat_flavortext_array):
    """
    Selects a random flavortext from the list and notifies the user that their raincoat has broken.
    :param message: raw user inputted message
    :param raincoat_flavortext_array: an array of all of the potential flavortext for when a raincoat breaks
    :return: None
    """

    flavortext_length = len(raincoat_flavortext_array) - 1
    roll_it = random.randint(0, flavortext_length)
    await message.channel.send(raincoat_flavortext_array[roll_it])



