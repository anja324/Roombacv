
async def mentions_information(message):
    """
    determines if mentions are present.  if no, kicks back use mentions.  if yes, saves id and nick of the user mentioned

    :param message: raw user sent message
    :return: user_id, user_nick
    """
    mentions_list = message.mentions
    if len(mentions_list) == 0:
        await message.channel.send("Invalid parameter, please use a mention to select a user.")
    elif len(mentions_list) >= 2:
        await message.channel.send("Error: Roomba received multiple @mentions, when command calls for one.")
    else:
        user_id = mentions_list[0].id
        user_nick = mentions_list[0].nick or mentions_list[0].name
        return user_id, user_nick
