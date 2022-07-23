import logo from './logo.svg';
import './App.css';
import { StyleSheet, css } from 'aphrodite';
import {
  useRecoilState,
  useRecoilValue,
  useSetRecoilState,
} from 'recoil';
import { deviceListState, authState, panelSizes, selectedDeviceState } from './atoms.js';
import { getRecoil, setRecoil } from "recoil-nexus";
import {
  TabContent,
  TabPane,
  Nav,
  NavItem,
  NavLink,
  Card,
  Button,
  CardText,
  Row,
  Col,
  CardHeader,
  CardBody,
  Form,
  Badge,
  Navbar,
  Collapse,
  Container,
  Modal, ModalHeader, ModalBody, ModalFooter
} from "reactstrap";
import React, { useState, memo, useEffect, Component } from "react";
import SplitPane from "react-split-pane";
import Pane from "react-split-pane";
import MapContainer from './Map';
import { auth_manager, device_list_manager } from './managers';
var auth_link = "http://localhost:8000";
var device_link = "http://localhost:8001";


const blockWidth = 172;
const blockHeight = 36;
const foreignObjectSize = 40;

const colors = {
  pale_red: "#FF6F79",
  white: "#ffffff",
  light_grey: "#b0b0b0",
  light_blue: "#75d1d0",
  dark_grey: "#616161",
  dark_blue: "#006c6e"
};

const sizes = {
  header: 60,
  simInfo: 37
};


const MapComponent = (args) => {
  const K_WIDTH = 40;
  const K_HEIGHT = 40;
  const placeStyle = {
    // initially any map object has left top corner at lat lng coordinates
    // it's on you to set object origin to 0,0 coordinates
    position: 'absolute',
    width: K_WIDTH,
    height: K_HEIGHT,
    left: -K_WIDTH / 2,
    top: -K_HEIGHT / 2,

    border: '5px solid #f44336',
    borderRadius: K_HEIGHT,
    backgroundColor: 'white',
    textAlign: 'center',
    color: '#3f51b5',
    fontSize: 16,
    fontWeight: 'bold',
    padding: 4
  };
  var deviceList = useRecoilValue(deviceListState);

  return <div style={{ width: "100%", height: "100%" }}>
    <MapContainer style={{ width: "100%", height: "100%" }}></MapContainer>
  </div>;
}

const deviceListComponentStyles = StyleSheet.create({
  container_styles : {
  textAlign : "left",
  display : 'flex',
  flexDirection : 'row'
}});


const DeviceListComponent = (args) => {
  const deviceList = useRecoilValue(deviceListState);

  return <>
    <Card>
      <CardHeader>
        Devices
      </CardHeader>
      <CardBody>
        {
          deviceList.devices.map((device) => {
            // console.log(device);
            return <>
              <Card id={device.device_id}>
                <CardBody>
                  <Container fluid="md" className={css(deviceListComponentStyles.container_styles)}>
                    <Row className="justify-content-md-center">
                      <Col md="auto">
                        <CardText>Device ID: {device.device_id}</CardText>
                      </Col>
                      <Col md="auto">
                        <CardText>Warning Level: {device.warning_level}</CardText>
                      </Col>
                      <Button
                      variant="secondary"
                      size="sm"
                      style={{ marginBottom: "1rem" }}
                      onClick={() => { device_list_manager.toggle_device_pin(device.device_id); }}
                      >
                        {device.pinned ? "Pinned" : "Not Pinned"}
                      </Button>
                      <Button
                        variant="secondary"
                        size="sm"
                        style={{ marginBottom: "1rem" }}
                        onClick={() => { device_list_manager.select_device(device.device_id); }}>
                        View
                      </Button>
                    </Row>
                  </Container>
                </CardBody>
              </Card>
            </>
          })
        }
      </CardBody>
    </Card>
  </>


}

const HorizontalSplit = props => {
  // const panel = useRecoilValue(panelSizes);
  const vh =
    Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0) -
    sizes.header;
  const [topHeight, setTopHeight] = useState(parseInt(vh / 2).toString() + "px");
  const [bottomHeight, setBottomHeight] = useState(parseInt(vh / 2).toString() + "px");

  const onChange = size => {
    setTopHeight(size[0]);
    setBottomHeight(size[1]);
  };
  setRecoil(panelSizes, { ...getRecoil(panelSizes), hTop: topHeight, hBottom: bottomHeight });
  return (
    <div>
      <SplitPane split="horizontal" onChange={size => onChange(size)}>
        <Pane
          initialSize={topHeight}
          minSize={parseInt(0.1 * vh).toString() + "px"}
          maxSize={parseInt(0.9 * vh).toString() + "px"}
        >
          <div id="mapID">
            <MapComponent></MapComponent>
          </div>
        </Pane>
        <Pane
          initialSize={bottomHeight}
          minSize={parseInt(0.1 * vh).toString() + "px"}
          maxSize={parseInt(0.9 * vh).toString() + "px"}
        >
          <div style={{ maxHeight: bottomHeight, height: bottomHeight }}>
            <div
              style={{
                maxHeight: bottomHeight,
                height: parseInt(bottomHeight) - sizes.simInfo,
                overflowY: "scroll"
              }}
            >
              <DeviceListComponent></DeviceListComponent>
            </div>
          </div>
        </Pane>
      </SplitPane>
    </div>
  );
};

const DeviceInfoPanel = (args) => {
  const selectedDevice = useRecoilValue(selectedDeviceState);
  return <>
    <Card>
      <CardHeader>DeviceID: {selectedDevice.device_id}</CardHeader>
      <CardBody>

      </CardBody>
    </Card>
  </>
}

const VerticalSplit = props => {
  const vh =
    Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0) -
    sizes.header;
  const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
  const [leftWidth, setLeftWidth] = useState(parseInt(vw * 0.7).toString() + "px");
  const [rightWidth, setRightWidth] = useState(parseInt(vw * 0.3).toString() + "px");

  const onChange = size => {
    setLeftWidth(size[0]);
    setRightWidth(size[1]);
  };
  setRecoil(panelSizes, { ...getRecoil(panelSizes), vLeft: leftWidth, vRight: rightWidth });
  return (
    <>
      <SplitPane
        split="vertical"
        onChange={size => {
          onChange(size);
        }}
      >
        <Pane initialSize={leftWidth} minSize="10%" maxSize="90%">
          <div>
            <HorizontalSplit style={{ maxHeight: vh, height: vh }}></HorizontalSplit>
          </div>
        </Pane>
        <Pane minSize="10%" maxSize="90%">
          <div style={{ overflowY: "scroll" }}>
            <DeviceInfoPanel></DeviceInfoPanel>
          </div>
        </Pane>
      </SplitPane>
    </>
  );
};



const appStyles = StyleSheet.create({
  text_style : {
  textAlign : "left"
}});

function App() {
  const navBarStyle = {
    height: sizes.header,
    background: colors.pale_red,
    margin: 0,
  };

  auth_manager.get_auth_key(device_list_manager.get_device_list);

  return (
    <div className={css(appStyles.text_style)} style={{ height: "100%" }}>
      <Navbar style={navBarStyle}>
        <h1>Dashboard</h1>
      </Navbar>
      <VerticalSplit style={{ height: "100%" }}></VerticalSplit>
      {/* <SplitPane split="vertical" defaultSize={200} primary="second">
        <div />
        <div />
      </SplitPane> */}
    </div>

  );
}

export default App;
