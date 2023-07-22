from modules.raincoat import retrieve_raincoat, raincoat_db_add
from modules.scoring import deduct_from_score, score_query


async def buy_raincoat(message):
    """
    Buys a raincoat.
    :param message: Raw user inputted message.
    :return:
    """

    user_id = message.author.id
    raincoat_status = await retrieve_raincoat(user_id)
    current_score = await score_query(user_id)
    cost_of_raincoat = int(round((current_score * 3 / 100), 0))
    print(cost_of_raincoat)
    if raincoat_status == 1:
        await message.channel.send("You already own a raincoat.")
    elif current_score < cost_of_raincoat:
        await message.channel.send("You can't afford this.")
    else:
        await raincoat_db_add(user_id)
        user_id = message.author.id
        await deduct_from_score(user_id, cost_of_raincoat)
        await message.channel.send(f"You have purchased a raincoat for {cost_of_raincoat} AnjaPoints™️.")


async def uwu(message):
    """
    Posts a gif of a weeb uwu and deducts 500 points from the user
    :param message: The raw user inputted message
    :return:
    """

    user_id = message.author.id
    current_score = await score_query(user_id)
    if current_score >= 500:
        amount_to_deduct = 500
        await deduct_from_score(user_id, amount_to_deduct)
        await message.channel.send("You have spent 500 AnjaPoints™️")
        await message.channel.send("https://tenor.com/bpHsW.gif")
    else:
        await message.channel.send("You cannot afford to uwu.")


async def nom(message):
    """
    Posts a link containing a cookie monster gif and deducts 50 points from the user.
    :param message: The raw user inputted message
    :return:
    """

    user_id = message.author.id
    current_score = await score_query(user_id)
    if current_score >= 50:
        amount_to_deduct = 50
        await deduct_from_score(user_id, amount_to_deduct)
        await message.channel.send("You have spent 50 AnjaPoints™️")
        await message.channel.send("https://tenor.com/view/cookies-gif-14785632")
    else:
        await message.channel.send("You cannot afford to nom.")