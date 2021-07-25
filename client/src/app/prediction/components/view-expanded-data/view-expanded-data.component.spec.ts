import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewExpandedDataComponent } from './view-expanded-data.component';

describe('ViewExpandedDataComponent', () => {
  let component: ViewExpandedDataComponent;
  let fixture: ComponentFixture<ViewExpandedDataComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ViewExpandedDataComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ViewExpandedDataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
