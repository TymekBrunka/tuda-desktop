import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { TheComponent } from './the/the.component';
import { PnfComponent } from './pnf/pnf.component';

export const routes: Routes = [
  {path: "", component: HomeComponent},
  {path: "app", component: TheComponent},
  {path: "**", component: PnfComponent},
];
