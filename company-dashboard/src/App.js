import logo from './logo.svg';
import './App.css';
import { StyleSheet, css } from 'aphrodite';
import "bootstrap/dist/css/bootstrap.min.css";
import {
  useRecoilState,
  useRecoilValue,
  useSetRecoilState,
} from 'recoil';
import { deviceListState, authState, panelSizes, selectedDeviceState, accountListState, selectedAccountState } from './atoms.js';
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
  Container,
  Modal, ModalHeader, ModalBody, ModalFooter, FormGroup, Label, Input
} from "reactstrap";
import React, { useState, memo, useEffect, Component } from "react";
import SplitPane from "react-split-pane";
import Pane from "react-split-pane";
import MapContainer from './Map';
import { auth_manager, device_list_manager, account_manager } from './managers';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';


// const blockWidth = 172;
// const blockHeight = 36;
// const foreignObjectSize = 40;

const colors = {
  pale_red: "#3487f5",
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

const styles = {
  card_style: {
    padding: 5,
    margin: 15,
    borderRadius: 3,
    // backgroundColor : '#232223',
    // borderColor : '#232223',
    // backgroundColor: '#232323',
    height: '100%',
    backgroundColor : '#1c1c1c',
    borderColor : '#1c1c1c',
  },
  container_styles: {
  },
  header_styles: {
    marginLeft: 10,
    padding: 20,
    margin: 5,
    width: '100%',
    color: '#e7eded',
    fontSize: 25,
    float: 'left',
    clear: 'right',
    backgroundColor : '#232223',
    borderColor : '#232223',
  },
  col_styles: {
    backgroundColor: '#a3e0ff',
    borderRadius: 10,
    margin: 5,
    padding: 10,
    float: 'left'
  },
  row_styles: {
    // backgroundColor: '#074587',
    borderRadius: 10,
    margin: 5,
    padding: 1,
    float: 'left',
    width: '100%',
    // borderColor : '#f5f5f5',
    // borderWidth : 2,
    border:'1px solid #999999',
  },
  text_style: {
    paddingTop: 5,
    paddingRight: 0,
    paddingBottom: 0,
    paddingLeft: 0,
    margin: 5,
    fontSize: 20,
    clear: 'left right',
    color: '#8f979a'
  },
  button_styles: {
    backgroundColor: '#2db4f7',
    boxShadow: 0,
    borderRadius: 10,
    padding: 10,
    margin: 5,
    borderColor: '#2db4f7',
    width: '7em'
  },
}

const modified_styles = {
  unpinned_button_styles: {
    ...styles.button_styles,
    backgroundColor: '#6a777d',
    borderColor: '#6a777d'
  }
}

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
  var height = (parseInt(getRecoil(panelSizes).hTop.replace(/px/, "")) - 40) + "px";
  const mapComponentStyles = StyleSheet.create({
    card_style: {
      ...styles.card_style,
      height: height,
      width: '97%'
    }
  });
  return <div className={css(mapComponentStyles.card_style)} style={{ width: "100%", height: height }}>
    <MapContainer style={{ width: "100%", height: height }}></MapContainer>
  </div>;
}

const deviceListComponentStyles = StyleSheet.create({
  card_style: {
    ...styles.card_style,
    backgroundColor : '#1c1c1c',
    borderColor : '#1c1c1c',
    paddingTop : 0,
    marginTop : 0
  },
  card_body_style: {
    ...styles.card_style,
    backgroundColor : '#232223',
    borderColor : '#232223',
    paddingTop : 0,
    marginTop : 0,
    marginLeft : 0,
    paddingLeft : 10,
    paddingRight : 0

  },
  container_styles: {
  },
  header_styles: {
    ...styles.header_styles,
    backgroundColor : '#1c1c1c',
    borderColor : '#1c1c1c',
    paddingTop : 0,
    marginTop : 0,
    marginBottom : 0,
    paddingBottom : 10,
  },
  col_styles: {
    ...styles.col_styles,
    minWidth : 'fit-content'
  },
  row_styles: {
    ...styles.row_styles,
    marginLeft : 0,
    marginRight : 0
  },
  button_styles: {
    ...styles.button_styles
  },
  unpinned_button_style: {
    ...modified_styles.unpinned_button_styles,
  }
});


const DeviceListComponent = (args) => {
  const deviceList = useRecoilValue(deviceListState);

  return <Card className={css(deviceListComponentStyles.card_style)} style={{ height: '100%' }}>
    <CardHeader className={css(deviceListComponentStyles.header_styles)}>
      <CardText>Devices</CardText>
    </CardHeader>
    <CardBody className={css(deviceListComponentStyles.card_body_style)}>
      {
        deviceList.devices.map((device) => {
          // console.log(device);
          return <>
            {/* <Card id={device.device_id}> */}
              <CardBody>
                <Container fluid="md" className={css(deviceListComponentStyles.container_styles)}>
                  <Row className={css(deviceListComponentStyles.row_styles)} >
                    <Col xs="3" className={css(deviceListComponentStyles.col_styles)} >
                      {/* <CardText className={css(deviceListComponentStyles.header_styles)}>Device ID: {device.device_id}</CardText> */}
                      Device ID: {device.device_id}
                    </Col>
                    <Col xs="3" className={css(deviceListComponentStyles.col_styles)} >
                      {/* <CardText className={css(deviceListComponentStyles.header_styles)}>Warning Level: {device.warning_level}</CardText> */}
                      Warning Level: {device.warning_level}
                    </Col>
                    <Button
                      className={css(device.pinned ? deviceListComponentStyles.button_styles : deviceListComponentStyles.unpinned_button_style)}
                      variant="secondary"
                      size="sm"
                      style={{ marginBottom: "1rem" }}
                      onClick={() => { device_list_manager.toggle_device_pin(device.device_id); }}
                    >
                      {device.pinned ? "Pinned" : "Not Pinned"}
                    </Button>
                    <Button
                      className={css(deviceListComponentStyles.button_styles)}
                      variant="secondary"
                      size="sm"
                      style={{ marginBottom: "1rem" }}
                      onClick={() => { device_list_manager.select_device(device.device_id); }}>
                      View
                    </Button>
                  </Row>
                </Container>
              </CardBody>
            {/* </Card> */}
          </>
        })
      }
    </CardBody>
  </Card>


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

const deviceInfoPanelStyles = StyleSheet.create({
  card_style: {
    ...styles.card_style,
    backgroundColor : '#232223',
    borderColor : '#232223',
  },
  card_body_style: {
    ...styles.card_style,
    backgroundColor : '#232223',
    borderColor : '#232223',
    paddingTop : 0,
    marginTop : 0,
    paddingLeft : 0,
    paddingRight : 0

  },
  container_styles: {
  },
  header_styles: {
    ...styles.header_styles
  },
  row_styles: {
    ...styles.row_styles,
    marginLeft : 0,
    marginRight : 0
  },
  text_style: {
    ...styles.text_style
  },
  button_styles: {
    ...styles.button_styles,
  },
  unpinned_button_styles: {
    ...modified_styles.unpinned_button_styles,
  },
  selected_switch_button_styles: {
    ...styles.button_styles,
    backgroundColor: '#2db4f7',
    borderRadius: 3,
    padding: 3,
    margin: 5,
    borderColor: '#2db4f7',
    width: '4em'
  },
  switch_button_styles: {
    ...modified_styles.unpinned_button_styles,
    borderRadius: 3,
    padding: 3,
    margin: 5,
    width: '4em'
  }
});


const DeviceInfoPanel = (args) => {
  const selectedDevice = useRecoilValue(selectedDeviceState);
  const panel = useRecoilValue(panelSizes);
  const width = parseInt(panel.vRight, 10) - 60;

  const changePeriodType = (periodType) => {
    device_list_manager.select_device(selectedDevice.device_id, periodType);
  };
  if (selectedDevice.device_id) {
    var date = new Date(parseInt(selectedDevice.creation_date) * 1000);
    const dateStr = date.getDate() + '/' + date.getMonth() + '/' + date.getFullYear();
    return <>
      <Card className={css(deviceInfoPanelStyles.card_style)}>
        <CardHeader className={css(deviceInfoPanelStyles.header_styles)}><CardText>DeviceID: {selectedDevice.device_id}</CardText></CardHeader>
        <CardBody className={css(deviceInfoPanelStyles.card_body_style)}>
          {/* pinned */}
          <Button
            className={css(selectedDevice.pinned ? deviceInfoPanelStyles.button_styles : deviceInfoPanelStyles.unpinned_button_styles)}
            variant="secondary"
            size="sm"
            style={{ marginBottom: "1rem" }}
            onClick={() => { device_list_manager.toggle_device_pin(selectedDevice.device_id, (() => { device_list_manager.select_device(selectedDevice.device_id) })); }}
          >
            {selectedDevice.pinned ? "Pinned" : "Not Pinned"}
          </Button>
          {/* warning level height */}
          <CardText className={css(deviceInfoPanelStyles.text_style)}>
            Warning Level Height: {selectedDevice.warning_level_height_mm}
          </CardText>
          {/* creation date */}
          <CardText className={css(deviceInfoPanelStyles.text_style)}>
            Creation Date: {dateStr}
          </CardText>
          {/* warning level */}
          <CardText className={css(deviceInfoPanelStyles.text_style)}>
            Warning Level: {selectedDevice.warning_level}
          </CardText>
          <CardText className={css(deviceInfoPanelStyles.text_style)}>Comments: </CardText>
          {/* comments */}
          {/* <Card>
            {selectedDevice.comments.map(comment => <CardText>comment</CardText>)}
          </Card> */}
          {/* <CanvasJSChart options = {chart_options} ></CanvasJSChart> */}
          <Row className={css(deviceInfoPanelStyles.text_style)}> 
            {[['day', 'Day'], ['week', 'Week'], ['month', 'Month'], ['year', 'Year']].map(([key, label]) => {
              return <Button className={css(selectedDevice.measurement_period_type === key ?
                deviceInfoPanelStyles.selected_switch_button_styles : deviceInfoPanelStyles.switch_button_styles)}
                onClick={() => { changePeriodType(key) }}>
                {label}
              </Button>
            })}
          </Row>
          <LineChart width={width} height={400} data={selectedDevice.measurements}>
            <Line type="monotone" dataKey="distance_mm" stroke="#8884d8" />
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="time_s" />
            <YAxis />
            <Tooltip />
          </LineChart>
        </CardBody>
      </Card>
    </>
  }
  return <>
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
    setRightWidth((vw - parseInt(size[0].replace(/px/, ""))) + "px");
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


const DeviceMetricsPage = props => {
  return <VerticalSplit  style={{ height: "100%" }}></VerticalSplit>
}

const accountsPageStyle = StyleSheet.create({
  main_style: {
    display: 'flex',
    justifyContent: 'center',
    flexDirection: 'column'
  },
  row_style: {
    display: 'flex',
    justifyContent: 'center',
    width: '100%'
  },
  create_new_style: {
    backgroundColor: '#2db4f7',
    boxShadow: 0,
    borderRadius: 10,
    padding: 10,
    margin: 5,
    borderColor: '#2db4f7',
    marginTop: 50,
    marginBottom: 20,
    width: '20em'
  },
  break_style: {
    flexBasis: '100%',
    height: 0
  },
  account_button_style: {
    minWidth: '40em',
    height: '3em',
    fontSize: 18,
    width: 'fit-content',
    marginBottom: 20,
  },
  search_style: {
    width: '20em',
    marginBottom: 30
  },
  delete_button_style: {
    backgroundColor: "#ff4545",
    borderColor: "#ff4545"
  }
});
const AccountsPage = props => {
  const accountList = useRecoilValue(accountListState);
  const selectedAccount = useRecoilValue(selectedAccountState)
  const [newAccountModal, setNewAccountModal] = useState(false);
  const [modifyAccountModal, setModifyAccountModal] = useState(false);
  const [searchText, setSearchText] = useState("");


  console.log(selectedAccount);
  const onFormSubmitAccount = (e) => {
    e.preventDefault();
    account_manager.create_account(e.target.newEmail.value,
      e.target.newPassword.value,
      e.target.newViewDevices.checked,
      e.target.newRegisterDevices.checked,
      e.target.newManageAccounts.checked
    )
    setNewAccountModal(false);
  }

  const onFormSubmitModifyAccount = (e) => {
    e.preventDefault();
    account_manager.modify_account(
      selectedAccount.id,
      e.target.modifyViewDevices.checked,
      e.target.modifyRegisterDevices.checked,
      e.target.modifyManageAccounts.checked
    )
    setModifyAccountModal(false);
  }

  const toggle_permission = (permission_key) => {
    setRecoil(selectedAccountState, {
      ...selectedAccount,
      permissions: {
        ...selectedAccount.permissions,
        'permission_key': !selectedAccount.permissions['permission_key']
      }
    })
  }

  const handleSearchChange = event => {
    setSearchText(event.target.value);
  };

  return <>
    <Modal isOpen={newAccountModal}>
      <ModalHeader toggle={() => { setNewAccountModal(!newAccountModal) }}>Create New Account</ModalHeader>
      <ModalBody>

        <Form onSubmit={onFormSubmitAccount}>
          <legend>Details</legend>
          <FormGroup valid>
            <Label for="newEmail">Email*</Label>
            <Input type="email" name="email" id="newEmail" placeholder=""></Input>
            <Label for="newPassword">Password*</Label>
            <Input type="password" name="password" id="newPassword" placeholder=""></Input>
            <Label for="repeatNewPassword">Repeat Password*</Label>
            <Input type="password" name="password" id="repeatNewPassword" placeholder=""></Input>
          </FormGroup>
          <legend>Permissions</legend>
          <FormGroup check>
            <Label check>
              <Input id="newViewDevices" type="checkbox" />
              View Devices
            </Label>
          </FormGroup>
          <FormGroup check>
            <Label check>
              <Input id="newRegisterDevices" type="checkbox" />
              Register Devices
            </Label>
          </FormGroup>
          <FormGroup check>
            <Label check>
              <Input id="newManageAccounts" type="checkbox" />
              Manage Accounts
            </Label>
          </FormGroup>
          <Button type="submit">Submit</Button>
        </Form>

      </ModalBody>
    </Modal>

    {selectedAccount.id != null ?
      <Modal isOpen={modifyAccountModal}>
        <ModalHeader toggle={() => { setModifyAccountModal(!modifyAccountModal) }}>Modify Account</ModalHeader>
        <ModalBody>
          <CardText>{selectedAccount.email}</CardText>
          <Form onSubmit={onFormSubmitModifyAccount}>
            <legend>Change Permissions</legend>
            <FormGroup check>
              <Label check>
                <Input id="modifyViewDevices" type="checkbox"
                  defaultChecked={selectedAccount.permissions.view_devices}
                  onChange={() => toggle_permission('view_devices')}
                />
                View Devices
              </Label>
            </FormGroup>
            <FormGroup check>
              <Label check>
                <Input id="modifyRegisterDevices" type="checkbox"
                  defaultChecked={selectedAccount.permissions.register_devices}
                  onChange={() => toggle_permission('register_devices')} />
                Register Devices
              </Label>
            </FormGroup>
            <FormGroup check>
              <Label check>

                <Input id="modifyManageAccounts" type="checkbox"
                  defaultChecked={selectedAccount.permissions.manage_accounts}
                  onChange={() => toggle_permission('manage_accounts')} />
                Manage Accounts
              </Label>
            </FormGroup>
            <Button type="submit">Submit</Button>
          </Form>
          <Button className={css(accountsPageStyle.delete_button_style)}
            onClick={() => { account_manager.delete_account(selectedAccount.id); setModifyAccountModal(false) }}>
            Delete Account
          </Button>
        </ModalBody>
      </Modal> : <></>
    }

    <div className={css(accountsPageStyle.main_style)}>
      <Row className={css(accountsPageStyle.row_style)}>
        <Button className={css(accountsPageStyle.create_new_style)} onClick={() => { setNewAccountModal(true); }}>Create New</Button>
      </Row>
      <Row className={css(accountsPageStyle.row_style)}>
        <Input className={css(accountsPageStyle.search_style)} value={searchText} onChange={handleSearchChange} placeholder="Search Accounts"></Input>
      </Row>
      {
        accountList.accounts.filter(account => account.email.toLowerCase().includes(searchText.toLowerCase())).map(account => {
          return <>
            <Row className={css(accountsPageStyle.row_style)}>
              <Button className={css(accountsPageStyle.account_button_style)}
                onClick={() => { account_manager.select_account(account.id); setModifyAccountModal(true); }}>{account.email}</Button>
            </Row>
          </>
        })
      }
    </div>
  </>
}

const FleetMetricsPage = props => {
  return <></>
}


const appStyles = StyleSheet.create({
  app_style: {
    textAlign: "left",
    backgroundColor: '#1c1c1c'
  }
});

function App() {
  const navBarStyle = {
    height: sizes.header,
    background: colors.pale_red,
    margin: 0,
  };

  auth_manager.get_auth_key(() => { device_list_manager.get_device_list(); account_manager.get_account_list() });

  return (
    <div className={css(appStyles.app_style)} style={{ height: "100vh" }}>
      <Navbar style={navBarStyle}>
        <h1>Manhole Metrics Dashboard</h1>
      </Navbar>
      <DeviceMetricsPage style={{ height: "100%" }}></DeviceMetricsPage>
      {/* <AccountsPage style={{ height: "100%" }}></AccountsPage> */}
    </div>

  );
}

export default App;
