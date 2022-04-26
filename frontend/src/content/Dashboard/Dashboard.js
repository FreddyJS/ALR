import React from 'react';
import Konva from 'konva';
import stage from './stage.json';
import background from './background.png';

import { Stage, Layer, Rect, Text, Image } from 'react-konva';
import { dashboardSocket } from '../../sockets';
import Crono from '../Crono/Crono';

const dSocket = dashboardSocket();
let halls = [];

const Dashboard = () => {
  const [hallId, setHallId] = React.useState('BASE');
  const stageRef = React.useRef(null);
  const rectRef = React.useRef(null);

  const backgroundImage = new window.Image();
  backgroundImage.src = background;

  var cont_inic = true;
  var cont_parar = false;
  var time = [];
  var time2 = [];

  dSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Dashboard Received: ", data);

    if (data.hall !== undefined) {
      rectRef.current.opacity(1);
      halls.push(data.hall);
      setHallId(data.hall);
    }

    if (data.active !== undefined && data.active && cont_inic) {
      document.getElementById("restart").click();
      document.getElementById("start").click();
      cont_inic = !cont_inic;
      cont_parar = !cont_parar;

    } else if (data.active !== undefined && !data.active && cont_parar) {
      document.getElementById("stop").click();
      var a = document.getElementById("timer").textContent;
      time = a.split(":");
      time2 = time[2].split(".")
      cont_parar = !cont_parar;
      cont_inic = !cont_inic;

      var requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ robot_id: 'R01', destiny: data.route.dest_room, minutes: time[1], seconds: time2[0], miliseconds: time2[1] })
      };

      try {
        fetch(
          'http://localhost:8000/api/stats/', requestOptions)
          .then(response => {
            response.json()
          })
      }
      catch (error) {
        console.error(error);
      }

    }
  };

  React.useEffect(() => {
    console.log(rectRef);
    if (rectRef.current !== null) {
      var period = 300;

      const anim = new Konva.Animation(frame => {
        if (rectRef.current !== null) {
          rectRef.current.opacity((Math.sin(frame.time / period) + 1) / 2);
        }

      }, rectRef.current.getLayer());

      anim.start();
      return () => {
        anim.stop();
      };
    }
  }, []);

  return (
    <>
      <Crono id="crono"></Crono>
      <Stage width={stage.stageWidth} height={stage.stageHeight} ref={stageRef}>
        {stage.layers.map((layer, index) => {
          return (
            <Layer key={index}>
              {index === 0 && <Image image={backgroundImage} width={1280} height={720} />}

              {layer.elements.map((element, index) => {
                if (element.type === "Rect") {
                  let inPath = false;
                  inPath = halls.find((hall) => element.attrs.id === hall) ? true : false;
                  inPath = inPath || element.attrs.id === hallId;

                  if (element.attrs.id === "BASE")
                    inPath = false; //Si es el HALL inicial lo dejamos en cian
                  if (hallId === "BASE" && halls.length !== 0) {
                    halls.splice(0, halls.length);
                    halls.splice(0, halls.length); //Al volver al HALL (id="hall0") vaciamos array de halls -> "reiniciamos"
                  }
                  return <Rect key={index} {...element.attrs} fill={inPath === true ? "green" : element.attrs.fill} ref={element.attrs.id === hallId ? rectRef : null} />;
                } else if (element.type === "Text") {
                  return <Text key={index} {...element.attrs} />;
                }

                return null;
              })}
            </Layer>
          );
        }
        )}
      </Stage></>
  );
};

export default Dashboard;