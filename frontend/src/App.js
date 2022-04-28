// import logo from './logo.svg';
import React from 'react';

import './App.scss';
import PageHeader from './components/PageHeader';

import { Route, Switch } from 'react-router-dom';
import { Content } from 'carbon-components-react';

import RoomPage from './content/RoomPage';

import Dashboard from './content/Dashboard';
import DashboardDev from './content/Dashboard/DashboardDev';
import Stats from './content/Stats/Stats';

import logo from './images/logo_guiame.jpg'

function App() {
  return (
    <>
      {!window.location.href.includes("room") && <PageHeader/>}
      <Content>
        <div className="room-page__header">
        <h1><img src={logo} alt='descripcion' style={{ maxWidth: "100%" }}/></h1>
        </div>
        <Switch>
          <Route exact path="/" component={Dashboard} />
          <Route exact path="/mapdev" component={DashboardDev} />
          <Route exact path="/room" component={RoomPage} />
          <Route exact path="/stats" component={Stats} />
        </Switch>
      </Content>
    </>
  );
}

export default App;
