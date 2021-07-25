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
import { DailyDataDisplayComponent } from './components/daily-data-display/daily-data-display.component';
import { GaugeModule } from 'angular-gauge';
import { BarChartPartComponent } from './components/bar-chart-part/bar-chart-part.component';
import { MatTabsModule } from '@angular/material/tabs';
import { SharedModule } from '../shared/shared.module';


@NgModule({
  declarations: [
    PredictionBaseComponent,
    InflowCurrentCycleComponent,
    OutflowComponent,
    InflowTrendsComponent,
    ViewExpandedDataComponent,
    DailyDataDisplayComponent,
    BarChartPartComponent
  ],
  imports: [
    CommonModule,
    PredictionRoutingModule,
    MatCardModule,
    MatIconModule,
    MatDialogModule,
    ChartsModule,
    GaugeModule.forRoot(),
    SharedModule,
    MatTabsModule
  ],
  entryComponents: [ViewExpandedDataComponent]
})
export class PredictionModule { }
