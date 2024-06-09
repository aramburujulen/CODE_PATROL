import os
import pytest
from io import BytesIO

def test_students(client):
    response = client.get('/students')
    assert response.status_code == 200


def test_insert_student(client):
    student_data = {
        "id": "123",
        "name": "Steve",
        "surname": "Stevenson"
    }

    response = client.post('/addStudent', json = student_data)
    assert response.status_code == 200


def test_insert_submission(client):
    submission_data = {
        "student_id": "123",
        "name": "Steve's Exam",
        "subject": "Math",
        "date": "2024-08-21"
    }

    file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'SubmissionToAdd.zip')

    with open(file_path, 'rb') as f:
        file_bytes = BytesIO(f.read())
        file_bytes.name = 'SubmissionToAdd.zip'

    submission_data["file"] = file_bytes

    response = client.post('/addSubmission', data=submission_data, content_type='multipart/form-data')
    
    assert response.status_code == 200


def test_delete_submission(client):

    response = client.delete("/deleteSubmission/1")

    assert response.status_code == 204



def test_delete_student(client):
    
    response = client.delete("/deleteStudent/123")

    assert response.status_code == 204






    








