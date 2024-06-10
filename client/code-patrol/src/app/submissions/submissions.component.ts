import { Component, OnInit } from '@angular/core';
import { DragDropModule, moveItemInArray, CdkDragDrop, transferArrayItem, copyArrayItem } from '@angular/cdk/drag-drop';
import { ApiService } from '../api.service';
import { ResultsService } from '../results.service';
import { Router } from '@angular/router';
import {FormGroup, FormControl, ReactiveFormsModule } from '@angular/forms';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-submissions',
  standalone: true,
  imports: [DragDropModule, ReactiveFormsModule, DatePipe],
  templateUrl: './submissions.component.html',
  styleUrl: './submissions.component.css'
})
export class SubmissionsComponent implements OnInit {

  submissions: any[] = []
  leftSubmissions: any[] = []
  rightSubmissions: any[] = []

  formFilters = new FormGroup({
    "init_date": new FormControl(null),
    "end_date": new FormControl(null),
    "student_id": new FormControl(null),
    "name": new FormControl(null),
    "subject": new FormControl(null)
  })

  constructor(private api: ApiService, private resultsServ: ResultsService, private router: Router){}

  ngOnInit(): void {
    this.getSubmissions()
  }

  getSubmissions(){
    this.api.getSubmissions().subscribe((data) => {
      this.submissions = data
    })
  }

  onDrop(event: CdkDragDrop<any[]>) {
    console.log('Event:', event);
    console.log('Previous Container:', event.previousContainer);
    console.log('Current Container:', event.container);
    if((event.previousContainer.id == "cdk-drop-list-0" || event.previousContainer.id == "cdk-drop-list-0") && event.container.id == "cdk-drop-list-2"){
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
      return
    }

    console.log(event.container + " " + event.previousContainer)
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
      console.log("MOVING " + event.container.data)
    } else {
      copyArrayItem(event.previousContainer.data, event.container.data, event.previousIndex, event.currentIndex);
      console.log("COPYING " + event.previousContainer.data)
    }
  }

  compare(){
    let leftIds: number[] = []
    let rightIds: number[] = []

    this.leftSubmissions.forEach((sub) => {
      leftIds.push(sub.submission_id)
    })

    this.rightSubmissions.forEach((sub) => {
      rightIds.push(sub.submission_id)
    })

    let body = {
      ids_a: leftIds,
      ids_b: rightIds
    }

    this.api.compareSubmissions(body).subscribe((response) => {
      this.resultsServ.setResults(response)
      this.router.navigate(['/results']);
    })
  }

  onDelete(sub_id: any){
    this.api.deleteSubmission(sub_id).subscribe((response) => {
      console.log(response)
      this.getSubmissions()
    }, (error) => {
      console.log(error)
    })
  }

  onRemove(side: string, sub_id: any){
    if(side == "left"){
      const index = this.leftSubmissions.findIndex(submission => submission.submission_id === sub_id);
      console.log(index)
      if (index !== -1) {
          this.leftSubmissions.splice(index, 1);
      }
    }
    else{
      const index = this.rightSubmissions.findIndex(submission => submission.submission_id === sub_id);
      if (index !== -1) {
          this.rightSubmissions.splice(index, 1);
      }
    }
  }

  onEmpty(side: string){
    if(side == "left"){
      this.leftSubmissions.length = 0
    }
    else{
      this.rightSubmissions.length = 0
    }
  }

  addAll(side: string){
    if(side == "left"){
      this.submissions.forEach(submission => {
        if (!this.leftSubmissions.filter(leftSubmission => leftSubmission.submission_id === submission.submission_id).length) {
            this.leftSubmissions.push(submission);
        }
      });
    } else {
      this.submissions.forEach(submission => {
        if (!this.rightSubmissions.filter(rightSubmission => rightSubmission.submission_id === submission.submission_id).length) {
            this.rightSubmissions.push(submission);
        }
      });
    }
  }

  onSubmitFilters(){
    this.api.getFilteredSubmissions(this.formFilters.value).subscribe((response) => {
      this.submissions = response;
    }, (error) => {
      console.log(error)
    })
  }

  onClearFilters(){
    this.getSubmissions();
    this.formFilters.reset();
  }
  


}
