import {socketConstants} from "../_constants/socket.constants";

const url = "http://localhost:4000/";

export default function socketMiddleware(newSock) {
    let socket = newSock;

    return storeAPI => next => action => {
        switch(action.type) {
            case socketConstants.SOCKET_REQUEST : {
                socket.connect();
                socket.connected();
                break;
            }
            case socketConstants.SEND_WEBSOCKET_MESSAGE: {
                socket.send(action.event, action.payload);
                break;
            }
            case socketConstants.SOCKET_MESSAGE_RECEIVE: {
                socket.on(action.event, action.payload);
                break;
            }
        }

        return next(action);
    }
};

// export default socketMiddleware