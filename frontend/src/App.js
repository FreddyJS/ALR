// import logo from './logo.svg';
import React from 'react';
import './App.scss';
import { Content } from 'carbon-components-react';
import PageHeader from './components/PageHeader';
import { Route, Switch } from 'react-router-dom';
import { Button } from 'carbon-components-react';

import HomePage from './content/HomePage';
import CounterPage from './content/CounterPage';
import RoomPage from './content/RoomPage';
import { RobotSocket, UISocket } from './sockets';

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
          <Route exact path="/" component={HomePage} />
          <Route path="/counter" component={CounterPage} />
          <Route path="/room" component={RoomPage} />
        </Switch>
      </Content>
    </>
  );

}

export default App;
