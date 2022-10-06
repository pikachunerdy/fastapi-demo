import {
    atom,
} from 'recoil';


interface deviceSetupState {
    connected : boolean,
    deviceID : string | null,
    setMaxDistance_mm : boolean,
    maxDistance_mm : number | null,
    setExpectedDistance_mm : boolean,
    expectedDistance_mm : number | null,
    currentDistance_mm : number | null,
    confirmedCorrectDistance_mm : boolean,
    setCoordinates : boolean,
    coordinates : [number,number] | null,
    confirmedCompletion : boolean,
}

export const deviceSetupStateAtom = atom<deviceSetupState>({
    key: 'deviceSetupStateAtom', // unique ID (with respect to other atoms/selectors)
    default: {
        connected : false,
        deviceID : null,
        setMaxDistance_mm : false,
        maxDistance_mm : null,
        setExpectedDistance_mm : false,
        expectedDistance_mm : null,
        currentDistance_mm : null,
        confirmedCorrectDistance_mm : false,
        setCoordinates : false,
        coordinates : null,
        confirmedCompletion : false,
    }
});

interface DeviceSetupPageUI {
    deviceConnectedToServer : boolean,
    confirmedDistance : boolean,
    completed : boolean,
}

export const deviceSetupPageUIAtom = atom<DeviceSetupPageUI>({
    key: 'deviceSetupPageUIAtom', // unique ID (with respect to other atoms/selectors)
    default: {
        deviceConnectedToServer : false,
        confirmedDistance : false,
        completed : false,
    }
});


interface loginPageUIState {
    failedPassword : boolean,
}

export const loginPageUIStateAtom = atom<loginPageUIState>({
    key: 'loginPageUIStateAtom', // unique ID (with respect to other atoms/selectors)
    default: {
        failedPassword : true,
    }
});


interface PageState {
    deviceSetupPage : boolean
}

export const pageStateAtom = atom<PageState>({
    key: 'pageStateAtom', // unique ID (with respect to other atoms/selectors)
    default: {
        deviceSetupPage : false,
    }
});
