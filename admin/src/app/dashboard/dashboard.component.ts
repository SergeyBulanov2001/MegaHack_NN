import { ToggleAddModal } from './../store/dealer.state';
import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Store, Select } from '@ngxs/store';
import { DealerState, SetToken } from '../store/dealer.state';
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

  stocks: Array<any>;
  orders: Array<any>;

  constructor(private http: HttpClient, private store: Store) {
    this.dealerId$.subscribe((val) => {
      console.log(val);
      this.dealerId = val;
    });

    this.getStocks();
    this.getOrders();
  }

  getStocks() {
    const token = this.store.selectSnapshot(DealerState.token);

    this.http.get(`http://95.79.50.190:5001/${token}/stock_request`).subscribe((data: any) => {
      console.log(data);
      data.sort((a, b) => {
        if (a.status === 'available' && b.status === 'closed') {
          return -1;
        }
        if (a.status === 'closed' && b.status === 'available') {
          return 1;
        }

        return 0;
      });

      this.stocks = data;
    });
  }

  getOrders() {
    const token = this.store.selectSnapshot(DealerState.token);

    this.http.get(`http://95.79.50.190:5001/${token}/orders`).subscribe((data: any) => {
      console.log(data);

      this.orders = data;
    });
  }

  ngOnInit() {
  }

  logout() {
    this.store.dispatch(new SetToken(''));
  }

  openAddStock() {
    this.store.dispatch(new ToggleAddModal());
  }

  close(id) {
    const token = this.store.selectSnapshot(DealerState.token);

    this.http.get(`http://95.79.50.190:5001/${token}/closing_stock/${id}`).subscribe((data: any) => {
      console.log(data);
      this.getStocks();
    });
  }

}
