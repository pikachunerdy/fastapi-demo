import { StatusBar } from 'expo-status-bar';
import { useState } from 'react';
import { Alert, Button, StyleSheet, Text, TextInput, View } from 'react-native';
import { RecoilRoot, useRecoilState, useRecoilValue } from 'recoil';
import RecoilNexus from 'recoil-nexus';
import { loginPageUIStateAtom, pageStateAtom } from './src/atoms';
import { DeviceSetupPage } from './src/deviceSetup';
import { loginManager, setupManager } from './src/manager';
import { AppDataController, appStateAtom } from './src/store';

AppDataController.create();


const Separator = () => (
  <View style={styles.separator} />
);

const LoginPage = () => {
  const [emailText, setEmailText] = useState('');
  const [passwordText, setPasswordText] = useState('');
  const [loginPageUIState, setLoginPageUIState] = useRecoilState(loginPageUIStateAtom)
  const email = <TextInput style={styles.input}
    maxLength={40}
    editable
    autoComplete='email'
    keyboardType='email-address'
    placeholder='email'
    onChangeText={text => setEmailText(text)}
    value={emailText}></TextInput>;
  const password = <TextInput style={styles.input}
    maxLength={40}
    editable
    secureTextEntry
    placeholder='password'
    onChangeText={text => setPasswordText(text)}
    value={passwordText}></TextInput>;
  return <>
    {email}
    {password}
    <Separator />
    {loginPageUIState ? <>
      <Text>Incorrect Password</Text>
      <Separator />
    </> : <></>}
    <Button title='Submit'
      onPress={async () => { await loginManager.login(emailText, passwordText) }}
    ></Button>
  </>
}

const mainPageStyles = StyleSheet.create({
  logoutContainer: {
    right: 10,
    left: 10,
    position: 'absolute',
    bottom: 10,
  },
  emailContainer: {
    right: 10,
    left: 10,
    position: 'absolute',
    top: 100,
  },
  emailText: {
    textAlign: 'center',
    fontSize: 20
  }
});

const MainPage = () => {

  const appState = useRecoilValue(appStateAtom);
  const [pageState,setPageState] = useRecoilState(pageStateAtom);

  const logoutAlert = () =>
    Alert.alert(
      "Logout",
      "Are you sure you want to logout",
      [
        {
          text: "Cancel",
          onPress: () => { },
          style: "cancel"
        },
        { text: "OK", onPress: async () => { alert('Logged Out'); await loginManager.logout(); } }
      ]
    );

  if (pageState.deviceSetupPage){
    return <DeviceSetupPage></DeviceSetupPage>
  }


  return <>
    <Button title='Start Setup'
      onPress={() => {  setupManager.checkConnected() ; setPageState({...pageState, deviceSetupPage : true})}}
    ></Button>
    <Separator />
    <View style={mainPageStyles.logoutContainer}>
      <Text style={mainPageStyles.emailText}>{'Email: ' + appState.accountEmail}</Text>
      <Separator></Separator>
      <Separator></Separator>
      <Button title='Logout'
        onPress={logoutAlert}
      ></Button>
    </View>
  </>
}


function Main() {

  const appState = useRecoilValue(appStateAtom);
  const loggedIn = appState.loggedIn;

  return (
    <View style={styles.container}>
      {loggedIn ? <MainPage></MainPage> : <LoginPage></LoginPage>}
      <StatusBar style="auto" />
    </View>
  );
}

export default function App() {

  return <RecoilRoot>
    <RecoilNexus />
    <Main></Main>
  </RecoilRoot>
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
