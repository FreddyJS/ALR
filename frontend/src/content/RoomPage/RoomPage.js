import React from 'react';

import { TextInput, Button, Tile } from 'carbon-components-react';

const RoomPage = () => {
  const [roomNumber, setRoomNumber] = React.useState('');

  return(
    <div className="room-page">
      <div className="room-page__header">
        <h1>ALR: Automated Leading Robot</h1>
        <p>Un guía de confianza para gente de todo tipo</p>
      </div>

      <Tile className="room-page__content">
        <h3>Introduce el número de habitación</h3>
        <TextInput id="room-number" type="text" value={roomNumber} placeholder="Nº de habitación" disabled/>

        <div className="room-page__keyboard">
          <div className="room-page__keyboard-row">
            <Button className="room-page__keyboard-button" onClick={() => setRoomNumber(roomNumber + "1")}>1</Button>
            <Button className="room-page__keyboard-button" onClick={() => setRoomNumber(roomNumber + "2")}>2</Button>
            <Button className="room-page__keyboard-button" onClick={() => setRoomNumber(roomNumber + "3")}>3</Button>
          </div>
          <div className="room-page__keyboard-row">
            <Button className="room-page__keyboard-button" onClick={() => setRoomNumber(roomNumber + "4")}>4</Button>
            <Button className="room-page__keyboard-button" onClick={() => setRoomNumber(roomNumber + "5")}>5</Button>
            <Button className="room-page__keyboard-button" onClick={() => setRoomNumber(roomNumber + "6")}>6</Button>
          </div>
          <div className="room-page__keyboard-row">
            <Button className="room-page__keyboard-button" onClick={() => setRoomNumber(roomNumber + "7")}>7</Button>
            <Button className="room-page__keyboard-button" onClick={() => setRoomNumber(roomNumber + "8")}>8</Button>
            <Button className="room-page__keyboard-button" onClick={() => setRoomNumber(roomNumber + "9")}>9</Button>
          </div>
        </div>
      </Tile>
    </div>
  )
};

export default RoomPage;
