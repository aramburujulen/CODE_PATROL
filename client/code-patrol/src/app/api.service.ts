import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  processSubmissionFolder(file: any):Observable<any>{
    return this.http.post("http://localhost:5000/processSubmissionFolder", file);
  }

  getStudents():Observable<any>{
    return this.http.get("http://localhost:5000/students")
  }

  addStudent(data:any):Observable<any>{
    return this.http.post("http://localhost:5000/addStudent", data)
  }

  deleteStudent(id:any): Observable<any>{
    return this.http.delete(`http://localhost:5000/deleteStudent/${id}`)
  }

  getSubmissions(): Observable<any>{
    return this.http.get("http://localhost:5000/submissions")
  }

  addSubmission(data:any): Observable<any>{
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/json');
    return this.http.post("http://localhost:5000/addSubmission", data, {headers: headers})
  }

  compareSubmissions(data:any): Observable<any>{
    return this.http.post("http://localhost:5000/compareSubmissions", data)
  }

  deleteSubmission(sub_id:any): Observable<any>{
    return this.http.delete(`http://localhost:5000/deleteSubmission/${sub_id}`)
  }

  getFilteredSubmissions(filters: any): Observable<any>{
    return this.http.post("http://localhost:5000/filterSubmissions", filters)
  }

  editStudent(data: any): Observable<any>{
    return this.http.put("http://localhost:5000/editStudent", data)
  }
}
