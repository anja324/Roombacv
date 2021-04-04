

def create_easter_egg_dict():
    """
    creates a dictionary which holds all easter eggs and responses

    :return:dictionary of all easter eggs
    """

    response_dict = open("text_files/easter_egg_responses", "r")
    easter_egg_dict = {}
    for line in response_dict:
        split_line = line.split(" ", 1)
        easter_egg_dict.update({split_line[0]: split_line[1]})
    return easter_egg_dict


async def easter_eggs(message, easter_egg_dict, lowered_message):
    """
    searches lowered message for easter egg keywords, prints the desired response in channel

    :param message: raw user sent message
    :param easter_egg_dict: easter egg triggers and their responses
    :param lowered_message: lowercase version of user message
    :return: None
    """
    #   dictionary format: { trigger : response }
    maybe_easter_egg = easter_egg_dict.get(lowered_message)
    if maybe_easter_egg is not None:
        await message.channel.send(maybe_easter_egg)
