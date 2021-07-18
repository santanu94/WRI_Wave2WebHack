import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PredictionRoutingModule } from './prediction-routing.module';
import { PredictionBaseComponent } from './components/prediction-base/prediction-base.component';
import { InflowCurrentCycleComponent } from './components/inflow-current-cycle/inflow-current-cycle.component';
import { OutflowComponent } from './components/outflow/outflow.component';
import { InflowTrendsComponent } from './components/inflow-trends/inflow-trends.component';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatDialogModule } from '@angular/material/dialog';
import { ChartsModule } from 'ng2-charts';
import { ViewExpandedDataComponent } from './components/view-expanded-data/view-expanded-data.component';


@NgModule({
  declarations: [
    PredictionBaseComponent,
    InflowCurrentCycleComponent,
    OutflowComponent,
    InflowTrendsComponent,
    ViewExpandedDataComponent
  ],
  imports: [
    CommonModule,
    PredictionRoutingModule,
    MatCardModule,
    MatIconModule,
    MatDialogModule,
    ChartsModule
  ],
  entryComponents: [ViewExpandedDataComponent]
})
export class PredictionModule { }
