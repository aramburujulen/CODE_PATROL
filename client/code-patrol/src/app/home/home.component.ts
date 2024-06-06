import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import {FormGroup, FormControl, ReactiveFormsModule } from '@angular/forms';
import { ResultsService } from '../results.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

  file: any

  form = new FormGroup({
    "file": new FormControl(null)
  })
  
  constructor(private api: ApiService, private resultsServ: ResultsService, private router: Router ){}

  onFileChange(event: any) {
    if (event.target.files.length > 0) {
      this.file = event.target.files[0];
    }
  }

  onSubmit(){
    if(this.file){
      const formData = new FormData();
      formData.append('file', this.file);

      this.api.processSubmissionFolder(formData).subscribe((response) => {
        console.log('Upload success:', response);
        this.resultsServ.setResults(response)
        this.router.navigate(['/results']);
      }, error => {
        console.error('Upload error:', error);
      });
    }
  }


}
