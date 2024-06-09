from src.detection.comparison_thread import ComparisonThread
from zipfile import ZipFile
from src.models.submission import Submission
from src.models.student import Student
from src.models.file import File
from src.models.submission_comparison import submission_comparison
from datetime import datetime
from flask import Response, current_app
from sqlalchemy import Insert
from io import BytesIO
from src.utils.name_checker import check_file_name
from src.models import db
from sqlalchemy.orm import joinedload
import os

def compare_submissions_from_folder(zip_file, compare_with_db):
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
                is_valid = check_file_name(folder_name)
                new_submission = Submission(
                    name = folder_name if is_valid else "INVALID",
                    date = datetime.now(),
                    subject = zip_file.filename.split("_")[0],
                    student_id = folder_name.split("_")[0] if is_valid else 999
                )
                new_submission.files.extend(obtain_files(zip_pointer, folder_name, ""))
                submissions.append(new_submission)
                if not is_valid:
                    results.append({
                        "error": "INVALID SUBMISSION NAME",
                        "name": folder_name
                    })
            elif folder_name.endswith(".zip"):
                print("ZIP DETECTED")
                is_valid = check_file_name(folder_name)
                with zip_pointer.open(folder_name) as file:
                    with ZipFile(BytesIO(file.read())) as zip_sub_pointer:
                        new_submission = Submission(
                            name = folder_name if is_valid else "INVALID",
                            date = datetime.now(),
                            subject = zip_file.filename.split("_")[0],
                            student_id = folder_name.split("_")[0] if is_valid else 999
                        )
                        new_submission.files.extend(obtain_files(zip_sub_pointer, "", folder_name.split(".")[0] + "/"))
                        submissions.append(new_submission)
                if not is_valid:
                    results.append({
                        "error": "INVALID SUBMISSION NAME",
                        "name": folder_name
                    })
    print(f"LENGHT {len(submissions)}")
    if compare_with_db:
        all_submissions = submissions
        all_submissions.extend(get_submissions_from_subject(zip_file.filename))
        threads = []
        for i in range(len(all_submissions)):
            for j in range(i, len(all_submissions)):
                if(i != j):
                    new_thread = ComparisonThread(current_app._get_current_object(), all_submissions[i], all_submissions[j])
                    new_thread.start()
                    threads.append(new_thread)
    else:
        threads = []
        for i in range(len(submissions)):
            for j in range(i, len(submissions)):
                if(i != j):
                    new_thread = ComparisonThread(current_app._get_current_object(), submissions[i], submissions[j])
                    new_thread.start()
                    threads.append(new_thread)

    
    
    for thread in threads:
        thread.join()

    valid_submissions = list(filter(lambda sub: sub.name != "INVALID", submissions))
    insert_submissions(valid_submissions)

    for thread in threads:
        results.extend(thread.results)

    print(str(results) + "I AM HERE I AM HERE I AM HERE")
    return results


def obtain_files(zip_pointer, parent, saved_path):
    files = []

    for file_name in zip_pointer.namelist():
        if file_name.startswith(parent) and not file_name.endswith("/"):
            with zip_pointer.open(file_name) as f:
                try:
                    content = f.read().decode("utf-8")
                    files.append(File(name=os.path.join(saved_path, parent, file_name), content=content))
                except Exception as e:
                    print(f"Skipping file with weird decoding: {file_name}", e)
                    continue
    print(files)
    return files


def compare_submissions(ids_a, ids_b):

    try:

        submissions_a = Submission.query \
            .filter(Submission.submission_id.in_(ids_a)) \
            .options(joinedload(Submission.files)) \
            .all()

        submissions_b = Submission.query \
            .filter(Submission.submission_id.in_(ids_b)) \
            .options(joinedload(Submission.files)) \
            .all()
        
        print(str(len(submissions_a)))
        print(str(len(submissions_b)))
        threads = []
        for submission_a in submissions_a:
            for submission_b in submissions_b:
                new_thread = ComparisonThread(current_app._get_current_object(), submission_a, submission_b)
                threads.append(new_thread)
                new_thread.start()
        
        for thread in threads:
            thread.join()
        
        print(len(threads))
        results = []

        
        for thread in threads:
            results.extend(thread.results)

        insert_comparisons(results)
        return results
    
    except Exception as e:
        print("Error comparing submissions", e)
        return Response(status=404)

    
def insert_comparisons(results):
    try:
        print(results)
        comparison_values = []
        for result in results:
            if result["file_1_sub_id"] and result["file_2_sub_id"]:
                comparison_values.append({
                    "submission_1_id": result["file_1_sub_id"],
                    "submission_2_id": result["file_2_sub_id"],
                    "overlap_in_s1": result["sim1"],
                    "overlap_in_s2": result["sim2"]
                })
        if comparison_values:
            insert_stmt = submission_comparison.insert().values(comparison_values)
            db.session.execute(insert_stmt)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Error attempting to store comparison ", e)


def insert_submissions(submissions):
    try:
        for submission in submissions:
            student = Student.query.get(submission.student_id)

            if not student:
                student = Student(
                    student_id=submission.student_id,
                    name=submission.name.split("_")[1],
                    surname=submission.name.split("_")[2].replace(".zip", "")
                )
                db.session.add(student)

        db.session.add_all(submissions)
        db.session.commit()
    finally:
        db.session.close()

def get_submissions_from_subject(subject):
    try:
        submissions = Submission.query.filter_by(subject=subject).all()

        return submissions
    except Exception as e:
        print("Error getting submissions", e)
        return []


