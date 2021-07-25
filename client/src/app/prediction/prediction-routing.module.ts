import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PredictionBaseComponent } from './components/prediction-base/prediction-base.component';

const routes: Routes = [
  { path: '', component: PredictionBaseComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PredictionRoutingModule { }
