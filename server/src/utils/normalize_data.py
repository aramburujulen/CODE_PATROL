

def normalize_data(data):

    if isinstance(data, list):
        normalized_dict_list = []
        for object in data:
            normalized_dict_list.append(normalize_data(object))
        return normalized_dict_list
    elif hasattr(data, "__table__"):
        normalized_dict = {}
        for col in data.__table__.columns:
            normalized_dict[col.name] = getattr(data, col.name)
        
        return normalized_dict
    




