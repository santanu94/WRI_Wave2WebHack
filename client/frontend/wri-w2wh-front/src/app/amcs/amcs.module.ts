import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AmcsRoutingModule } from './amcs-routing.module';
import { PlaceholderComponent } from './components/placeholder/placeholder.component';


@NgModule({
  declarations: [PlaceholderComponent],
  imports: [
    CommonModule,
    AmcsRoutingModule
  ]
})
export class AmcsModule { }
