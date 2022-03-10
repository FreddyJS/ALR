// import logo from './logo.svg';
import React from 'react';

import './App.scss';
import PageHeader from './components/PageHeader';

import { Route, Switch } from 'react-router-dom';
import { Content } from 'carbon-components-react';

import RoomPage from './content/RoomPage';

import Dashboard from './content/Dashboard';
import DashboardDev from './content/Dashboard/DashboardDev';

function App() {
  return (
    <>
      <PageHeader/>
      <Content>
        <div className="room-page__header">
          <h1>guiaMe: Automated Guiding Robot</h1>
          <p>Un guía de confianza para gente de todo tipo</p>
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
