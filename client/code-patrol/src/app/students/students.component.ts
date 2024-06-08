import { Component, OnInit } from '@angular/core';
import {FormGroup, FormBuilder, FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
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

  constructor(private api: ApiService, private fb: FormBuilder) {}

  formStudent = new FormGroup({
    "id": new FormControl(""),
    "name": new FormControl(""),
    "surname": new FormControl("")
  })

  formEditStudents: FormGroup[] = []

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

  getFormGroup(index: number){
    return this.formEditStudents[index]
  }

  editStudent(index: number) {
    const studentToEdit = this.students[index];
    this.students[index].editing = true;
    this.formEditStudents[index] = this.fb.group({
      std_id: [studentToEdit.student_id],
      new_name: [studentToEdit.name, Validators.required],
      new_surname: [studentToEdit.surname, Validators.required]
    });
  }

  saveStudent(index: number) {
    if (this.formEditStudents[index].valid) {
      const updatedData = this.formEditStudents[index].value;
      this.api.editStudent(updatedData).subscribe(() => {
        this.getStudents();
        this.students[index].editing = false;
      });
    }
  }

  cancelEdit(index: number) {
    this.students[index].editing = false;
    this.formEditStudents[index].reset();
  }
  

}
