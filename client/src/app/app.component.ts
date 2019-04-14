import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Личный кабинет';

  techMsis = '9957789408';

  date: string;
  msisdn: string;
  balance: string;
  tariff: string;
  dealer: number;

  stocks: Array<any>;
  userStocks: Array<any>;
  userStocksId: Array<number>;

  error: string;

  constructor(private http: HttpClient) {
    let date = new Date();
    let time = ('0' + date.getHours()).slice(-2) + ':' + ('0' + date.getMinutes()).slice(-2);
    this.date = time;

    // this.getInfo(this.techMsis);
    this.request()
  }

  request() {
    this.techMsis = window.prompt('Введите MSISDN для входа в личный кабинет');
    this.getInfo(this.techMsis);
  }

  getInfo(msisdn) {
    this.msisdn = msisdn.slice(0, 3) + ' ' + msisdn.slice(3, 6) + ' ' + msisdn.slice(6, 8) + ' ' + msisdn.slice(8, 10);
    this.http.get(`http://192.168.10.53:5005/user_request/${msisdn}`).subscribe((data: any) => {
      console.log(data);
      if (data.type === 'error') {
        alert('MSISDN введён неверно.');
        this.request();
      }

      this.balance = String(data.balance).replace(/\./, ',');
      this.tariff = data.tariff_name;
      this.dealer = data.dealer;
      this.getAllStocks();
    });
  }

  getAllStocks() {
    this.http.get(`http://192.168.10.53:5005/stock_request/${this.dealer}`).subscribe((data: any) => {
      console.log(data);
      this.stocks = data;
      this.getUserStocks();
    });
  }

  getUserStocks() {
    this.http.get(`http://192.168.10.53:5000/api/stock/get/${this.techMsis}`).subscribe((data: any) => {
      console.log(data);
      this.userStocksId = data;
      let newArr = [];

      if (data.type === 'success') {
        data.message.forEach(el => {
          this.stocks.forEach(element => {
            if (element.stock_id === el) {
              newArr.push({
                name: element.stock_name,
                id: el
              });
            }
          });
        });
      }
      console.log(newArr);
      this.userStocks = newArr;
    });
  }

  connect(id) {
    this.http.get(`http://192.168.10.53:5000/api/stock/add/${this.techMsis}&${this.dealer}&${id}`).subscribe((data: any) => {
      console.log(data);
      if (data.type === 'error') {
        this.error = data.message;
      } else {
        this.getUserStocks();
      }
    });
  }

  descTip(data) {
    let tip = '';

    if (data.calls) tip += `Пакет ${data.calls} звонков \n`;
    if (data.sms) tip += `Пакет ${data.sms} сообщений  \n`;
    if (data.internet) tip += `Трафик +${data.internet}  Гб\n`;
    if (data.sale) tip += `Скидка ${data.sale}% \n`;

    return tip;
  }
}
