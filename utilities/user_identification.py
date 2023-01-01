async def user_is_mod(message):
    """
    looks at a member's roles to determine if they have sufficient permissions to perform an action

    :param message: raw user submitted object
    :return: mod_status
    """

    mod_status = False
    roles = message.author.roles
    for role in roles:
        if role.name == "Moderator" or role.name == "Administrator":
            mod_status = True
    return mod_status

