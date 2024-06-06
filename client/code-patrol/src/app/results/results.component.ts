import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { ResultsService } from '../results.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-results',
  standalone: true,
  imports: [],
  templateUrl: './results.component.html',
  styleUrl: './results.component.css'
})
export class ResultsComponent implements OnInit {

  results: any[] = []

  constructor(private api: ApiService, private resultsServ: ResultsService) {}

  ngOnInit(): void {
    this.results = this.resultsServ.getResults()
    
    this.results.forEach((result) => result.isExpanded = false)
  }

  expandResult(result: any){
    result.isExpanded = !result.isExpanded
  }


}
