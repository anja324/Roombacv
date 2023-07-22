from modules.scoring import deduct_from_score


async def someone_cheated(message):
    """
    determines whether someone used a gif he should have paid for in the user message, charges the user,
      and logs occurrence in a logs channel
    """
    list_of_purchases = ["https://tenor.com/view/ok-bro-gif-23915781", "https://tenor.com/view/cookies-gif-14785632", "https://tenor.com/bpHsW.gif"]

    user_id = message.author.id
    double_price = 1000

    #   okbro
    if message.content == list_of_purchases[0]:
        await deduct_from_score(user_id, double_price)
        await message.channel.send(f"You have attempted to use eye-candy without paying.  Shame on you (probably Vin!).  Your balance has been reduced by double the cost ({double_price} AnjaPoints™️)")

    #   nom
    elif message.content == list_of_purchases[1]:
        await deduct_from_score(user_id, 100)
        await message.channel.send(f"You have attempted to nom cookies without paying.  Shame on you.  Your balance has been reduced by double the cost (100 AnjaPoints™️)")

    #   uwu
    elif message.content == list_of_purchases[2]:
        await deduct_from_score(user_id, double_price)
        await message.channel.send(f"You have attempted to uwu without paying.  Shame on you.  Your balance has been reduced by double the cost ({double_price} AnjaPoints™️)")

    else:
        return

