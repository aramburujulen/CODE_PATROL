import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ResultsComponent } from './results/results.component';
import { StudentsComponent } from './students/students.component';
import { NewSubmissionComponent } from './new-submission/new-submission.component';
import { SubmissionsComponent } from './submissions/submissions.component';

export const routes: Routes = [
    {path:"home", component:HomeComponent},
    {path:"results", component:ResultsComponent},
    {path:"students", component:StudentsComponent},
    {path:"newSubmission", component:NewSubmissionComponent},
    {path:"submissions", component:SubmissionsComponent}
];
