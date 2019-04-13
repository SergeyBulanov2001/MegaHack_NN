import { State, Action, StateContext, Selector } from '@ngxs/store';

export class SetToken {
	static readonly type = '[Dealer] Set Token';
	constructor(public token: string) { }
}

export class SetDealerId {
	static readonly type = '[Dealer] Set Id';
	constructor(public id: string) { }
}

// export class SetChats {
// 	static readonly type = '[Dealer] Set Token';
// 	constructor(public token: string) { }
// }

export interface DealerStateModel {
	token: string;
	id: string;
}

@State<DealerStateModel>({
	name: 'timetable',
	defaults: {
		token: '',
		id: ''
	}
})

export class DealerState {
	@Selector()
	static token(state: DealerStateModel) { return state.token; }

	@Selector()
	static dealerId(state: DealerStateModel) { return state.id; }

	@Action(SetToken)
	private setToken({ patchState }: StateContext<DealerStateModel>, { token }: SetToken) {
		patchState({
			token
		});
	}

	@Action(SetDealerId)
	private setDealerId({ patchState }: StateContext<DealerStateModel>, { id }: SetDealerId) {
		patchState({
			id
		});
	}

}
