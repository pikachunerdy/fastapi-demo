import * as SecureStore from 'expo-secure-store';
import {
    atom,
} from 'recoil';
import { getRecoil, setRecoil } from "recoil-nexus";


interface AppData {
    loggedIn: boolean,
    accountEmail: string | null,
    accountID: string | null,
    companyID: string | null,
    loginToken: string | null,
    registeredDevices: string[],
}

//shouldn't have recoil changed by anything other than app storage
export const appStateAtom = atom<AppData>({
    key: 'appStateAtom', // unique ID (with respect to other atoms/selectors)
    default: {
        loggedIn: false,
        accountEmail: null,
        accountID: null,
        companyID: null,
        loginToken: null,
        registeredDevices: []
    }
});

export class AppDataController {

    private static key: string = 'AppData';
    private static self: AppDataController | null = null;
    public appData: AppData;

    private constructor(appData: AppData | null) {
        if (appData) {
            this.appData = appData;
        }
        else {
            this.appData = {
                loggedIn: false,
                accountEmail: null,
                accountID: null,
                companyID: null,
                loginToken: null,
                registeredDevices: []
            };
        }
    }

    static async create(): Promise<AppDataController> {
        if (this.self !== null) {
            return this.self;
        }
        let result = await SecureStore.getItemAsync(AppDataController.key);
        this.self = new AppDataController(result !== null ? JSON.parse(result) : null);
        setRecoil(appStateAtom, this.self.appData);
        return this.self;
    }

    async save(): Promise<void> {
        setRecoil(appStateAtom, this.appData);
        await SecureStore.setItemAsync(AppDataController.key, JSON.stringify(this.appData));
    }

}

interface PageState {
    deviceSetupPage : boolean
}

export const pageStateAtom = atom<PageState>({
    key: 'pageStateAtom', // unique ID (with respect to other atoms/selectors)
    default: {
        deviceSetupPage : false,
    }
});
