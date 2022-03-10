import React from 'react';

import { RobotSocket, UISocket } from '../../sockets';
import { Button, Tile, Modal } from 'carbon-components-react';

const RoomPage = () => {
  const [roomNumber, setRoomNumber] = React.useState('');
  const [isModalOpen, setIsModalOpen] = React.useState(false);

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

  return(
    <div className="room-page">
      <div style={{display: "flex", flexDirection: "row", justifyContent: "center", alignItems: "center"}}>
        <Button style={{margin: "0.1rem"}} onClick={() => sendHelllo("UI")}> Client Message </Button>
        <Button style={{margin: "0.1rem"}} onClick={() => sendHelllo("Robot")}> Robot Message </Button>    
      </div>

      {isModalOpen && (
        <Modal
          open={isModalOpen}
          onRequestClose={() => setIsModalOpen(false)}
          modalHeading="Confirmar destino"
          primaryButtonText="Submit"
        >
          <div> 
            <h1>Ir a la habitación {roomNumber}?</h1>
            <img src="https://i.etsystatic.com/17441626/r/il/362050/1469060776/il_fullxfull.1469060776_e867.jpg" alt='room'/>
          </div>
        </Modal>
      )}

      <Tile className="room-page__content">
        {roomNumber === "" ? <h3>Introduce el número de habitación</h3> : <h3>Habitación: {roomNumber}</h3>}        
        {/* <TextInput id="room-number" type="text" value={roomNumber} placeholder="Nº de habitación" disabled/> */}

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
          <div className="room-page__keyboard-row">
            <Button className="room-page__keyboard-button" onClick={() => setRoomNumber("")}>Reset</Button>
            <Button className="room-page__keyboard-button" onClick={() => setRoomNumber(roomNumber + "0")}>0</Button>
            <Button className="room-page__keyboard-button" onClick={() => setIsModalOpen(true)}>OK</Button>
          </div>
        </div>
      </Tile>
    </div>
  )
};

export default RoomPage;
