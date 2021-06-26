import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PredictionRoutingModule } from './prediction-routing.module';
import { PredictionBaseComponent } from './components/prediction-base/prediction-base.component';
import { InflowCurrentCycleComponent } from './components/inflow-current-cycle/inflow-current-cycle.component';
import { OutflowComponent } from './components/outflow/outflow.component';
import { InflowTrendsComponent } from './components/inflow-trends/inflow-trends.component';
import { MatCardModule } from '@angular/material/card';


@NgModule({
  declarations: [
    PredictionBaseComponent,
    InflowCurrentCycleComponent,
    OutflowComponent,
    InflowTrendsComponent
  ],
  imports: [
    CommonModule,
    PredictionRoutingModule,
    MatCardModule
  ]
})
export class PredictionModule { }
