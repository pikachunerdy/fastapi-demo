import {
    atom,
} from 'recoil';
import { company_manager, device_list_manager } from './managers';

export const filterState = atom({
    key: 'filterState',
    default : {
        pinned : false,
        searchText : '',
        labels : []
    },
    effects: [
        () => {
            // device_list_manager.get_device_list();
        },
      ],
})

export const mapState = atom({
    key: 'mapState',
    default : {
        requested_centre : [0,0],
        required_update : false
    }
})

export const deviceListState = atom({
    key: 'deviceListState', // unique ID (with respect to other atoms/selectors)
    default: {
        devices : [],
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

export const companyState = atom({
    'key' : 'companyState',
    default : {
        labels : [],
    }
})

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


export const navStateAtom = atom({
    key : 'navState',
    default : 'device-metrics'
})
