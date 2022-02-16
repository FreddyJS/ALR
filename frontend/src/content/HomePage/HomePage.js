import React from 'react';
import logo from '../../logo.svg'

const HomePage = () => {
  return(
    <div className="App">
      <h1>React App with Carbon Design Components</h1>
      <br/>
      <h2>Using React Redux and reduxjs/toolkit</h2>
      <img className="App-logo" src={logo} alt="React logo"></img>
      <p>Hot deployment for reducers and components!</p>
    </div>
  )
};

export default HomePage;
