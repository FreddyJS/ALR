// import logo from './logo.svg';
import React from 'react';

import './App.scss';
import PageHeader from './components/PageHeader';

import { Route, Switch } from 'react-router-dom';
import { Content, Button } from 'carbon-components-react';

import RoomPage from './content/RoomPage';
import { RobotSocket, UISocket } from './sockets';

import Dashboard from './content/Dashboard';
import DashboardDev from './content/Dashboard/DashboardDev';

function App() {
  const sendHelllo = (from) => {
    const data = {
      type: from === 'UI' ? 'to.robot' : 'to.ui',
      message: "Hello from " + from,
    };

    if (from === "UI") {
      UISocket.send(JSON.stringify(data));
    } else {
      RobotSocket.send(JSON.stringify(data));
    }
  };

  return (
    <>
      <PageHeader/>
      <Content>
        <div style={{display: "flex", flexDirection: "row", justifyContent: "center", alignItems: "center"}}>
          <Button style={{margin: "0.1rem"}} onClick={() => sendHelllo("UI")}> Client Message </Button>
          <Button style={{margin: "0.1rem"}} onClick={() => sendHelllo("Robot")}> Robot Message </Button>    
        </div>

        <Switch>
          <Route exact path="/" component={Dashboard} />
          <Route exact path="/mapdev" component={DashboardDev} />
          <Route exact path="/room" component={RoomPage} />
        </Switch>
      </Content>
    </>
  );

}

export default App;
