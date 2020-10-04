import {userConstants} from "../_constants/user.constants";
import {socketConstants} from "../_constants/socket.constants";
import {sidebarConstants} from "../_constants/sidebar.constants";

export const callLogin = (UID) => {
    return{
        type: userConstants.LOGIN_REQUEST,
        UID: UID,
    }
};
export const setLogin = (UID, token) => {
    return{
        type: userConstants.LOGIN_SUCCESS,
        UID: UID,
        token: token
    }
};
export const callRegister = (UID) => {
    return{
        type: userConstants.REGISTER_REQUEST,
        UID: UID,
    }
};
export const setLoginfail = () => {
    return{
        type: userConstants.LOGIN_FAILURE,
        UID: '',
        token: ''
    }
};
export const createSocket = () => {
    return{
        type: socketConstants.SOCKET_REQUEST,
    }
};
export const successSocket = (host) => {
    return{
        type: socketConstants.SOCKET_SUCCESS,
        payload: host,
    }
};
export const failedSocket = () => {
    return{
        type: socketConstants.SOCKET_FAILURE,
    }
};
export const disconnectSocket = () => {
    return{
        type: socketConstants.SOCKET_DISCONNECT,
    }
};
export const sendSocketMessage = (ev, message) => {
    return{
        type: socketConstants.SEND_WEBSOCKET_MESSAGE,
        event: ev,
        payload: message,
    }
};
export const receiveSocketMessage = (ev, message) => {
    return{
        type: socketConstants.SOCKET_MESSAGE_RECEIVE,
        event: ev,
        payload: message,
    }
};
export const storeSocketMessage = (message) => {
    return{
        type: socketConstants.SOCKET_MESSAGE_STORE,
        payload: message,
    }
};
export const uploadSocketFile = (file) => {
    return{
        type: socketConstants.SOCKET_UPLOAD,
        file: file,
    }
};

export const toggleSidebarAction = (status) => {
    return{
        type: sidebarConstants.SIDEBAR_TOGGLE,
        payload: status,
    }
};