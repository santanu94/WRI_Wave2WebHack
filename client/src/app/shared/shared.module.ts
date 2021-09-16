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
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatMomentDateModule } from '@angular/material-moment-adapter';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { GoogleMapsModule } from '@angular/google-maps';

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
    MatChipsModule,
    MatSelectModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatMomentDateModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    GoogleMapsModule
  ],
  exports: [
    HeaderComponent,
    FooterComponent,
    SideSectionComponent
  ]
})
export class SharedModule { }
// apiKey: 'AIzaSyDq2sN6NHHeBFWZpv64ZzYyE0Dbe-FycqU'
