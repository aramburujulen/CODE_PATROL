import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ResultsService {
  private results: any[] = []

  constructor() { }

  setResults(results: any): void {
    this.results = results;
  }

  getResults(): any {
    return this.results;
  }
}
