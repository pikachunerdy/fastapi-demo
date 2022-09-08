import logo from './logo.svg';
import './App.css';
import { StyleSheet, css } from 'aphrodite';
import "bootstrap/dist/css/bootstrap.min.css";
import {
  useRecoilState,
  useRecoilValue,
  useSetRecoilState,
} from 'recoil';
import { deviceListState, authState, panelSizes, selectedDeviceState, accountListState, selectedAccountState, companyState, filterState } from './atoms.js';
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
  Modal, ModalHeader, ModalBody, ModalFooter, FormGroup, Label, Input, TextArea, Dropdown, DropdownItem, DropdownMenu, UncontrolledDropdown,
  DropdownToggle
} from "reactstrap";
import React, { useState, memo, useEffect, Component, useRef } from "react";
import SplitPane from "react-split-pane";
import Pane from "react-split-pane";
import MapContainer from './Map';
import { auth_manager, device_list_manager, account_manager, company_manager } from './managers';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';

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
    backgroundColor: '#1c1c1c',
    borderColor: '#1c1c1c',
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
    backgroundColor: '#232223',
    borderColor: '#232223',
    display: 'flex'

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
    border: '1px solid #999999',
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
  }
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
    backgroundColor: '#1c1c1c',
    borderColor: '#1c1c1c',
    paddingTop: 0,
    marginTop: 0,
    overflow: 'scroll'
  },
  card_body_style: {
    ...styles.card_style,
    backgroundColor: '#232223',
    borderColor: '#232223',
    paddingTop: 0,
    marginTop: 0,
    marginLeft: 0,
    paddingLeft: 10,
    paddingRight: 0,
    overflow: 'scroll'

  },
  container_styles: {
  },
  col_styles: {
    ...styles.col_styles,
    minWidth: 'fit-content'
  },
  label_col_style: {
    // ...styles.col_styles,
    // maxWidth: 50,
    paddingTop: 12,
    paddingBottom: 12,
    paddingLeft: 0,
    paddingRight: 0,
    margin: 0,
    maxWidth: 'fit-content',
  },
  label_badge_style: {
    // ...styles.col_styles,
    // maxWidth: 50,
    height: '100%',
    paddingTop: 8,
    paddingBottom: 8,
    maxWidth: 'fit-content',
    color: 'black',
    backgroundColor: '#ababab',
    marginRight: 5,
    marginLeft: 5,
  },
  row_styles: {
    ...styles.row_styles,
    marginLeft: 0,
    marginRight: 0
  },
  button_styles: {
    ...styles.button_styles
  },
  filter_button_styles: {
    ...styles.button_styles,
    width: '10em',
    paddingTop: 4,
    paddingBottom: 4,
    float: 'right'
  },
  disabled_filter_style: {
    ...modified_styles.unpinned_button_styles,
    width: '10em',
    paddingTop: 4,
    paddingBottom: 4,
    float: 'right'
  },
  unpinned_button_style: {
    ...modified_styles.unpinned_button_styles,
  },
  search_style: {
    marginLeft: 10,
    marginTop: 5,
    height: '2em',
    width: '20em',
    float: 'right'
  },
  header_text_style: {
    margin: 0,
    padding: 0
  },
  header_styles: {
    ...styles.header_styles,
    backgroundColor: '#1c1c1c',
    borderColor: '#1c1c1c',
    paddingTop: 0,
    marginTop: 0,
    marginBottom: 0,
    paddingBottom: 10,
    marginLeft: 0,
    paddingLeft: 0
  },

  checked_button_style: {
    padding: 0,
    paddingLeft: 5,
    paddingRight: 5,
    float: 'right',
    // marginTop: 5,
  },

  unchecked_button_style: {
    padding: 0,
    paddingLeft: 5,
    paddingRight: 5,
    float: 'right',
    backgroundColor: 'white',
    color: 'gray',
  },
  label_toggle_style: {
    width: '10em',
    paddingTop: 4,
    paddingBottom: 4,
    float: 'right',
    paddingRight: 5,
  },
  drop_down_style: {
    marginLeft: 5,
    marginTop: 5,
    // maxWidth: 800,
  },
  drop_down_menu_style: {
    width: 400,
    minWidth: 400,
    // maxWidth: 800,
  },

  delete_button_style: {
    // height: 20,
    padding: 0,
    paddingLeft: 5,
    paddingRight: 5,
    // paddingBottom: 5,
    backgroundColor: 'red',
    borderColor: 'red',
    float: 'right',
  }
});

const DeviceListComponent = (args) => {
  const company = useRecoilValue(companyState);
  const [filter, setFilterState] = useRecoilState(filterState);
  const deviceList = useRecoilValue(deviceListState);
  const [deviceSearchText, setDeviceSearchText] = useState('');
  return <Card className={css(deviceListComponentStyles.card_style)} style={{ height: '100%' }}>
    <CardHeader className={css(deviceListComponentStyles.header_styles)}>
      <CardText className={css(deviceListComponentStyles.header_text_style)}>Devices</CardText>
      <Input className={css(deviceListComponentStyles.search_style)} placeholder="Search Devices"
        value={deviceSearchText} onChange={(event) => setDeviceSearchText(event.target.value)} ></Input>
      <Button className={css(filter.pinned ? deviceListComponentStyles.filter_button_styles : deviceListComponentStyles.disabled_filter_style)}
        onClick={() => setFilterState({ ...filter, pinned: !filter.pinned })}>Filter Pinned</Button>
      <UncontrolledDropdown className={css(deviceListComponentStyles.drop_down_style)}>
        <DropdownToggle
          caret
          color="dark"
          className={css(deviceListComponentStyles.label_toggle_style)}
        >
          Filter With Labels
        </DropdownToggle>
        <DropdownMenu dark className={css(deviceListComponentStyles.drop_down_menu_style)}>
          {company.labels.map((label) => {
            return <DropdownItem text>
              <Row>
                <Col><CardText>{label}</CardText></Col>
                <Col>
                  <Button
                    className={css(
                      filter.labels.includes(label) ?
                        deviceListComponentStyles.checked_button_style :
                        deviceListComponentStyles.unchecked_button_style
                    )}
                    onClick={() => {
                      if (filter.labels.includes(label)) {
                        setFilterState({
                          ...filter,
                          labels: [...filter.labels].filter((item) => item !== label)
                        })
                      }
                      else {
                        setFilterState({
                          ...filter,
                          labels: [...filter.labels, label]
                        })
                      }
                    }}>
                    {filter.labels.includes(label) ? 'Selected' : 'Select'}
                  </Button>
                </Col>
                <Col>
                  <Button className={css(deviceListComponentStyles.delete_button_style)}
                    onClick={() => { company_manager.delete_label(label) }}>
                    Delete
                  </Button>
                </Col>
              </Row>
            </DropdownItem>
          })}
        </DropdownMenu>
      </UncontrolledDropdown>
    </CardHeader>
    <CardBody className={css(deviceListComponentStyles.card_body_style)}>
      {
        deviceList.devices.filter(device => device.device_id.toLowerCase().includes(deviceSearchText.toLowerCase()))
          .filter(device => device.pinned || !filter.pinned)
          .map((device) => {
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
                    {
                      device.labels.map((label) => {
                        return <Col xs="3" className={css(deviceListComponentStyles.label_col_style)} >
                          <Badge className={css(deviceListComponentStyles.label_badge_style)}>{label}</Badge>
                        </Col>
                      })
                    }
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
                // overflowY: "scroll"
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

const label_spacing = 10;
const card_body_padding_right = 15;
const deviceInfoPanelStyles = StyleSheet.create({
  card_style: {
    ...styles.card_style,
    backgroundColor: '#232223',
    borderColor: '#232223',
    // overflowY: "scroll",
    height: '100%'
  },
  labels_card_style: {
    backgroundColor: '#232223',
    borderColor: '#232223',
    overflowY: "scroll",
    height: 'auto',
    maxHeight: 400,
    borderRadius: 3,
    marginLeft: 5,
    paddingTop: 0,
    paddingBottom: 0,
    borderColor: '#999999',
  },
  labels_card_body_style: {
    paddingTop: label_spacing,
    paddingBottom: 0,
  },
  card_body_style: {
    ...styles.card_style,
    backgroundColor: '#232223',
    borderColor: '#232223',
    paddingTop: 0,
    marginTop: 0,
    paddingLeft: 0,
    paddingRight: card_body_padding_right,
    overflowY: "scroll",
    height: '100%'
  },
  container_styles: {
    overflowY: "scroll"
  },
  header_styles: {
    ...styles.header_styles
  },
  row_styles: {
    ...styles.row_styles,
    marginLeft: 0,
    marginRight: 0
  },
  text_style: {
    ...styles.text_style
  },
  label_text_style: {
    // ...styles.text_style,
    maxWidth: 300,
    minWidth: 100,
    width: 'auto',
    height: 35,
    padding: 3,
    paddingTop: 8,
    margin: 5,
    fontSize: 15,
    marginTop: 0,
    marginBottom: label_spacing,
    paddingLeft : 5,
    paddingRight : 5,
  },
  button_styles: {
    ...styles.button_styles,
    marginLeft: 5,
    marginBottom: 10,
  },
  remove_button_styles: {
    ...styles.button_styles,
    marginLeft: 5,
    marginTop: 0,
    marginBottom: label_spacing,
    // marginBottom: 10,
    height: 35,
    padding: 3,
    width: 80,
    background: 'red',
    borderColor: 'red',
    float : 'right',
  },
  comment_button_styles: {
    ...styles.button_styles,
    display: 'block',
    clear: 'right'
  },
  unpinned_button_styles: {
    ...modified_styles.unpinned_button_styles,
    marginLeft: 5,
    marginBottom: 10,
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
    width: '4em',
    marginBottom: 10,
  },
  chart_style: {
    margin: 0,
    padding: 0,
  },
  comments_style: {
    backgroundColor: '#232223',
    borderColor: '#999999',
    borderWidth: 2,
    marginLeft: 5,
    borderRadius: 6,
    width: '100%',
    color: '#999999',
    marginBottom: 10,
    padding: 5,
    maxHeight: 300
  },
  warning_level_style: {
    width: '10em',
    backgroundColor: '#232223',
    borderColor: '#999999',
    borderWidth: 2,
    marginLeft: 5,
    borderRadius: 6,
    color: '#999999',
    marginBottom: 10,
    padding: 5,
    // height: 40,
  },
  add_label_dropdown_button_style: {
    marginLeft: 5,
    marginTop: 5,
  },
});

const DeviceInfoPanel = (args) => {
  const company = useRecoilValue(companyState);
  const selectedDevice = useRecoilValue(selectedDeviceState);
  const panel = useRecoilValue(panelSizes);
  const [newLabelModal, setNewLabelModal] = useState(false);
  const [newLabelText, setNewLabelText] = useState('');
  const [commentChanges, setCommentChanged] = useState(false);
  const [warningLevelChanged, setWarningLevelChanged] = useState(false);
  const [warningLevel, setWarningLevel] = useState('');
  const [commentText, setCommentText] = useState('');
  const width = parseInt(panel.vRight, 10) - 70 - card_body_padding_right;
  const [deviceID, setDeviceID] = useState('');
  if (!(deviceID === selectedDevice.device_id)) {
    setDeviceID(selectedDevice.device_id);
    setCommentText(selectedDevice.comments);
    setWarningLevel(selectedDevice.warning_level_height_mm);
    setCommentChanged(false);
    setWarningLevelChanged(false);
  }

  const text_area = useRef(null);

  <textarea id='commentTextAreaBlockInfo' className={css(deviceInfoPanelStyles.comments_style)} value={commentText} onChange={(event) => { setCommentChanged(!(event.target.value === selectedDevice.comments)); setCommentText(event.target.value); }} ></textarea>;

  useEffect(() => {
    if (text_area.current != null) {
      text_area.current.style.height = "";
      text_area.current.style.height = text_area.current.scrollHeight + 'px';
    }
  });

  const changePeriodType = (periodType) => {
    device_list_manager.select_device(selectedDevice.device_id, periodType);
  };

  if (!(selectedDevice.device_id)) {
    return <>
    </>
  }
  var date = new Date(parseInt(selectedDevice.creation_date) * 1000);
  const dateStr = date.getDate() + '/' + date.getMonth() + '/' + date.getFullYear();
  return <>
    <Modal isOpen={newLabelModal} style={{
      width: '300px',
      height: '300px',
      position: 'absolute',
      left: ' 50%',
      top: '50%',
      marginLeft: '-150px',
      marginTop: '-150px',
    }}>
      <ModalHeader toggle={() => { setNewLabelModal(!newLabelModal) }}>Create New Label</ModalHeader>
      <ModalBody>
        <Input value={newLabelText} onChange={(event) => { setNewLabelText(event.target.value); }}></Input>
        <Button style={{ marginTop: 20 }} onClick={() => {
          company_manager.create_label(newLabelText);
          setNewLabelModal(false);
          setNewLabelText("");
        }}>Save</Button>
      </ModalBody>
    </Modal>
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
        {/* labels */}
        <CardText className={css(deviceInfoPanelStyles.text_style)}>
          Labels:
        </CardText>
        <Card className={css(deviceInfoPanelStyles.labels_card_style)}>
          <CardBody className={css(deviceInfoPanelStyles.labels_card_body_style)}>
            {selectedDevice.labels.map((label) => {
              return <>
                <Row>
                  <Badge className={css(deviceInfoPanelStyles.label_text_style)}>{label}</Badge>
                  <Button className={css(deviceInfoPanelStyles.remove_button_styles)}
                    onClick={async () => {
                      await company_manager.remove_device_label(selectedDevice.device_id, label);
                      await device_list_manager.get_device_list(() => { device_list_manager.select_device(selectedDevice.device_id)});}}
                  >Remove</Button>
                </Row>
              </>
            })}
          </CardBody>
        </Card>
        <UncontrolledDropdown className={css(deviceInfoPanelStyles.add_label_dropdown_button_style)}>
          <DropdownToggle
            caret
            color="dark"
          >
            Add Label
          </DropdownToggle>
          <DropdownMenu dark>
            {company.labels.map((label) => {
              return <DropdownItem onClick={async () => {
              await company_manager.add_device_label(selectedDevice.device_id, label);
              await device_list_manager.get_device_list(() => { device_list_manager.select_device(selectedDevice.device_id)});
              }}>
                {label}
              </DropdownItem>
            })}
            <DropdownItem divider />
            <DropdownItem onClick={() => setNewLabelModal(true)}>
              Create New Label
            </DropdownItem>
          </DropdownMenu>
        </UncontrolledDropdown>
        {/* warning level height */}
        <CardText className={css(deviceInfoPanelStyles.text_style)}>
          Warning Level Height: <input className={css(deviceInfoPanelStyles.warning_level_style)} value={warningLevel} onChange={(event) => {
            setWarningLevel(event.target.value); setWarningLevelChanged(true);
          }}></input>
        </CardText>
        {warningLevelChanged ? <Button className={css(deviceInfoPanelStyles.comment_button_styles)}
          onClick={() => {
            device_list_manager.change_device_warning_level_height(selectedDevice.device_id, warningLevel);
            setWarningLevelChanged(false);
          }}>
          Save
        </Button> : <></>}
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
        <div style={{ width: '100%', paddingRight: 7 }}>
          <textarea id='commentTextAreaBlockInfo' className={css(deviceInfoPanelStyles.comments_style)} value={commentText} onChange={(event) => { setCommentChanged(!(event.target.value === selectedDevice.comments)); setCommentText(event.target.value); }} ref={text_area}></textarea>
        </div>
        {commentChanges ? <Button className={css(deviceInfoPanelStyles.comment_button_styles)}
          onClick={() => {
            device_list_manager.change_device_comments(selectedDevice.device_id, commentText);
            setCommentChanged(false);
          }}>
          Save
        </Button> : <></>}
        {/* <Card>
            {selectedDevice.comments.map(comment => <CardText>comment</CardText>)}
          </Card> */}
        {/* <CanvasJSChart options = {chart_options} ></CanvasJSChart> */}
        <CardText className={css(deviceInfoPanelStyles.text_style)}>
          Distance Measurements (mm):
        </CardText>
        <LineChart className={css(deviceInfoPanelStyles.chart_style)} width={width} height={400} data={selectedDevice.measurements}>
          <Line type="monotone" dataKey="distance_mm" stroke="#8884d8" />
          <CartesianGrid stroke="#ccc" />
          <XAxis dataKey="time_s" />
          {/* <YAxis label={{ value: 'Height (mm)', angle: -90, position: 'insideLeft', fill: '#6a6f71' }} /> */}
          <YAxis width={30}></YAxis>
          <Tooltip />
        </LineChart>
        <Row className={css(deviceInfoPanelStyles.text_style)}>
          {[['day', 'Day'], ['week', 'Week'], ['month', 'Month'], ['year', 'Year']].map(([key, label]) => {
            return <Button className={css(selectedDevice.measurement_period_type === key ?
              deviceInfoPanelStyles.selected_switch_button_styles : deviceInfoPanelStyles.switch_button_styles)}
              onClick={() => { changePeriodType(key) }}>
              {label}
            </Button>
          })}
        </Row>
      </CardBody>
    </Card>
  </>
}

const VerticalSplit = props => {
  const vh =
    Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0) -
    sizes.header;
  const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
  const [leftWidth, setLeftWidth] = useState(parseInt(vw * 0.6).toString() + "px");
  const [rightWidth, setRightWidth] = useState(parseInt(vw * 0.4).toString() + "px");

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
        <Pane minSize="10%" maxSize="90%" style={{ overflowY: "scroll", height: '100%' }}>
          <div style={{ height: '100%' }}>
            <DeviceInfoPanel style={{ height: '100%' }}></DeviceInfoPanel>
          </div>
        </Pane>
      </SplitPane>
    </>
  );
};

const DeviceMetricsPage = props => {
  return <VerticalSplit style={{ height: "100%" }}></VerticalSplit>
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
    width: '40em',
    marginLeft: 0,
    marginRight: 0,
    background: '#2d2d2d',
    borderColor: '#b6b6b6',
    marginBottom: 20,
    textAlign: 'left',
  },
  search_style: {
    width: '45em',
    paddingRight: '10em',
    paddingLeft: '0em',
    marginLeft: '0em',
    marginRight: '0em',
    marginBottom: 30
  },
  delete_button_style: {
    backgroundColor: "#ff4545",
    borderColor: "#ff4545",
    marginTop: 15,
  },
  submit_button_style: {
    marginTop: 10,
  },
});

const AccountsPage = props => {
  const accountList = useRecoilValue(accountListState);
  const selectedAccount = useRecoilValue(selectedAccountState)
  const [newAccountModal, setNewAccountModal] = useState(false);
  const [modifyAccountModal, setModifyAccountModal] = useState(false);
  const [searchText, setSearchText] = useState("");


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
          {/* submit */}
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
            <Button type="submit" className={css(accountsPageStyle.submit_button_style)}>Submit</Button>
          </Form>
          {/* delete */}
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
                onClick={() => { account_manager.select_account(account.id, () => { setModifyAccountModal(true); }); }}>{account.email}</Button>
            </Row>
          </>
        })
      }
    </div>
  </>
}

const login_page_styles = StyleSheet.create({
  form_styles: {
    display: 'inline-block',
    paddingTop: 100,
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%'
  },
  form_items: {
    clear: 'right',
    width: '20em',
    margin: 'auto',
    marginBottom: 10
  },
  form_button: {
    clear: 'right',
    width: '20em',
    margin: 'auto',
    display: 'inline-block'
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
    paddingRight: 0,
    paddingLeft: 0,
    marginLeft: 25,
    borderColor: '#2db4f7',
    marginTop: 50,
    marginBottom: 20,
    width: '20em'
  },
  invalid_credentials_style: {
    textAlign: 'center',
    clear: 'right',
    width: '20em',
    margin: 'auto',
    display: 'inline-block',
    color: '#e35f5f',
  },

});

const LoginPage = props => {

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const auth = useRecoilValue(authState);




  return <>
    <Form className={css(login_page_styles.form_styles)} >
      <FormGroup>
        <Input className={css(login_page_styles.form_items)} value={email} onChange={(event) => setEmail(event.target.value)} placeholder="email"></Input>
        <Input className={css(login_page_styles.form_items)} type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="password"></Input>
      </FormGroup>
      <Row className={css(login_page_styles.row_style)}>
        {auth.showInvalidCredWarning ? <>
          <p className={css(login_page_styles.invalid_credentials_style)}>Invalid Credentials</p>
        </> : <></>}
      </Row>
      <Row className={css(login_page_styles.row_style)}>
        <Button className={css(login_page_styles.create_new_style)} onClick={() => {
          auth_manager.get_auth_key(email, password, () => {
            device_list_manager.get_device_list(); account_manager.get_account_list()
          });
        }}>Login</Button>
      </Row>
      {/* <Button className={css(login_page_styles.form_button)} type="submit">Submit</Button> */}
    </Form>
  </>
}

const appStyles = StyleSheet.create({
  app_style: {
    textAlign: "left",
    backgroundColor: '#1c1c1c'
  },
  nav_button_styles: {
    display: 'inline-block',
    float: 'right',
    borderColor: '#aad8e2',
    paddingTop: 0,
    paddingBottom: 0,
    marginLeft: 10,
    height: 40,
    marginTop: 5
  },
  nav_header_styles: {
    marginRight: 20,
    marginLeft: 10
  },
  nav_bar_styles: {
    justifyContent: 'left',
    alignItems: 'left',
    display: 'flex',
    height: sizes.header,
    background: colors.pale_red,
    margin: 0,
    paddingTop: 5,
  },

  logout_button: {
    display: 'inline-block',
    float: 'right',
    borderColor: '#aad8e2',
    paddingTop: 0,
    paddingBottom: 0,
    marginLeft: 10,
    height: 40,
    marginTop: 5
  },
});

const MainPage = props => {
  const [navState, setNavState] = useState('device-metrics');

  const vh =
    Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0) -
    sizes.header;
  const pageHeight = ((parseInt(vh) - sizes.header).toString() + "px");

  var page = <></>;

  switch (navState) {
    case 'device-metrics':
      page = <DeviceMetricsPage style={{ height: "100%" }}></DeviceMetricsPage>;
      break;
    case 'accounts-page':
      page = <AccountsPage style={{ height: "100%" }}></AccountsPage>;
      break;
  }
  return (
    <div className={css(appStyles.app_style)} style={{ height: "100vh" }}>
      <div className={css(appStyles.nav_bar_styles)}>
        <h1 className={css(appStyles.nav_header_styles)}>Manhole Metrics Dashboard</h1>
        <Button className={css(appStyles.nav_button_styles)} onClick={() => setNavState('device-metrics')}>Device Metrics Page</Button>
        <Button className={css(appStyles.nav_button_styles)} onClick={() => setNavState('accounts-page')}>Accounts Page</Button>
        <Button className={css(appStyles.logout_button)} onClick={() => auth_manager.logout()}>Logout</Button>
      </div>
      <div style={{ height: pageHeight }}>{page}</div>
    </div>);
}

const FilterStateComponent = props => {
  const filter = useRecoilValue(filterState);
  device_list_manager.get_device_list();

  return <MainPage></MainPage>;
}

function App() {
  const auth = useRecoilValue(authState);

  if (!auth.validToken) {
    auth_manager.check_token();
  }
  else {
    device_list_manager.get_device_list();
    account_manager.get_account_list();
    company_manager.setup();
  }
  if (!auth.validToken) {
    return (
      <div className={css(appStyles.app_style)} style={{ height: "100vh" }}>
        <div className={css(appStyles.nav_bar_styles)}>
          <h1 className={css(appStyles.nav_header_styles)}>Manhole Metrics Dashboard</h1>
        </div>
        <LoginPage></LoginPage>
      </div>
    )
  }
  return (<FilterStateComponent></FilterStateComponent>);
}

export default App;
