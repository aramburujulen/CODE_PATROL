import { Component, OnInit } from '@angular/core';
import {FormGroup, FormControl, ReactiveFormsModule } from '@angular/forms';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-new-submission',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './new-submission.component.html',
  styleUrl: './new-submission.component.css'
})
export class NewSubmissionComponent implements OnInit {

  students : any[] = []

  file:any
  constructor(private api: ApiService) {}

  formNewSub = new FormGroup({
    "student_id" : new FormControl(""),
    "name" : new FormControl(""),
    "date" : new FormControl(""),
    "subject" : new FormControl("")
  })

  ngOnInit(): void {
    this.api.getStudents().subscribe((data) => {
      this.students = data
    })
  }

  onSubmit(){
    const formData = new FormData();
    formData.append('student_id', this.formNewSub.value.student_id!);
    formData.append('name', this.formNewSub.value.name!);
    formData.append('date', this.formNewSub.value.date!);
    formData.append('subject', this.formNewSub.value.subject!);
    formData.append('file', this.file);
    console.log(formData)
    this.api.addSubmission(formData).subscribe(() => {})
  }

  onFileChange(event: any) {
    if (event.target.files.length > 0) {
      this.file = event.target.files[0];
    }
  }
}
