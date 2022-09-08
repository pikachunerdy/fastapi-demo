import { deviceListState, authState, selectedDeviceState, accountListState, selectedAccountState, companyState, filterState } from './atoms.js';
import { getRecoil, setRecoil } from "recoil-nexus";


var auth_link = "http://localhost:8000";
var device_link = "http://localhost:8001";



export var auth_manager = {
  get_auth_key: async function (username, password, callback = () => { }) {
    console.log('get auth key')
    var obj = {
      link: auth_link + '/token',
      object: {
        method: 'POST',
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: 'username=' + username + '&password=' + password
      }
    }
    var response = await fetch(obj.link, obj.object).then(response => {
      console.log('response')
      if (!response.ok) {
        alert("Invalid Credentials");
        setRecoil(authState, { token: '', validToken: false, showInvalidCredWarning: true });
        return;
      }
      return response.json()
    }).then(response => {
      console.log(response)
      setRecoil(authState, {
        token: response.access_token, validToken: true, showInvalidCredWarning: false
      });
      localStorage.setItem('token', response.access_token);
      console.log(response.access_token)
      callback();
    })
  },

  check_token: function () {
    const token = localStorage.getItem('token')
    var obj = {
      link: auth_link + '/validate_token',
      object: {
        method: 'GET',
        headers: {
          // 'Accept': 'application/json',
          'Authorization': 'Bearer ' + token,
        }
      }
    };
    fetch(obj.link, obj.object)
      .then(response => {
        if (!response.ok) {
          // setRecoil(authState, { token: '', validToken : false })
        }
        else {
          setRecoil(authState, { token: token, validToken: true, showInvalidCredWarning: false });
        }
      })
  },

  logout: function () {
    localStorage.setItem('token', '');
    setRecoil(authState, { token: '', validToken: false, showInvalidCredWarning: false })
  }
};

export var company_manager = {

  _get_labels: function () {
    var obj = {
      link: device_link + '/company/labels',
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
      .then(data => setRecoil(companyState, {labels : data}));
  },

  remove_device_label: async function (device_id, label) {
    var obj = {
      link: device_link + '/company/device_label?' + new URLSearchParams({
        label: label,
        device_id: device_id,
      }),
      object: {
        method: 'DELETE',
        headers: {
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + getRecoil(authState).token,
        }
      }
    };
    await fetch(obj.link, obj.object);
  },

  add_device_label: async function (device_id, label) {
    var obj = {
      link: device_link + '/company/device_label?' + new URLSearchParams({
        label: label,
        device_id: device_id,
      }),
      object: {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + getRecoil(authState).token,
        }
      }
    };
    await fetch(obj.link, obj.object);
  },

  create_label: function (label) {
    var obj = {
      link: device_link + '/company/label?' + new URLSearchParams({
        label: label,
      }),
      object: {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + getRecoil(authState).token,
        }
      }
    };
    fetch(obj.link, obj.object)
      .then(() => this._get_labels());
  },

  delete_label: function (label) {
    var obj = {
      link: device_link + '/company/label?' + new URLSearchParams({
        label: label,
      }),
      object: {
        method: 'DELETE',
        headers: {
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + getRecoil(authState).token,
        }
      }
    };
    fetch(obj.link, obj.object)
      .then(() => this._get_labels());
  },

  setup : function () {
    this._get_labels();
  }
}

export var device_list_manager = {
  get_device_list: async function (callback = () => {}) {
    const filter = getRecoil(filterState);
    const params = filter.labels ? new URLSearchParams({
      pinned: filter.pinned,
    }) :new URLSearchParams({
    });
    var label_param = '';
    filter.labels.map(label => '&labels=' + label).forEach(label => label_param += label);
    var obj = {
      link: device_link + '/devices?' + params + label_param,
      object: {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + getRecoil(authState).token,
        }
      }
    };
    // console.log(obj);
    await fetch(obj.link, obj.object)
      .then(response => response.json())
      .then((response) => {console.log(response); return response})
      .then(data => setRecoil(deviceListState, data))
      .then(callback());
  },

  select_device: async function (device_id, measurement_period_type = "day") {
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
   await fetch(obj.link, obj.object)
      .then(response => response.json())
      .then(data => { setRecoil(selectedDeviceState, data) });
    // .then(console.log(getRecoil(selectedDeviceState)))
  },

  toggle_device_pin: function (device_id, callback = () => { }) {
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
        fetch(obj.link, obj.object).then(() => { this.get_device_list(); callback(); this.select_device(device_id); });
      });
  },

  change_device_comments: function (device_id, comments, callback = () => { }) {
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
        device.comments = comments;
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
        fetch(obj.link, obj.object).then(() => { this.get_device_list(); callback(); this.select_device(device_id); });
      });
  },

  change_device_warning_level_height: function (device_id, warning_level_height, callback = () => { }) {
    var obj = {
      link: device_link + '/device?' + new URLSearchParams({
        device_id: device_id,
        measurement_period_type: 'none',
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
        device.warning_level_height_mm = warning_level_height;
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
        fetch(obj.link, obj.object).then(() => { this.get_device_list(); callback(); this.select_device(device_id); });
      });
  },
}

export var account_manager = {
  get_account_list: function () {
    var obj = {
      link: auth_link + '/accounts/accounts',
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
      .then(data => setRecoil(accountListState, data));
  },

  create_account: function (email, password, view_devices, register_devices, manage_accounts) {
    const new_account = {
      email: email,
      password: password,
      permissions: {
        view_devices: view_devices,
        register_devices: register_devices,
        manage_devices: view_devices,
        manage_accounts: manage_accounts,
        view_device_data: view_devices
      }
    }
    var obj = {
      link: auth_link + '/accounts/account',
      object: {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + getRecoil(authState).token,
          'Content-type': 'application/json'
        },
        body: JSON.stringify(
          new_account
        )
      }
    };
    fetch(obj.link, obj.object).then(() => { this.get_account_list() });
  },

  select_account: function (account_id, callback = () => { }) {
    var obj = {
      link: auth_link + '/accounts/account/' + account_id,
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
      .then((response) => { return response })
      .then(data => { setRecoil(selectedAccountState, data) })
      .then(() => callback());
  },

  delete_account: function (account_id) {
    var obj = {
      link: auth_link + '/accounts/account/' + account_id,
      object: {
        method: 'DELETE',
        headers: {
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + getRecoil(authState).token,
        }
      }
    };
    fetch(obj.link, obj.object).then(() => this.get_account_list());
  },

  modify_account: function (account_id, view_devices, register_devices, manage_accounts) {
    const new_account = {
      id: account_id,
      permissions: {
        view_devices: view_devices,
        register_devices: register_devices,
        manage_devices: view_devices,
        manage_accounts: manage_accounts,
        view_device_data: view_devices
      }
    }
    var obj = {
      link: auth_link + '/accounts/account',
      object: {
        method: 'PUT',
        headers: {
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + getRecoil(authState).token,
          'Content-type': 'application/json'
        },
        body: JSON.stringify(
          new_account
        )
      }
    };
    fetch(obj.link, obj.object).then(() => { this.get_account_list() });
  }
}
