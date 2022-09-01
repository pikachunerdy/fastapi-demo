import {
    atom,
} from 'recoil';

export const deviceListState = atom({
    key: 'deviceListState', // unique ID (with respect to other atoms/selectors)
    default: {
        devices : []
    }, // default value (aka initial value)
});

export const accountListState = atom({
    key: 'accountListState', // unique ID (with respect to other atoms/selectors)
    default: {
        accounts : []
    }, // default value (aka initial value)
});

export const selectedDeviceState = atom({
    key : 'selectedDeviceState',
    default : {

    },
});

export const selectedAccountState = atom({
    key : 'selectedAccountState',
    default : {
        id : null
    },
});

export const authState = atom({
    key : 'authState',
    default : {
        token : '',
        validToken : false,
        showInvalidCredWarning : false,
    }
});

export const panelSizes = atom({
    key : 'panelSizes',
    default : {
        hTop : 0,
        vLeft : 0,
        vRight : 0
    }
})