import React, { Component } from 'react';
import { Map, GoogleApiWrapper, Marker } from 'google-maps-react';
import { getRecoil } from 'recoil-nexus';
import { deviceListState, panelSizes } from './atoms';
import { auth_manager, device_list_manager } from './managers';

var mapStyles = {
  width: '0px',
  height: '0px',
  zIndex: '-10'
};

export class MapContainer extends Component {
  componentDidMount() {
    document.getElementById("mapID").firstChild.firstChild.firstChild.style.width = "0px";
    document.getElementById("mapID").firstChild.firstChild.firstChild.style.height = "0px";    // set el height and width etc.
  };
  render() {
    mapStyles = {
      height: (parseInt(getRecoil(panelSizes).hTop.replace(/px/,""))-40)+"px",
      width: (parseInt(getRecoil(panelSizes).vLeft.replace(/px/,""))-60)+"px",
    };
    var devices = getRecoil(deviceListState);
    return (
      <Map
        resetBoundsOnResize={true}
        google={this.props.google}
        zoom={14}
        style={mapStyles}
        initialCenter={
          {
            lat: 51.49,
            lng: -0.183
          }
        }
      >
        {devices.devices.map((device) => {
          return (<Marker position={{lat : device.latitude, lng : device.longitude}} onClick={() => device_list_manager.select_device(device.device_id)}/>)
        })}
      </Map>
    );
  }
}

export default GoogleApiWrapper({
  apiKey: 'AIzaSyAXrhOvVPfXbX4svEMfTXnxIXNFkOyl474'
})(MapContainer);
