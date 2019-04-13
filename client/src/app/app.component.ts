import { Component } from '@angular/core';

import { Store, Select } from '@ngxs/store';
import { DealerState } from './store/dealer.state';
import { Observable } from 'rxjs';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  @Select(DealerState.token)
  public token$: Observable<string>;

  title = 'client';
  isAuthed: boolean = false;

  constructor(private store: Store) {
    this.token$.subscribe((val) => {
      console.log(val);
      this.isAuthed = val.length > 0;
    });
  }
}
