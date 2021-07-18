import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { SideSectionComponent } from './components/side-section/side-section.component';

import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatSelectModule } from '@angular/material/select';
import { GaugeModule } from 'angular-gauge';

@NgModule({
  declarations: [
    HeaderComponent,
    FooterComponent,
    SideSectionComponent
  ],
  imports: [
    CommonModule,
    MatToolbarModule,
    MatIconModule,
    MatCardModule,
    GaugeModule.forRoot(),
    MatChipsModule,
    MatSelectModule
  ],
  exports: [
    HeaderComponent,
    FooterComponent,
    SideSectionComponent
  ]
})
export class SharedModule { }
