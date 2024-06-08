from detection.comparison_thread import ComparisonThread
from zipfile import ZipFile
from models.submission import Submission
from models.file import File
from datetime import datetime
from flask import Response, current_app
from io import BytesIO
from utils.name_checker import check_file_name
import os

def compare_submissions_from_folder(zip_file):
    submissions = []
    results = []
    with ZipFile(zip_file, "r") as zip_pointer:
        first_level_folders = set()

        for folder_name in zip_pointer.namelist():
            if "/" in folder_name:
                first_level_folders.add(folder_name.split("/")[0] + "/")
            elif folder_name.endswith(".zip"):
                first_level_folders.add(folder_name)

        
        for folder_name in first_level_folders:
            if folder_name.endswith("/"):
                if check_file_name(folder_name):

                    new_submission = Submission(
                        submission_id = 99,
                        name = folder_name,
                        date = datetime.now(),
                        subject = "default",
                        student_id = "default"
                    )
                    new_submission.files.extend(obtain_files(zip_pointer, folder_name, ""))
                    submissions.append(new_submission)
                else:
                    results.append({
                        "error": "INVALID SUBMISSION NAME",
                        "name": folder_name
                    })
            elif folder_name.endswith(".zip"):
                print("ZIP DETECTED")
                if check_file_name(folder_name):
                    with zip_pointer.open(folder_name) as file:
                        with ZipFile(BytesIO(file.read())) as zip_sub_pointer:
                            new_submission = Submission(
                                submission_id = 99,
                                name = folder_name,
                                date = datetime.now(),
                                subject = "default",
                                student_id = "default"
                            )
                            new_submission.files.extend(obtain_files(zip_sub_pointer, "", folder_name.split(".")[0] + "/"))
                            submissions.append(new_submission)
                else:
                    results.append({
                        "error": "INVALID SUBMISSION NAME",
                        "name": folder_name
                    })
    print(f"LENGHT {len(submissions)}")
    threads = []
    for i in range(len(submissions)):
        for j in range(i, len(submissions)):
            if(i != j):
                new_thread = ComparisonThread(current_app._get_current_object(), submissions[i], submissions[j])
                new_thread.start()
                threads.append(new_thread)
                
    for thread in threads:
        thread.join()

    

    for thread in threads:
        results.extend(thread.results)

    return results


def obtain_files(zip_pointer, parent, saved_path):
    files = []

    for file_name in zip_pointer.namelist():
        if file_name.startswith(parent) and not file_name.endswith("/"):
            with zip_pointer.open(file_name) as f:
                try:
                    content = f.read().decode("utf-8")
                    files.append(File(file_id=99, name=os.path.join(saved_path, parent, file_name), content=content))
                except Exception as e:
                    print(f"Skipping file with weird decoding: {file_name}", e)
                    continue
    print(files)
    return files


def compare_submissions(ids_a, ids_b):

    try:
        print(ids_a)
        print(ids_b)
        submissions_a = Submission.query.filter(Submission.submission_id.in_(ids_a)).all()

        submissions_b = Submission.query.filter(Submission.submission_id.in_(ids_b)).all()
        
        threads = []
        for submission_a in submissions_a:
            for submission_b in submissions_b:
                new_thread = ComparisonThread(current_app._get_current_object(), submission_a, submission_b)
                new_thread.start()
                threads.append(new_thread)
        
        for thread in threads:
            thread.join()
        
        results = []


        for thread in threads:
            results.extend(thread.results)
        
        return results
    
    except Exception as e:
        print("Error comparing submissions", e)
        return Response(status=404)

    

    

    


