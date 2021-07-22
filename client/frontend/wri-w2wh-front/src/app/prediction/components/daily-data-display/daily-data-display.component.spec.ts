import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DailyDataDisplayComponent } from './daily-data-display.component';

describe('DailyDataDisplayComponent', () => {
  let component: DailyDataDisplayComponent;
  let fixture: ComponentFixture<DailyDataDisplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DailyDataDisplayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DailyDataDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
