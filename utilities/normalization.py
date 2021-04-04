import string


def tidying_caps_punct(message):
    """
    returns a list of message contents with no capital letters or punctuation
    
    :param message: the contents of a user sent message in any channel of the guild
    :return: a list of the user sent message content lowered with no punctuation
    """

    #   create both a lowered message for direct reference, and an array of each word in the lowered message
    lowered_message = message.content.lower()
    lowered_message_list = lowered_message.split(" ")

    #  remove punctuation
    no_punct_list = []
    for entry in lowered_message_list:
        no_punct = entry.translate(str.maketrans("", "", string.punctuation))
        no_punct_list.append(no_punct)

    return no_punct_list, lowered_message