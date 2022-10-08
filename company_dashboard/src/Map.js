import mapboxgl from '!mapbox-gl'; // eslint-disable-line import/no-webpack-loader-syntax
import React, { useRef, useEffect, useState } from 'react';
import { useRecoilState, useRecoilValue } from 'recoil';

import { getRecoil } from 'recoil-nexus';
import { deviceListState, filterState, mapState, navStateAtom, panelSizes } from './atoms';
import { device_list_manager } from './managers';

mapboxgl.accessToken = 'pk.eyJ1IjoibWF4LXdpY2toYW0iLCJhIjoiY2w4bjlnNGIwMGY0NTN1b2FtMDZ4dWRqMSJ9.qbF5dOznUZ0eWlOay_3V4Q';

export default function MapContainer() {
  const mapContainer = useRef(null);
  const devices = useRecoilValue(deviceListState);
  const panel = useRecoilValue(panelSizes);
  const nav = useRecoilValue(navStateAtom);
  const filter = useRecoilValue(filterState)
  const [mapAtom, setMapAtom] = useRecoilState(mapState);
  const map = useRef(null);
  const [lng, setLng] = useState(-70.9);
  const [lat, setLat] = useState(42.35);
  const [zoom, setZoom] = useState(3);
  const size = 100;


  useEffect(() => {
    if (map.current) {
      map.current.triggerRepaint();
      if (mapAtom.required_update) {
        map.current.setCenter(mapAtom.requested_centre);
        setMapAtom({ ...mapAtom, required_update: false });
      }
      map.current.resize()
      map.current.triggerRepaint();

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

      const onLoad = () => {

        console.log('loaded');
        // console.log('hello');
        var current_devices = getRecoil(deviceListState);
        // console.log(current_devices);
        if (!map.current.hasImage('pulsing-dot')) {
          map.current.addImage('pulsing-dot', pulsingDot, { pixelRatio: 2 });
        }
        if (map.current.getSource('dot-point')) {
          map.current.removeLayer('layer-with-pulsing-dot');
          map.current.removeSource('dot-point');
        }
        const data = current_devices.devices.filter(device => device.device_id.toLowerCase().includes(filter.searchText.toLowerCase()))
        .filter(device => device.pinned || !filter.pinned).map(device => {
          return {
            'type': 'Feature',
            'id': device.device_id,
            'geometry': {
              'type': 'Point',
              'coordinates': [device.longitude, device.latitude] // icon position [lng, lat]
            }
          }
        });
        // console.log(data);
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


      };
      if (map.current.loaded()) {
        onLoad();
      }

      map.current.on('load', () => {
        onLoad();
      });

      // map.current.on('data', () => {
      //   onLoad();
      // });
    }
    if (map.current) return; // initialize map only once
    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [0, 52],
      zoom: zoom
    });
  });
  const mapStyles = {
    height: (parseInt(panel.hTop.replace(/px/, "")) - 30) + "px",
    width : (parseInt(panel.vLeft.replace(/px/, "")) - 40) + "px",
  };
  return (
    <div>
      <div style={{ height: mapStyles.height, width : mapStyles.width}}>
        <div ref={mapContainer} style={{ height: '100%' }} />
      </div>
    </div>
  );
}
