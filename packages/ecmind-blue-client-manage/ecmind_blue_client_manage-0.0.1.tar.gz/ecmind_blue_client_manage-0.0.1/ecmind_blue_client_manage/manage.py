from ecmind_blue_client import Job
from ecmind_blue_client import Client
from XmlElement import XmlElement


def get_users(client:Client) -> dict:
    user_list_result = client.execute(Job('mng.GetUserList', Flags=0))
    users_element = XmlElement.from_string(user_list_result.values['UserList']).find('Users')
    users_element.find('User').flag_as_list = True
    result = {}
    for user_entry in users_element.to_dict()['User']:
        result[user_entry['@benutzer']] = {
            'id': user_entry['@id'],
            'login': user_entry['@benutzer'],
            'name': user_entry['@name'],
            'guid': user_entry['@osguid'],
            'mail': user_entry['@osemail'],
            'locked': True if user_entry['@locked'] == 1 else False,
            'profile': user_entry['@profil'],
        }
    return result


def get_user_ids(client:Client) -> dict:
    return { u['id']: u for u in get_users(client).values() }


def get_user_guids(client:Client) -> dict:
    return { u['guid']: u for u in get_users(client).values() }