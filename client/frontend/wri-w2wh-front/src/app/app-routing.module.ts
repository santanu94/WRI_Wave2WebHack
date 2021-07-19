import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';


const routes: Routes = [
  { path: '', redirectTo: 'prediction', pathMatch: 'full' },
  { path: 'prediction',
    loadChildren: () =>
      import(
        './prediction/prediction.module'
      ).then((m) => m.PredictionModule)
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
