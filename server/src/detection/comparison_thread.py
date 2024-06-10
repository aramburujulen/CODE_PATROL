import threading
from src.detection.algorithms.winnowing.process import compare_files
import time
from flask import Flask
from src.models import db

#Hilo para comprobar dos entregas
class ComparisonThread(threading.Thread):

    def __init__(self, app: Flask, submission_1, submission_2):
        super().__init__()
        self.submission_1 = submission_1
        self.submission_2 = submission_2
        self.app = app
        self.results = []

    #
    # Pre:---
    # Post: Función override de run encargada de comparar archivo por archivo y detectar plagios.
    # Devuelve los resultados alarmantes
    #
    def run(self):
        with self.app.app_context():
            start_time = time.time()
            results = []
            for file_a in self.submission_1.files:
                for file_b in self.submission_2.files:
                    if(file_a.language == file_b.language or file_a.name.split(".")[1] == file_b.name.split(".")[1]):
                        results.append(compare_files(file_a, file_b))
            
            filtered_results = filter(lambda res: res["sim1"] >= 50.0 or res["sim2"] >= 50.0, results)
            self.results = filtered_results

            end_time = time.time()
            print(f"Processed in {(end_time - start_time) * 1000} ms")

            db.session.remove()
        
    
        
        

    


    
        

        