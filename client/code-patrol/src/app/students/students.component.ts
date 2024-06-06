import { Component, OnInit } from '@angular/core';
import {FormGroup, FormControl, ReactiveFormsModule } from '@angular/forms';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-students',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './students.component.html',
  styleUrl: './students.component.css'
})
export class StudentsComponent implements OnInit {

  students: any[] = []

  constructor(private api: ApiService) {}

  formStudent = new FormGroup({
    "id": new FormControl(""),
    "name": new FormControl(""),
    "surname": new FormControl("")
  })

  ngOnInit(): void {
    this.getStudents()
  }

  getStudents(){
    this.api.getStudents().subscribe((data) => {
      this.students = data
    })
  }

  onSubmit(){
    let newStudent = {
      id: this.formStudent.value.id,
      name: this.formStudent.value.name,
      surname: this.formStudent.value.surname
    };

    this.api.addStudent(newStudent).subscribe(() => {
      this.getStudents()
      this.formStudent.reset()
    })
  }

  deleteStudent(id:any){
    this.api.deleteStudent(id).subscribe(() => {
      this.getStudents()
    })
  }

}
