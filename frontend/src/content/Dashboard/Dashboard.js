import React from 'react';
import Konva from 'konva';
import stage from './stage.json';
import { Stage, Layer, Rect, Text } from 'react-konva';

const Dashboard = () => {
  const stageRef = React.useRef(null);
  const rectRef = React.useRef(null);
  const hall = 0;

  React.useEffect(() => {
    if (rectRef.current !== null) {
      var period = 300;
  
      var anim = new Konva.Animation(frame => {
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
    <Stage width={stage.stageWidth} height={stage.stageHeight} ref={stageRef}>
      {stage.layers.map((layer, index) => {
        const hallId = "hall" + hall;

        return (
          <Layer key={index}>
            {layer.elements.map((element, index) => {
              if (element.type === "Rect") {
                return <Rect key={index} {...element.attrs} fill={element.attrs.id === hallId ? "orange" : element.attrs.fill } ref={element.attrs.id === hallId ? rectRef : null} />; 
              } else if (element.type === "Text") {
                return <Text key={index} {...element.attrs} />
              }

              return null;
            })}
          </Layer>
        );
      }
      )}
    </Stage>
  );
};

export default Dashboard;