import { Component, OnInit } from '@angular/core';

import { Store, Select } from '@ngxs/store';
import { DealerState } from '../store/dealer.state';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  @Select(DealerState.dealerId)
  public dealerId$: Observable<string>;

  dealerId: string;

  constructor(private store: Store) {
    this.dealerId$.subscribe((val) => {
      console.log(val);
      this.dealerId = val;
    });
  }

  ngOnInit() {
  }

}
