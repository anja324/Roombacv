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


def store_gif_dict_creation():
    """
    creates an array of purchasable gif-objects

    :return: store_gif_dict
    """
    class PurchasableGif:
        def __init__(self, name, cost, link, rejection_message):
            self.name = name
            self.cost = cost
            self.link = link
            self.rejection_message = rejection_message

    store_gif_file = open("text_files/point_store_gifs", "r")
    store_gif_list = []
    store_gif_dict_init = {}

    for line in store_gif_file:
        gif = line.split(" ", 3)
        store_gif_list.append(gif)

    for gif in store_gif_list:
        gif_to_add = PurchasableGif(*gif)
        store_gif_dict_init[gif_to_add.name] = gif_to_add

    return store_gif_dict_init


async def gif_purchase(message):
    """
    Posts purchased gif, provided user can afford it.
    :param message: The raw user inputted message
    :return:
    """

    #   retrieves author score information
    user_id = message.author.id
    current_score = await score_query(user_id)
    #   identify desired gif
    requested_gif = store_gif_dict.get(message.content)
    #   determine if gif is eligible to be purchased and send gif or rejection message
    if current_score >= int(requested_gif.cost):
        amount_to_deduct = requested_gif.cost
        await deduct_from_score(user_id, amount_to_deduct)
        await message.channel.send(f"You have spent {requested_gif.cost} AnjaPoints™️")
        await message.channel.send(requested_gif.link)
    else:
        await message.channel.send(requested_gif.rejection_message)

store_gif_dict = store_gif_dict_creation()
