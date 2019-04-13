import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Store } from '@ngxs/store';
import { SetToken, SetDealerId } from '../store/dealer.state';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent implements OnInit {
  id: string;
  password: string;
  error: string;

  constructor(private http: HttpClient, private store: Store) {
  }

  ngOnInit() {
  }

  login() {
    if (this.id.length === 0) { this.error = 'Введите ID'; return; };
    if (this.password.length === 0) { this.error = 'Введите пароль'; return; };

    this.http.get(`http://192.168.10.53:5000/authorization/${this.id}&${this.password}`).subscribe((data: any) => {
      console.log(data);
      if (data.type === 'success') {
        this.store.dispatch(new SetToken(data.token));
        this.store.dispatch(new SetDealerId(this.id));
      } else if (data.type === 'error') {
        this.error = data.message;
      }
    });
  }

}
