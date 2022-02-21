// import logo from './logo.svg';
import React from 'react';
import './App.scss';
import { Content } from 'carbon-components-react';
import PageHeader from './components/PageHeader';
import { Route, Switch } from 'react-router-dom';

import HomePage from './content/HomePage';
import CounterPage from './content/CounterPage';
import RoomPage from './content/RoomPage';

function App() {
  return (
    <>
      <PageHeader/>
      <Content>
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