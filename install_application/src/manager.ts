import { getRecoil, setRecoil } from "recoil-nexus"
import { deviceSetupPageUIAtom, deviceSetupStateAtom } from "./atoms";
import { AppDataController, appStateAtom } from "./store"


export const loginManager = {

    login: async (email: string, password: string) => {
        // make a request to login with the server

        // if failed login set login page ui to reflect this
        // store the resultant details in the manager
        const appDataController = await AppDataController.create();
        appDataController.appData = {
            ...getRecoil(appStateAtom),
            loggedIn: true,
            accountEmail: email,
            accountID: '',
            companyID: '',
            loginToken: '',
        };
        await appDataController.save();
    },

    logout: async () => {
        const appDataController = await AppDataController.create();
        appDataController.appData = {
            loggedIn: false,
            accountEmail: null,
            accountID: null,
            companyID: null,
            loginToken: null,
            registeredDevices: [],
        };
        await appDataController.save()
    },

}



interface SetupStateMessage {
    deviceID: string | null,
    setMaxDistance_mm: boolean,
    maxDistance_mm: number,
    setExpectedDistance_mm: boolean,
    expectedDistance_mm: number,
    currentDistance_mm: number | null,
    confirmedCorrectDistance_mm: boolean,
    setCoordinates: boolean,
    coordinates: [number, number] | null,
    confirmedCompletion: boolean,
}

const setup_server_address = 'http://192.168.4.1:80';

export const setupManager = {

    checkConnected: async () => {
        console.log('checking connection')
        try {
            // check connected
            var obj = {
                link: setup_server_address + '/',
                object: {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                    }
                }
            };
            console.log(obj.link);
            await fetch(obj.link, obj.object)
                .then(response => {
                    alert(response.status);
                    console.log(response)
                    if (response.status === 200) {
                        setRecoil(deviceSetupStateAtom,
                            {
                                connected: true,
                                deviceID: null,
                                setMaxDistance_mm: false,
                                maxDistance_mm: null,
                                setExpectedDistance_mm: false,
                                expectedDistance_mm: null,
                                currentDistance_mm: null,
                                confirmedCorrectDistance_mm: false,
                                coordinates: null,
                                setCoordinates: false,
                                confirmedCompletion: false,
                            }
                        );
                    } else {
                        setRecoil(deviceSetupStateAtom, {
                            ...getRecoil(deviceSetupStateAtom),
                            connected: false,
                        });
                    }
                    return;
                });
            await setupManager.getSetupState();
        } catch {
            console.log('caight')
            return;
        }
    },

    resetSetup: async () => {
        // send reset
        try{
        const obj = {
            link: setup_server_address + '/reset',
            object: {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                }
            }
        };
        await fetch(obj.link, obj.object);
        // request setup state
        await setupManager.getSetupState();
        setRecoil(deviceSetupPageUIAtom, {
            deviceConnectedToServer: false,
            confirmedDistance: false,
            completed: false,
        });
    }catch {}
    },

    getConnection: async () => {
        // request setup state
        try {
            const obj = {
                link: setup_server_address + '/connection',
                object: {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                    }
                }
            };
            const serverStateResponse = await fetch(obj.link, obj.object);
            setRecoil(deviceSetupPageUIAtom,
                {
                    ...getRecoil(deviceSetupPageUIAtom),
                    deviceConnectedToServer: serverStateResponse.status === 200
                });
            // set server UI to have good connection
        } catch {
            return;
        }
    },

    getSetupState: async () => {
        try {
            // request setup state
            const obj = {
                link: setup_server_address + '/setup_state',
                object: {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                    }
                }
            };
            const serverStateResponse = await fetch(obj.link, obj.object);
            if (serverStateResponse.status !== 200) {
                setRecoil(deviceSetupStateAtom,
                    {
                        connected: false,
                        deviceID: null,
                        setMaxDistance_mm: false,
                        maxDistance_mm: null,
                        setExpectedDistance_mm: false,
                        expectedDistance_mm: null,
                        currentDistance_mm: null,
                        confirmedCorrectDistance_mm: false,
                        coordinates: null,
                        setCoordinates: false,
                        confirmedCompletion: false,
                    }
                );
                return;
            }
            const serverState = JSON.parse(await serverStateResponse.json()) as SetupStateMessage;
            // store setup state
            setRecoil(deviceSetupStateAtom, {
                ...serverState,
                connected: true,
            });
        } catch {
            return;
        }
    },

    setMaxDistance: async (maxDistance_mm: number) => {
        try {
            // set the max distance on device
            var obj = {
                link: setup_server_address + '/max_distance_mm?' + new URLSearchParams({ max_distance_mm: maxDistance_mm.toString() }),
                object: {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                    }
                }
            };
            await fetch(obj.link, obj.object);
            // request state
            await setupManager.getSetupState();
        } catch {
            return;
        }
    },

    setExpectedDistance: async (expectedDistance_mm: number) => {
        try {
            // set expected distance on device
            var obj = {
                link: setup_server_address + '/expected_distance_mm?' + new URLSearchParams({ expected_distance_mm: expectedDistance_mm.toString() }),
                object: {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                    }
                }
            };
            await fetch(obj.link, obj.object);
            // request state
            await setupManager.getSetupState();
        } catch {
            return;
        }
    },

    getCurrentDistance: async () => {
        try {
            await setupManager.getSetupState();
        } catch {
            return;
        }
    },

    confirmDistanceCorrect: async () => {
        try {
            // request distance correct check
            // request state
            await setupManager.getSetupState();
        } catch {
            return;
        }
    },

    setCoordinates: async (coordinates: [number, number]) => {
        try {
            // send coordinates
            var obj = {
                link: setup_server_address + '/coordinates?' + new URLSearchParams({ coordinates: coordinates.toString() }),
                object: {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                    }
                }
            };
            await fetch(obj.link, obj.object);
            // TODO
            // set state
            await setupManager.getSetupState();
        } catch {
            return;
        }
    },

    confirmCompletion: async () => {
        try {
            // request device completion
            // TODO checks to make sure complete
            var obj = {
                link: setup_server_address + '/complete',
                object: {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                    }
                }
            };
            const serverStateResponse = await fetch(obj.link, obj.object);
            if (serverStateResponse.status !== 200) {
                // TODO set in ui unable to connect to the server
                return
            }
            // save device ID
            // set connected to false
            // modify UI state to go to completion page
            const deviceID = getRecoil(deviceSetupStateAtom).deviceID;
            const appDataController = await AppDataController.create();
            appDataController.appData.registeredDevices.push(deviceID!);
            await appDataController.save();
            setRecoil(deviceSetupStateAtom,
                {
                    connected: false,
                    deviceID: null,
                    setMaxDistance_mm: false,
                    maxDistance_mm: null,
                    setExpectedDistance_mm: false,
                    expectedDistance_mm: null,
                    currentDistance_mm: null,
                    confirmedCorrectDistance_mm: false,
                    coordinates: null,
                    setCoordinates: false,
                    confirmedCompletion: false,
                }
            );
            setRecoil(deviceSetupPageUIAtom, {
                ...getRecoil(deviceSetupPageUIAtom),
                completed: true,
            })
        } catch {
            return;
        }
    },

}
