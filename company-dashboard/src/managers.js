import { deviceListState, authState, selectedDeviceState } from './atoms.js';
import { getRecoil, setRecoil } from "recoil-nexus";


var auth_link = "http://localhost:8000";
var device_link = "http://localhost:8001";



export var auth_manager = {
  get_auth_key: function (callback) {
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
    fetch(obj.link, obj.object).then(response => response.json()).then(response => {  setRecoil(authState, { token: response.access_token }); }).then(() => {  callback(); });
  }
};

export var device_list_manager = {
  get_device_list: function () {
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
    // console.log(obj);
    fetch(obj.link, obj.object)
      .then(response => response.json())
      .then(data => setRecoil(deviceListState, data));
  },

  select_device: function (device_id, measurement_period_type = "day") {
    var obj = {
      link: device_link + '/device?' + new URLSearchParams({
        device_id: device_id,
        measurement_period_type: measurement_period_type,
      }),
      object: {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + getRecoil(authState).token,
        }
      }
    };
    fetch(obj.link, obj.object)
      .then(response => response.json())
      .then(data => { setRecoil(selectedDeviceState, data)});
      // .then(console.log(getRecoil(selectedDeviceState)))
  },

  toggle_device_pin : function (device_id) {
    var obj = {
      link: device_link + '/device?' + new URLSearchParams({
        device_id: device_id,
        measurement_period_type: 'day',
      }),
      object: {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + getRecoil(authState).token,
        }
      }
    };
    fetch(obj.link, obj.object)
      .then(response => response.json())
      .then(device => {
        device.pinned = !device.pinned;
        var obj = {
          link: device_link + '/device',
          object: {
            method: 'PUT',
            headers: {
              'Accept': 'application/json',
              'Authorization': 'Bearer ' + getRecoil(authState).token,
              'Content-type': 'application/json'
            },
            body: JSON.stringify(
              device
            )
          }
        };
        fetch(obj.link, obj.object).then(() =>  this.get_device_list());
      });
  },

}