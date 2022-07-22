import React, { Component } from 'react';
import { Map, GoogleApiWrapper } from 'google-maps-react';
import { getRecoil } from 'recoil-nexus';
import { panelSizes } from './atoms';

var mapStyles = {
  width: '100%',
  height: '100%'
};

export class MapContainer extends Component {
  render() {
    mapStyles = {
        height : getRecoil(panelSizes).hTop,
        width : getRecoil(panelSizes).vLeft,
    };
    return (
      <Map
      resetBoundsOnResize={true}
        google={this.props.google}
        zoom={14}
        style={mapStyles}
        initialCenter={
          {
            lat: -1.2884,
            lng: 36.8233
          }
        }
      />
    );
  }
}

export default GoogleApiWrapper({
  apiKey: 'AIzaSyAXrhOvVPfXbX4svEMfTXnxIXNFkOyl474'
})(MapContainer);
