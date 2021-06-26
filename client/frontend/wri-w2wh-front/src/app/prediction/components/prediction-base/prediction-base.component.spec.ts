import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictionBaseComponent } from './prediction-base.component';

describe('PredictionBaseComponent', () => {
  let component: PredictionBaseComponent;
  let fixture: ComponentFixture<PredictionBaseComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PredictionBaseComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PredictionBaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
