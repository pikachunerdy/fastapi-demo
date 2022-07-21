import logo from './logo.svg';
import './App.css';
import { StyleSheet, css } from 'aphrodite';
import {
  useRecoilState,
  useRecoilValue,
} from 'recoil';
import { deviceListState, authState} from './atoms.js';
import { getRecoil, setRecoil } from "recoil-nexus";

var auth_token = '';

var auth_link = "http://localhost:8000";
var device_link = "http://localhost:8001";



var auth_manager = {
  get_auth_key : function (callback) {
    var obj = {
      link: auth_link + '/token',
      object: {
        method: 'POST',
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: 'username=test&password=test'
      }
    }
    fetch(obj.link, obj.object).then(response => response.json()).then(response => {console.log(response);setRecoil(authState, {token : response.access_token});console.log(getRecoil(authState).token)}).then(() => {console.log("running callback");callback();});
  }
}

var device_list_manager = {
  get_device_list: function () {
    console.log(getRecoil(authState).token);
    var obj = {
      link: device_link + '/devices',
      object: {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + getRecoil(authState).token,
        }
      }
    };
    console.log(obj);
    fetch(obj.link, obj.object)
      .then(response => response.json())
      .then(data => console.log(data));
  }
}

const MapComponent = (args) => {

  return <></>
}

const DeviceListComponent = (args) => {
  const deviceList = useRecoilValue(deviceListState);

  return <>
    {
      deviceList.devices.map((device) => {
        return <>
          <p>device.device_id</p>
        </>
      })
    }
  </>

}

const HorizontalSplit = (args) => {

  return <>
  </>
}

const DeviceInfoPanel = (args) => {

  return <></>
}

const VerticalSplit = (args) => {

  return <></>
}



const AppStyles = StyleSheet.create({

});

function App() {
  auth_manager.get_auth_key(device_list_manager.get_device_list);
  return (
    <div className={css(AppStyles) + ' App'}>
    </div>
  );
}

export default App;
