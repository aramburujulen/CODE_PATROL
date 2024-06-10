from src.detection.algorithms.winnowing.process import compare_files
import pytest
from src.models.submission import Submission
from src.models.file import File
from src.controllers import main_controller as mc
import os


TEST_FILES_PATH = os.path.join(os.path.dirname(__file__), "test_files")


#TEST: Comprobar que dos archivos claramente copiados devuelven un alto porcentaje de plagio.
def test_obvious_plagiarism():
    
    file1 = File(name="myExam.py", language="python")
    with open(os.path.join(TEST_FILES_PATH, "ObviousPlagiarism", "exercise1.py"), "r") as f:
        file1.content = f.read()

    file2 = File(name="myCopiedExam.py", language="python")
    with open(os.path.join(TEST_FILES_PATH, "ObviousPlagiarism", "copied_exercise1.py"), "r") as f:
        file2.content = f.read()

    
    result = compare_files(file1, file2, 5)
    print(str(result))
    assert result["sim1"] > 80 and result["sim2"] > 80

#TEST: Comprobar que un archivo tiene copiadas funciones de otro.
def test_copied_functions_plagiarism():
    
    file1 = File(name="myExam.java", language="java")

    with open(os.path.join(TEST_FILES_PATH, "CopiedFunctions", "ejercicioAventura.java"), "r") as f:
        file1.content = f.read()
    
    file2 = File(name="myExamWithFriendsFunctions.java", language="java")

    with open(os.path.join(TEST_FILES_PATH, "CopiedFunctions", "ejercicioAventuraCompleto.java"), "r") as f:
        file2.content = f.read()

    result = compare_files(file1, file2)

    assert result["sim2"] > result["sim1"] and result["sim2"] > 60


#TEST: Comprobar funcionalidad para procesar todas las entregas de un archivo.
def test_process_folder(client):

    zip_path = os.path.join(TEST_FILES_PATH, "SGE_examenes.zip")


    assert os.path.exists(zip_path)

    with open(zip_path, "rb") as f:

        data = {
            'file': (f, 'SGE_exams.zip'),
            'compareWithDB': 'false'
        }

        # Send POST request to the endpoint
        response = client.post('/processSubmissionFolder', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200


#TEST: Comprobar archivos que no están copiados
def test_not_copied_files():

    file1 = File(name="helloworld.py", language="python")

    with open(os.path.join(TEST_FILES_PATH, "NotPlagiarism", "hello.py"), "r") as f:
        file1.content = f.read()
    
    file2 = File(name="bubblesort.py", language="python")

    with open(os.path.join(TEST_FILES_PATH, "NotPlagiarism", "bubble_sort.py"), "r") as f:
        file2.content = f.read()

    result = compare_files(file1, file2)

    assert result["sim2"] < 50 and result["sim2"] < 50    