def get_unique_types(types):
    result = []
    for i in types:
        if i not in result:
            result.append(i)

    return result        


def get_groups_of_types(all_items,answer):
    result = []

    for i in all_items:
        if i.type == answer:
            if i.group not in result:
                result.append(i.group)

    return result


def get_items_of_group(all_items, type, group):
    result = []

    for i  in all_items:
        if i.type == type and i.group == group:
            if i.name not in result:
                result.append(i.name)  

    return result            


def get_item(all_items, item):
    for i in all_items:
        if i.name == item:
            return i    