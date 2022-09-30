// import React, { Component } from 'react';
// // import { Map, GoogleApiWrapper, Marker } from 'google-maps-react';
// import { getRecoil } from 'recoil-nexus';
// import { deviceListState, panelSizes } from './atoms';
// import { auth_manager, device_list_manager } from './managers';
// //     "google-maps-react": "*",
// var mapStyles = {
//   width: '0px',
//   height: '0px',
//   zIndex: '-10'
// };

// export default class MapContainer extends Component {
//   componentDidMount() {
//     // document.getElementById("mapID").firstChild.firstChild.firstChild.style.width = "0px";
//     // document.getElementById("mapID").firstChild.firstChild.firstChild.style.height = "0px";    // set el height and width etc.
//   };
//   render() {
//     mapStyles = {
//       height: (parseInt(getRecoil(panelSizes).hTop.replace(/px/,""))-40)+"px",
//       width: (parseInt(getRecoil(panelSizes).vLeft.replace(/px/,""))-60)+"px",
//     };
//     var devices = getRecoil(deviceListState);
//     return (
//       // <Map
//       //   resetBoundsOnResize={true}
//       //   google={this.props.google}
//       //   zoom={14}
//       //   style={mapStyles}
//       //   initialCenter={
//       //     {
//       //       lat: 51.49,
//       //       lng: -0.183
//       //     }
//       //   }
//       // >
//       //   {devices.devices.map((device) => {
//       //     return (<Marker position={{lat : device.latitude, lng : device.longitude}} onClick={() => device_list_manager.select_device(device.device_id)}/>)
//       //   })}
//       // </Map>
//       <div>Map</div>
//     );
//   }
// }

// // export default GoogleApiWrapper({
// //   apiKey: 'AIzaSyAXrhOvVPfXbX4svEMfTXnxIXNFkOyl474'
// // })(MapContainer);
//////////////////////////////////////////////////////////

// // import maplibregl = require('maplibre-gl');
// import React, { useEffect, useRef } from 'react';
// // import './myMap.css';
// import { Map } from 'maplibre-gl';


// const MapContainer = ({
//   mapIsReadyCallback /* To be triggered when a map object is created */,
// }) => {
//   const mapContainer = useRef(null);

//   useEffect(() => {
//     const myAPIKey = 'pk.eyJ1IjoibWF4LXdpY2toYW0iLCJhIjoiY2w4bjl0aDh4MDRhMDNwbzQyMGpibTJncyJ9.8GFH3xcOF3XmUrcUH8Yo5Q';
//     const mapStyle =
//       'https://maps.geoapify.com/v1/styles/dark-matter/style.json';

//     const initialState = {
//       lng: 11,
//       lat: 49,
//       zoom: 4,
//     };

//     const map = new Map({
//       container: mapContainer.current,
//       style: `${mapStyle}?apiKey=${myAPIKey}`,
//       center: [initialState.lng, initialState.lat],
//       zoom: initialState.zoom,
//     });

//     mapIsReadyCallback(map);
//   }, [mapContainer.current]);

//   return <div className="map-container" ref={mapContainer}></div>;
// };

// export default MapContainer;


import mapboxgl from '!mapbox-gl'; // eslint-disable-line import/no-webpack-loader-syntax
import React, { useRef, useEffect, useState } from 'react';
import { useRecoilValue } from 'recoil';

import { getRecoil } from 'recoil-nexus';
import { deviceListState, panelSizes } from './atoms';
import { device_list_manager } from './managers';

mapboxgl.accessToken = 'pk.eyJ1IjoibWF4LXdpY2toYW0iLCJhIjoiY2w4bjlnNGIwMGY0NTN1b2FtMDZ4dWRqMSJ9.qbF5dOznUZ0eWlOay_3V4Q';

export default function MapContainer() {
  const mapContainer = useRef(null);
  const devices = useRecoilValue(deviceListState);
  const map = useRef(null);
  const [lng, setLng] = useState(-70.9);
  const [lat, setLat] = useState(42.35);
  const [zoom, setZoom] = useState(9);
  console.log(devices);
  const size = 100;
  if (map.current) {
    console.log('settings map stuff')
    const pulsingDot = {
      width: size,
      height: size,
      data: new Uint8Array(size * size * 4),

      // When the layer is added to the map,
      // get the rendering context for the map canvas.
      onAdd: function () {
        const canvas = document.createElement('canvas');
        canvas.width = this.width;
        canvas.height = this.height;
        this.context = canvas.getContext('2d');
      },

      // Call once before every frame where the icon will be used.
      render: function () {
        // const duration = 1000;
        // const t = (performance.now() % duration) / duration;

        const radius = (size / 2) * 0.3;
        const context = this.context;

        // Draw the outer circle.
        context.clearRect(0, 0, this.width, this.height);
        // Draw the inner circle.
        context.beginPath();
        context.arc(
          this.width / 2,
          this.height / 2,
          radius,
          0,
          Math.PI * 2
        );
        context.fillStyle = 'rgba(255, 100, 100, 1)';
        context.strokeStyle = 'white';
        context.lineWidth = 4;
        context.fill();
        context.stroke();

        // Update this image's data with data from the canvas.
        this.data = context.getImageData(
          0,
          0,
          this.width,
          this.height
        ).data;

        // Continuously repaint the map, resulting
        // in the smooth animation of the dot.
        map.current.triggerRepaint();

        // Return `true` to let the map know that the image was updated.
        return true;
      }
    };

    map.current.on('load', () => {
      console.log('hello');
      const current_devices = getRecoil(deviceListState);
      console.log(current_devices);
      if (!map.current.hasImage('pulsing-dot')) {
        map.current.addImage('pulsing-dot', pulsingDot, { pixelRatio: 2 });
      }
      if (map.current.getSource('dot-point')) {
        map.current.removeLayer('layer-with-pulsing-dot');
        map.current.removeSource('dot-point');
      }
      const data = current_devices.devices.map(device => {
        return {
          'type': 'Feature',
          'id' : device.device_id,
          'geometry': {
            'type': 'Point',
            'coordinates': [device.longitude, device.latitude] // icon position [lng, lat]
          }
        }
      });
      console.log(data);
      map.current.addSource('dot-point', {
        'type': 'geojson',
        'data': {
          'type': 'FeatureCollection',
          'features': data
        }
      });
      map.current.addLayer({
        'id': 'layer-with-pulsing-dot',
        // 'type': 'symbol',
        'type': 'circle',
        'source': 'dot-point',
        // 'layout': {
        //   'icon-image': 'pulsing-dot'
        // }
        'paint': {
          'circle-radius': 6,
          'circle-color': '#B42222'
        },
      });
      map.current.on('click', 'layer-with-pulsing-dot', (e) => {
        device_list_manager.select_device(e.features[0].id);
        map.current.flyTo({

          center: e.features[0].geometry.coordinates
        });
      });

      map.current.on('mouseenter', 'layer-with-pulsing-dot', () => {
        map.current.getCanvas().style.cursor = 'pointer';
      });

      // Change it back to a pointer when it leaves.
      map.current.on('mouseleave', 'layer-with-pulsing-dot', () => {
        map.current.getCanvas().style.cursor = '';
      });
      map.current.triggerRepaint();
    });

  }
  useEffect(() => {


    if (map.current) return; // initialize map only once
    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [0, 0],
      zoom: zoom
    });
  });

  const mapStyles = {
    height: (parseInt(getRecoil(panelSizes).hTop.replace(/px/, "")) - 40) + "px",
    // width: (parseInt(getRecoil(panelSizes).vLeft.replace(/px/,""))-60)+"px",
  };
  // console.slog(mapStyles);
  return (
    <div>
      <div ref={mapContainer} className="map-container" style={{ mapStyles }} />
      {/* <div className="sidebar">
        Longitude: {lng} | Latitude: {lat} | Zoom: {zoom}
      </div> */}
    </div>
  );
}
