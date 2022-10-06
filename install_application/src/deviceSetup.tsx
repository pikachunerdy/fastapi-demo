import { useState } from 'react';
import { Alert, Button, StyleSheet, Text, TextInput, View, Dimensions } from 'react-native';
import { useRecoilValue } from "recoil"
import { getRecoil, setRecoil } from 'recoil-nexus';
import { deviceSetupPageUIAtom, deviceSetupStateAtom, pageStateAtom } from "./atoms"
import { setupManager } from './manager';

// Widgets

let ScreenHeight = Dimensions.get("window").height;
let ScreenWidth = Dimensions.get("window").width;

const topBarStyles = StyleSheet.create({
    container: {
        alignSelf: 'stretch',
        height: 52,
        flexDirection: 'row', // row
        backgroundColor: 'blue',
        alignItems: 'center',
        justifyContent: 'space-between', // center, space-around
        paddingLeft: 10,
        paddingRight: 10,
        position: 'absolute',
        width: '100%',
        top: 30,
        zIndex: 5,
    }
});

const TopBar = () => {

    const exitAlert = () =>
        Alert.alert(
            "Exit",
            "Are you sure you want to exit",
            [
                {
                    text: "Cancel",
                    onPress: () => { },
                    style: "cancel"
                },
                { text: "OK", onPress: async () => { setRecoil(pageStateAtom, { ...getRecoil(pageStateAtom), deviceSetupPage: false }); } }
            ]
        );

    const resetAlert = () =>
        Alert.alert(
            "Restart",
            "Are you sure you want to restart the setup",
            [
                {
                    text: "Cancel",
                    onPress: () => { },
                    style: "cancel"
                },
                {
                    text: "OK", onPress: async () => {
                        await setupManager.resetSetup()
                    }
                }
            ]
        );

    return (
        <View style={topBarStyles.container}>
            <Button title='Exit' onPress={exitAlert}></Button>
            {/* <Button title='middle'></Button> */}
            <Button title='Restart' onPress={resetAlert}></Button>
        </View>
    );
}


const pageStyles = StyleSheet.create({
    container: {
        height: '100%',
        width: ScreenWidth,
        position: 'absolute',
        alignContent: 'center',
        flexDirection: 'column',
        justifyContent: 'center',
        textAlign: 'center',
        // top : '50%',
    }
});

// Pages

const CompletedPage = () => {

    const exitAlert = () =>
        Alert.alert(
            "Exit",
            "Are you sure you want to exit",
            [
                {
                    text: "Cancel",
                    onPress: () => { },
                    style: "cancel"
                },
                { text: "OK", onPress: async () => { setRecoil(pageStateAtom, { ...getRecoil(pageStateAtom), deviceSetupPage: false }); } }
            ]
        );

    return <View style={{
        position: 'absolute',
        height: ScreenHeight,
        width: ScreenWidth,
        zIndex: 5,
    }}>
        <TopBar></TopBar>
        <View style={pageStyles.container}>
            <Text style={{
                width: '100%',
                textAlign: 'center',
                marginBottom: 20
            }}>Device Setup Complete</Text>
            <View style={{
                height: 40,
                width: '40%',
                marginLeft: '30%',
                marginRight: '30%',
            }}><Button title='Exit' onPress={exitAlert}></Button></View>
        </View>
    </View>
}

const ConfirmCompletionPage = () => {
    const deviceSetupState = useRecoilValue(deviceSetupStateAtom);

    return <View style={{
        position: 'absolute',
        height: ScreenHeight,
        width: ScreenWidth,
        zIndex: 5,
    }}>
        <TopBar></TopBar>
        <View style={pageStyles.container}>
            <Text style={{
                width: '100%',
                textAlign: 'center',
                marginBottom: 20
            }}>Confirm Completion of Setup</Text>
            <View style={{
                height: 40,
                width: '40%',
                marginLeft: '30%',
                marginRight: '30%',
            }}>
                <Text style={{
                    width: '100%',
                    textAlign: 'center',
                    marginBottom: 20,
                    fontWeight: 'bold',
                }}>Maximum Distance: {deviceSetupState.maxDistance_mm}</Text>

                <Text style={{
                    width: '100%',
                    textAlign: 'center',
                    marginBottom: 20,
                    fontWeight: 'bold',
                }}>Expected Distance: {deviceSetupState.expectedDistance_mm}</Text>

                <Text style={{
                    width: '100%',
                    textAlign: 'center',
                    marginBottom: 20,
                    fontWeight: 'bold',
                }}>Current Distance: {deviceSetupState.currentDistance_mm}</Text>

                <Button title='Confirm Setup Correct' onPress={
                    async () => {
                        await setupManager.confirmCompletion();
                    }
                }></Button></View>
        </View>
    </View>
}

const CoordinatesPage = () => {

    const [latitudeText, setLatitudeText] = useState('');
    const [longitudeText, setLongitudeText] = useState('');
    const latitude = <TextInput style={styles.input}
        maxLength={40}
        editable
        keyboardType='numeric'
        placeholder='latitude'
        onChangeText={text => setLatitudeText(text)}
        value={latitudeText}></TextInput>;

    const longitude = <TextInput style={styles.input}
        maxLength={40}
        editable
        keyboardType='numeric'
        placeholder='longitude'
        onChangeText={text => setLongitudeText(text)}
        value={longitudeText}></TextInput>;


    return <View style={{
        position: 'absolute',
        height: ScreenHeight,
        width: ScreenWidth,
        zIndex: 5,
    }}>
        <TopBar></TopBar>
        <View style={pageStyles.container}>
            <Text style={{
                width: '100%',
                textAlign: 'center',
                marginBottom: 20,
                padding: 20,
            }}>Please enter latitude and longitude coordinates of manhole</Text>
            <View style={{
                alignItems: 'center',
                alignContent: 'center',
                alignSelf: 'center',
                width: 200,
                height: 60,
            }}>
                {latitude}
                {longitude}
                <Button title='Confirm Coordinates' onPress={async () => {
                    let lat = parseInt(latitudeText);
                    let long = parseInt(longitudeText);
                    if (isNaN(lat) || isNaN(long)) {
                        alert('Not an integer');
                    } else {
                        await setupManager.setCoordinates([lat, long]);
                    }
                }}></Button></View>
        </View>
    </View>
}

const ConfirmDistanceCorrectPage = () => {

    const deviceSetupState = useRecoilValue(deviceSetupStateAtom);
    return <View style={{
        position: 'absolute',
        height: ScreenHeight,
        width: ScreenWidth,
        zIndex: 5,
    }}>
        <TopBar></TopBar>
        <View style={pageStyles.container}>

            <Text style={{
                width: '100%',
                textAlign: 'center',
                marginBottom: 20
            }}>Ensure the sensor distance is inline with the expected distance</Text>

            <Text style={{
                width: '100%',
                textAlign: 'center',
                marginBottom: 20,
                fontWeight: 'bold',
            }}>Expected Distance: {deviceSetupState.expectedDistance_mm}</Text>

            <Text style={{
                width: '100%',
                textAlign: 'center',
                marginBottom: 20,
                fontWeight: 'bold',
            }}>Current Distance: {deviceSetupState.currentDistance_mm}</Text>

            {
                deviceSetupState.confirmedCorrectDistance_mm ?
                    // true ?
                    <View style={{
                        height: 40,
                        width: '40%',
                        marginLeft: '30%',
                        marginRight: '30%',
                    }}>
                        <Button title='Continue' onPress={setupManager.confirmDistanceCorrect}></Button>
                    </View> : <></>
            }


        </View>
    </View>
}

const ExpectedDistancePage = () => {

    const [distanceText, setDistanceText] = useState('');
    const email = <TextInput style={styles.input}
        maxLength={40}
        editable
        keyboardType='numeric'
        placeholder='current distance in mm'
        onChangeText={text => setDistanceText(text)}
        value={distanceText}></TextInput>;

    return <View style={{
        position: 'absolute',
        height: ScreenHeight,
        width: ScreenWidth,
        zIndex: 5,
    }}>
        <TopBar></TopBar>
        <View style={pageStyles.container}>
            <Text style={{
                width: '100%',
                textAlign: 'center',
                marginBottom: 20,
                padding: 10
            }}>Input the distance from the sensor to the current water level in mm</Text>
            <View style={{ width: '100%' }}>
                <View style={{
                    alignItems: 'center',
                    alignContent: 'center',
                    alignSelf: 'center',
                    width: 200,
                    height: 60,
                }}>
                    {email}
                    <Button title='Confirm Distance' onPress={async () => {
                        let x = parseInt(distanceText);
                        if (isNaN(x)) {
                            alert('Not an integer');
                        } else {
                            await setupManager.setExpectedDistance(x);
                        }
                    }}></Button></View>
            </View>
        </View>
    </View>
}

const MaxDistancePage = () => {

    const [distanceText, setDistanceText] = useState('');
    const email = <TextInput style={styles.input}
        maxLength={40}
        editable
        keyboardType='numeric'
        placeholder='maximum distance in mm'
        onChangeText={text => setDistanceText(text)}
        value={distanceText}></TextInput>;

    return <View style={{
        position: 'absolute',
        height: ScreenHeight,
        width: ScreenWidth,
        zIndex: 5,
    }}>
        <TopBar></TopBar>
        <View style={pageStyles.container}>
            <Text style={{
                width: '100%',
                textAlign: 'center',
                marginBottom: 20,
                padding: 10
            }}>Input the total height (mm) of the manhole from the base to the sensor</Text>
            <View style={{ width: '100%' }}>
                <View style={{
                    alignItems: 'center',
                    alignContent: 'center',
                    alignSelf: 'center',
                    width: 200,
                    height: 60,
                }}>
                    {email}
                    <Button title='Confirm Distance' onPress={async () => {
                        let x = parseInt(distanceText);
                        if (isNaN(x)) {
                            alert('Not an integer');
                        } else {
                            await setupManager.setMaxDistance(x);
                        }
                    }}></Button></View>
            </View>
        </View>
    </View>
}

const ConfirmDeviceServerConnectionPage = () => {

    return <View style={{
        position: 'absolute',
        height: ScreenHeight,
        width: ScreenWidth,
        zIndex: 5,
    }}>
        <TopBar></TopBar>
        <View style={pageStyles.container}>
            <Text style={{
                width: '100%',
                textAlign: 'center',
                marginBottom: 20
            }}>Ensure device able to connect to server</Text>
            <View style={{ width: '100%' }}>
                <View style={{
                    alignItems: 'center',
                    alignContent: 'center',
                    alignSelf: 'center',
                    width: 200,
                    height: 60,
                }}><Button title='Check Connection' onPress={setupManager.getConnection}></Button></View>
            </View>
        </View>
    </View>
}

const CheckConnectionPage = () => {

    return <View style={{
        position: 'absolute',
        height: ScreenHeight,
        width: ScreenWidth,
        zIndex: 5,
    }}>
        <TopBar></TopBar>
        <View style={pageStyles.container}>
            <Text style={{
                width: '100%',
                textAlign: 'center',
                marginBottom: 20
            }}>Please connect to device wifi</Text>
            <View style={{
                height: 40,
                width: '40%',
                marginLeft: '30%',
                marginRight: '30%',
            }}><Button title='Check Wifi' onPress={setupManager.checkConnected}></Button></View>
        </View>
    </View>
}

export const DeviceSetupPage = () => {
    const deviceSetupPageUIState = useRecoilValue(deviceSetupPageUIAtom);
    const deviceSetupState = useRecoilValue(deviceSetupStateAtom);

    // return <CompletedPage></CompletedPage>;

    if (!deviceSetupState.connected) {
        return <CheckConnectionPage></CheckConnectionPage>;
    }

    if (!deviceSetupPageUIState.deviceConnectedToServer) {
        return <ConfirmDeviceServerConnectionPage></ConfirmDeviceServerConnectionPage>;
    }

    if (!deviceSetupState.setMaxDistance_mm) {
        return <MaxDistancePage></MaxDistancePage>;
    }

    if (!deviceSetupState.setExpectedDistance_mm) {
        return <ExpectedDistancePage></ExpectedDistancePage>;
    }

    if (!deviceSetupState.confirmedCorrectDistance_mm ||
        deviceSetupPageUIState.confirmedDistance) {
        return <ConfirmDistanceCorrectPage></ConfirmDistanceCorrectPage>;
    }

    if (!deviceSetupState.setCoordinates) {
        return <CoordinatesPage></CoordinatesPage>;
    }

    if (!deviceSetupState.confirmedCompletion) {
        return <ConfirmCompletionPage></ConfirmCompletionPage>;
    }

    if (deviceSetupState.confirmedCompletion && deviceSetupPageUIState.completed) {
        return <CompletedPage></CompletedPage>;
    }

    return <CheckConnectionPage></CheckConnectionPage>;
}



const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: 'white',
        alignItems: 'center',
        justifyContent: 'center',
    },
    input: {
        borderColor: 'black',
        backgroundColor: 'white',
        borderWidth: 1,
        height: 40,
        margin: 12,
        padding: 5,
        width: 250,
        borderRadius: 10
    },
    separator: {
        marginVertical: 8,
        borderBottomColor: '#737373',
        borderBottomWidth: StyleSheet.hairlineWidth,
    },
});
