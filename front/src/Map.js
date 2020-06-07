import React, { useState } from 'react';
import { Map as LeafletMap, TileLayer, Marker, Popup } from 'react-leaflet';
import './style.css'
import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import L from 'leaflet';

import HelloWorld from './slider';

const iconPerson = new L.Icon({
    iconUrl: 'https://www.svgrepo.com/show/183744/ship-boat.svg',
    iconRetinaUrl: 'https://www.svgrepo.com/show/183744/ship-boat.svg',
    iconAnchor: null,
    shadowUrl: null,
    shadowSize: null,
    shadowAnchor: null,
    iconSize: new L.Point(20, 20),
    className: 'leaflet-div-icon-xyz'
});

class Map extends React.Component {
   constructor() {
    super(1);
    this.state = {
      markers: []
    };
  }

  addMarker = (e) => {
    const {markers} = this.state
      console.log(e.latlng);
    markers.push({x: e.latlng.lat,y: e.latlng.lng, popup: 'СаААААААСКЕ'})
    this.setState({markers})
  }

  resetMarkers = (e) =>{
       console.log(e);
       let newMarkers = []
       e.forEach(i =>{
           newMarkers.push({x: i.lat,y: i.lon, popup: i.name, rot: i.COG})
       })
      console.log(newMarkers);
      this.setState({markers: newMarkers})
  }

  render() {
    console.log('saske');
    return (<div>
            <HelloWorld updateData={this.resetMarkers}/>
      <LeafletMap
        center={[45.221846, 36.679352]}
        onClick={this.addMarker}
        zoom={10}
        maxZoom={14}
        minZoom={10}
        attributionControl={true}
        zoomControl={true}
        doubleClickZoom={false}
        scrollWheelZoom={true}
        dragging={true}
        animate={true}
        className={'rec'}
      >
        <TileLayer

          url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
        />
        {this.state.markers.map((ship, idx) =>
          <Marker key={`marker-${idx}`} position={[ship.x, ship.y]}   icon={iconPerson}>
          <Popup>
            <span>{ship.popup}</span>
          </Popup>
        </Marker>
        )}
      </LeafletMap>
        </div>
    );
  }
}

export default Map
