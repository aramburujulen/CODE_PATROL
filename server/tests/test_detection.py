from src.detection.algorithms.winnowing.process import compare_files
import pytest
from src.models.submission import Submission
from src.models.file import File
import os


TEST_FILES_PATH = os.path.join(os.path.dirname(__file__), "test_files")

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


def test_copied_functions_plagiarism():
    
    file1 = File(name="myExam.java", language="java")

    with open(os.path.join(TEST_FILES_PATH, "CopiedFunctions", "ejercicioAventura.java"), "r") as f:
        file1.content = f.read()
    
    file2 = File(name="myExamWithFriendsFunctions.java", language="java")

    with open(os.path.join(TEST_FILES_PATH, "CopiedFunctions", "ejercicioAventuraCompleto.java"), "r") as f:
        file2.content = f.read()

    result = compare_files(file1, file2)

    assert result["sim2"] > result["sim1"] and result["sim2"] > 60






    
