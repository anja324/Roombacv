from resident_member_info.Resident import Resident
from utilities.json_tokens import JsonConfig


async def accept_new_resident(member, resident_roster):
    """
    Greets a new member of the server, and adds them to the database

    :param resident_roster: a list of all resident-objects
    :param member: the discord provided member object
    :return: None
    """

    #   Greets member
    await JsonConfig.channel.audits.send(f"New User: {member}!")
    await JsonConfig.channel.lounge.send(f"You have arrived at Anja's House!  Welcome to the family <3.  "
                                          f"Please mind the rules, found in {JsonConfig.channel.rules.mention}."
                                          f"If you are a rat and wish to be added to the 'Fuel Rat' group, please hit up an admin or a mod.")

    #   Adds to DB
    new_res = Resident(member.name, member.id)
    resident_roster.append(new_res)
    new_res.create_database_entry()
