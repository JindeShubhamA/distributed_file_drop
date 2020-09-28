import {authentication} from './authentication.reducer'
import {socketReducer} from "./socket.reducer";
import {combineReducers} from "redux";

function handleData(state = {data1: {}}, action) {
    switch (action.type) {
        case 'ApiGotData': return Object.assign({}, state, {data1: action.data});
        default: return state;
    }
}
const allReducers = combineReducers({
    authentication,
    socketReducer,
});

export default allReducers