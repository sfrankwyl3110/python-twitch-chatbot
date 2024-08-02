def hasKey(current_dict: dict, key):
    return key in list(current_dict.keys())


def get_dict_with_highest_key_value(dict_list, key='importance'):
    if not dict_list:
        return None  # Return None if the list is empty
    return max(dict_list, key=lambda x: x.get(key, float('-inf')))
