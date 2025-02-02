import React from 'react';
import robot from './robot.png'

import { createUISocket, RobotSocket } from '../../sockets';
import { Button, Tile, Modal } from 'carbon-components-react';

import { getRoutes } from '../../services/routes';
import RoomInput from '../../components/RoomInput';
import {
  AiOutlineArrowUp,
  AiOutlineArrowRight,
  AiOutlineArrowDown,
  AiOutlineArrowLeft,
  AiFillStop
} from "react-icons/ai";

const RoomPage = () => {
  const debug = false;
  const [roomNumber, setRoomNumber] = React.useState('');
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const [wrongRoomNumber, setWrongRoomNumber] = React.useState(false);
  const [route, setRoute] = React.useState();
  const [inPath, setInPath] = React.useState(false);
  const [nextDirection, setNextDirection] = React.useState('');
  const [socket,] = React.useState(createUISocket("PiCar"));

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const message = data.message;
    console.log("RoomPage Received: ", data);
    if (message === undefined || message.type === undefined) {
      return;
    }

    if (message.type === "next_direction") {
      for (let i = 0; i < route["route"].length; i++) {
        if (route["route"][i].includes("CRUCE")) {
          setNextDirection(route.route[i]);
          break;
        }
      }
    } else if (message.type === "finished_route") {
      setNextDirection('stop');
      setTimeout(() => {
        setInPath(false);
      }, 5000);
    }
  }

  const sendHelllo = (from) => {
    const data = {
      type: from === 'UI' ? 'to.robot' : 'to.ui',
      message: "Hello from " + from,
    };

    if (from === "UI") {
      socket.send(JSON.stringify(data));
    } else {
      RobotSocket.send(JSON.stringify(data));
    }
  };

  const onRoomSubmit = async () => {
    if (roomNumber === 'BLE') {
      const data = {
        type: 'to.robot',
        message: {
          type: 'bluetooth'
        }
      }

      socket.send(JSON.stringify(data));
      return;
    }

    const routes = await getRoutes();
    const route = routes.find(r => r.dest_room === roomNumber && r.origin_room === 'hall');

    if (route) {
      console.log("Route:", route);
      setRoute(route);
      setIsModalOpen(true);
    } else {
      setWrongRoomNumber(true);
    }
  };

  const onModalSubmit = () => {
    setInPath(true);
    for (let i = 0; i < route["route"].length; i++) {
      if (route["route"][i].includes("CRUCE")) {
        setNextDirection(route.route[i]);
        break;
      }
    }

    const data = {
      type: 'to.robot',
      message: {
        type: 'start',
        room: roomNumber,
        route: route
      }
    };

    socket.send(JSON.stringify(data));
    setIsModalOpen(false);
  };

  return (
    <div className="room-page">
      {debug &&
        <div style={{ display: "flex", flexDirection: "row", justifyContent: "center", alignItems: "center", marginBottom: "10px" }}>
          <Button style={{ margin: "0.1rem" }} onClick={() => sendHelllo("UI")}> Client Message </Button>
          <Button style={{ margin: "0.1rem" }} onClick={() => sendHelllo("Robot")}> Robot Message </Button>
        </div>
      }

      {isModalOpen && (
        <Modal
          open={isModalOpen}
          onRequestClose={() => setIsModalOpen(false)}
          onRequestSubmit={() => onModalSubmit()}
          modalHeading="Confirmar destino"
          primaryButtonText="Submit"
        >
          <div>
            <h1>Ir a la habitación {roomNumber}?</h1>
            <img src="https://i.etsystatic.com/17441626/r/il/362050/1469060776/il_fullxfull.1469060776_e867.jpg" alt='room' />
          </div>
        </Modal>
      )}

      <Tile className="room-page__content">
        {roomNumber === "" ? <h3>Introduce o número da habitación</h3> : <h3>Habitación: {roomNumber}</h3>}
        {wrongRoomNumber && <h3 style={{ color: "red" }}>Non existe a habitación</h3>}
        {/* <TextInput id="room-number" type="text" value={roomNumber} placeholder="Nº de habitación" disabled/> */}

        {!inPath ?
          <RoomInput onSubmit={() => onRoomSubmit()} onChange={(room) => { setRoomNumber(room); setWrongRoomNumber(false); }} value={roomNumber} />
          :
          <div>
            {nextDirection === 'stop' ?
              <>
                <h4>Chegou ao destino</h4>
                <AiFillStop style={{ width: "70%", height: "70%", fill: "green" }} onClick={() => window.location.reload()} />
              </>
              :
              <h4>No próximo cruce: <strong>{nextDirection.split(".")[0]}</strong></h4>
            }

            {nextDirection.startsWith('recto') && <AiOutlineArrowUp style={{ width: "70%", height: "70%", fill: "green" }} />}
            {nextDirection.startsWith('derecha') && <AiOutlineArrowRight style={{ width: "70%", height: "70%", fill: "green" }} />}
            {nextDirection.startsWith('vuelta') && <AiOutlineArrowDown style={{ width: "70%", height: "70%", fill: "green" }} />}
            {nextDirection.startsWith('izquierda') && <AiOutlineArrowLeft style={{ width: "70%", height: "70%", fill: "green" }} />}
          </div>
        }

      </Tile>
      <img src={robot} alt="robot" />
    </div>
  )
};

export default RoomPage;
