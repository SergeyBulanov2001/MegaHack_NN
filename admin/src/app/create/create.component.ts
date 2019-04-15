import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Store, Select } from '@ngxs/store';
import { DealerState, ToggleAddModal, SetToken } from '../store/dealer.state';
import { Observable } from 'rxjs';
@Component({
  selector: 'app-create',
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.css']
})
export class CreateComponent implements OnInit {
  @Select(DealerState.dealerId)
  public dealerId$: Observable<string>;
  dealerId: string;

  tariffs: Array<any>;

  error: string;

  name: string;
  desc: string;

  isCalls: boolean = false;
  calls: string;
  isSMS: boolean = false;
  sms: string;
  isInternet: boolean = false;
  internet: string;
  isSale: boolean = false;
  sale: string;

  tariff: string = "1";
  isBalance: boolean = false;
  balance: string;
  isDate: boolean = false;
  date: string;

  constructor(private http: HttpClient, private store: Store) {
    this.dealerId$.subscribe((val) => {
      console.log(val);
      this.dealerId = val;
    });
  }

  ngOnInit() {
    const token = this.store.selectSnapshot(DealerState.token);

    this.http.get(`http://95.79.50.190:5001/${token}/tariffs`).subscribe((data: any) => {
      console.log(data);
      this.tariffs = data;
      // if (data.type == "success") {
      //   // TODO Вывод
      //   this.back();
      // }
    });
  }

  back() {
    this.store.dispatch(new ToggleAddModal());
  }

  create() {
    let services: any;
    services = {};

    if (!this.name) {
      this.error = "Введите имя акции";
      return;
    }

    if (!this.desc) {
      this.error = "Введите описание акции";
      return;
    }

    if (!this.isCalls && !this.isSMS && !this.isInternet && !this.isSale) {
      this.error = "Выберите подключаемые услуги";
      return;
    }

    if (this.isCalls) {
      if (!this.calls || this.calls.length === 0) {
        this.error = "Введите подключённые услуги";
        return;
      }
      services.calls = parseInt(this.calls);
    }
    if (this.isSMS) {
      if (!this.sms || this.sms.length === 0) {
        this.error = "Введите подключённые услуги";
        return;
      }
      services.sms = parseInt(this.sms);
    }
    if (this.isInternet) {
      if (!this.internet || this.internet.length === 0) {
        this.error = "Введите подключённые услуги";
        return;
      }
      services.internet = parseInt(this.internet);
    }
    if (this.isSale) {
      if (!this.sale || this.sale.length === 0) {
        this.error = "Введите подключённые услуги";
        return;
      }
      if (parseInt(this.sale) > 100) {
        this.error = "Скидка не может быть больше 100%";
        return;
      }
      services.sale = parseInt(this.sale);
    }

    let conditions: any;
    conditions = {};

    conditions.tariff_id = parseInt(this.tariff);
    if (this.isBalance) conditions.balance = parseInt(this.balance);
    if (this.isDate) conditions.lifetime = this.date;

    const token = this.store.selectSnapshot(DealerState.token);

    this.http.get(`http://95.79.50.190:5001/${token}/stock/${this.name}&${JSON.stringify(services)}&${JSON.stringify(conditions)}&${this.desc}`).subscribe((data: any) => {
      console.log(data);
      if (data.type == "success") {
        // TODO Вывод акций
        this.back();
      }
    });
  }

  logout() {
    this.store.dispatch(new SetToken(''));
  }

}
