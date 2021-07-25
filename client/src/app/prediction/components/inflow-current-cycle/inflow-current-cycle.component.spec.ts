import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InflowCurrentCycleComponent } from './inflow-current-cycle.component';

describe('InflowCurrentCycleComponent', () => {
  let component: InflowCurrentCycleComponent;
  let fixture: ComponentFixture<InflowCurrentCycleComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InflowCurrentCycleComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InflowCurrentCycleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
