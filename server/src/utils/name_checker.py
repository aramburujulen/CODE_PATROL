
DNI_REFS = [
    "T", "R", "W", "A", "G", "M", "Y", "F", 
    "P", "D", "X", "B", "N", "J", "Z", "S", 
    "Q", "V", "H", "L", "C", "K", "E"
]


def check_file_name(file_name: str):

    try:
        data = file_name.split("_")

        if len(data) != 3:
            return False
        
        if  not check_id(data[0]):
            return False
        

        return True
    
    except Exception as e:
        print("Error attempting to check name, most likely invalid ", e)
        return False
    


def check_id(dni):

    if dni[0] == "X" or dni[0] == "Y" or dni[0] == "Z":
        initial_conversion = {'X': '0', 'Y': '1', 'Z': '2'}
        numeric_value = int(initial_conversion[dni[0]] + dni[1:8])
    else:
        numeric_value = int(dni[:8])
        print(str(numeric_value % 23))


    return dni[8] == DNI_REFS[numeric_value % 23]

    


