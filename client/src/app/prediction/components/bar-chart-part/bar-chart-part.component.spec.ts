import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BarChartPartComponent } from './bar-chart-part.component';

describe('BarChartPartComponent', () => {
  let component: BarChartPartComponent;
  let fixture: ComponentFixture<BarChartPartComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BarChartPartComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BarChartPartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
