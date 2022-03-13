import React from 'react';
import Konva from 'konva';
import stage from './stage.json';
import { Stage, Layer, Rect, Text } from 'react-konva';

const Dashboard = () => {
  const stageRef = React.useRef(null);
  const hall = 0;

  const rectRef = React.useRef(null);
  const [blink, setBlink] = React.useState(false);
  React.useEffect(() => {
    console.log(rectRef);
    if (!rectRef.current) {
      return;
    }
    var period = 300;

    var anim = new Konva.Animation(frame => {
      rectRef.current.opacity((Math.sin(frame.time / period) + 1) / 2);
    }, rectRef.current.getLayer());

    anim.start();
    return () => {
      anim.stop();
    };
  }, [blink]);

  return (
    
    <Stage width={stage.stageWidth} height={stage.stageHeight} ref={stageRef}>
      {stage.layers.map((layer, index) => {
        return (
          <Layer key={index}>
            {layer.elements.map((element, index) => {
              if (element.type === "Rect") {
                return <Rect key={index} {...element.attrs} fill={element.attrs.id === "hall" + hall ? "orange" : element.attrs.fill } ref={element.attrs.id === "hall" + hall ? rectRef : null} />; 
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