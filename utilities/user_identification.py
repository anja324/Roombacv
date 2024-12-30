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


async def user_is_naughty(message):
    """
    looks at a member's roles to determine if they are in the naughty corner and will receive a point penalty

    :param message: raw user submitted object
    :return: nc_status
    """

    nc_status = False
    roles = message.author.roles
    for role in roles:
        if role.name == "Naughty Corner":
            nc_status = True
    return nc_status


async def user_is_very_naughty(message):
    """
    looks at a member's roles to determine if they are in the very naughty corner and will receive no points

    :param message: raw user submitted object
    :return: vnc_status
    """

    vnc_status = False
    roles = message.author.roles
    for role in roles:
        if role.name == "Very Naughty Corner":
            vnc_status = True
    return vnc_status

