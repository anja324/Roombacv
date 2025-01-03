from database.database_functions import *
from utilities.json_tokens import JsonConfig
from utilities.normalization import tidying_caps_punct


async def leaderboard_bottom_five(message):
    """
    retrieves and prints the bottom five scores in the community

    :param message: the contents of the raw user message
    :return: None
    """

    no_punct_list, lowered_message, = tidying_caps_punct(message)
    if len(no_punct_list) > 1:
        await message.channel.send("This command does not take any parameters.")
    else:
        non_zero_scores = []
        score_id_list = await retrieve_leaderboard()
        for user_tuple in score_id_list:
            if user_tuple[0] <= 0:
                continue
            else:
                non_zero_scores.append(user_tuple)
        if len(non_zero_scores) > 5:
            non_zero_scores.reverse()
            print(non_zero_scores)
            placed_list = enumerate(non_zero_scores[:5], 1)
            bottom_five = "The bottom five residents are:\n"
            for place, (score, name) in placed_list:
                bottom_five += f"{place}.  {name}, {int(score)} AnjaPoints™️\n"
            await JsonConfig.channel.botSpam.send(bottom_five)
        else:
            await message.channel.send("There are not enough residents to determine a bottom five board.")


async def leaderboard(message):
    """
    provide the leaderboard of all community members who have spoken and their scores

    :param message: Raw user inputted message object
    :return: None
    """
    no_punct_list, lowered_message, = tidying_caps_punct(message)
    if len(no_punct_list) > 1:
        await message.channel.send("This command does not take any parameters.")
    else:
        non_zero_scores = []
        score_id_list = await retrieve_leaderboard()
        for user_tuple in score_id_list:
            if user_tuple[0] <= 0:
                continue
            else:
                non_zero_scores.append(user_tuple)
        leaderboard_writeup = "The current resident balances are:\n"
        placed_list = enumerate(non_zero_scores, 1)
        for place, (score, name) in placed_list:
            leaderboard_writeup += f"{place}.  {name}, {int(score)} AnjaPoints™️\n"
        await JsonConfig.channel.botSpam.send(leaderboard_writeup)


async def leaderboard_top_five(message):
    """
    provides the top five users on the leaderboard

    :param message: Raw user inputted message object
    :return: None
    """
    no_punct_list, lowered_message, = tidying_caps_punct(message)
    if len(no_punct_list) > 1:
        await message.channel.send("This command does not take any parameters.")
    else:
        score_id_list = await retrieve_leaderboard()
        placed_list = enumerate(score_id_list[:5], 1)
        top_five = "The top five residents are:\n"
        for place, (score, name) in placed_list:
            top_five += f"{place}.  {name}, {int(score)} AnjaPoints™️\n"
        await JsonConfig.channel.botSpam.send(top_five)


async def leaderboard_top_ten(message):
    """
    provides the top ten users on the leaderboard

    :param message: Raw user inputted message object
    :return: None
    """
    no_punct_list, lowered_message, = tidying_caps_punct(message)
    if len(no_punct_list) > 1:
        await message.channel.send("This command does not take any parameters.")
    else:
        score_id_list = await retrieve_leaderboard()
        placed_list = enumerate(score_id_list[:10], 1)
        top_ten = "The top ten residents are:\n"
        for place, (score, name) in placed_list:
            top_ten += f"{place}.  {name}, {int(score)} AnjaPoints™️\n"
        await JsonConfig.channel.botSpam.send(top_ten)


async def count_leaderboard(message):
    """
    provide the count leaderboard of all community members who have counted and their scores

    :param message: Raw user inputted message object
    :return: None
    """
    no_punct_list, lowered_message, = tidying_caps_punct(message)
    if len(no_punct_list) > 1:
        await message.channel.send("This command does not take any parameters.")
    else:
        non_zero_scores = []
        score_id_list = await retrieve_count_leaderboard()
        for user_tuple in score_id_list:
            if user_tuple[0] <= 0:
                continue
            else:
                non_zero_scores.append(user_tuple)
        leaderboard_writeup = "The current resident count balances are:\n"
        placed_list = enumerate(non_zero_scores, 1)
        for place, (score, name) in placed_list:
            leaderboard_writeup += f"{place}.  {name}, {int(score)} times counted.  Ah ah ah.️\n"
        await JsonConfig.channel.botSpam.send(leaderboard_writeup)