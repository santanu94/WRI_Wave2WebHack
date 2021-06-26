import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InflowTrendsComponent } from './inflow-trends.component';

describe('InflowTrendsComponent', () => {
  let component: InflowTrendsComponent;
  let fixture: ComponentFixture<InflowTrendsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InflowTrendsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InflowTrendsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
