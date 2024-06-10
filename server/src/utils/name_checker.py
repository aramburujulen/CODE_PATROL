
DNI_REFS = [
    "T", "R", "W", "A", "G", "M", "Y", "F", 
    "P", "D", "X", "B", "N", "J", "Z", "S", 
    "Q", "V", "H", "L", "C", "K", "E"
]

#
# Pre:---
# Post: Función para validar el nombre de archivo del estudiante
# params: file_name
#
def check_file_name(file_name: str):

    try:
        
        data = file_name.split("_")
        print(data)
        if len(data) != 3:
            return False
        
        if  not check_id(data[0]):
            return False
        

        return True
    
    except Exception as e:
        print("Error attempting to check name, most likely invalid ", e)
        return False
    


#
# Pre:---
# Post: Función para comprobar la validez de un DNi/NIE siguiendo la fórmula utilizada
# params: dni
#
def check_id(dni):
    if dni[0] == "X" or dni[0] == "Y" or dni[0] == "Z":
        initial_conversion = {'X': '0', 'Y': '1', 'Z': '2'}
        numeric_value = int(initial_conversion[dni[0]] + dni[1:8])
    else:
        numeric_value = int(dni[:8])

    expected_ref = DNI_REFS[numeric_value % 23]
    return dni[8] == expected_ref

    


