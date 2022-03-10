import React from 'react';

import stage from './stage.json';
import { Stage, Layer, Rect, Text } from 'react-konva';


const Dashboard = () => {
  const stageRef = React.useRef(null);

  React.useEffect(() => {
    console.log(stageRef.current);
  }, []);

  return (
    <Stage width={stage.stageWidth} height={stage.stageHeight} ref={stageRef}>
      {stage.layers.map((layer, index) => {
        return (
          <Layer key={index}>
            {layer.elements.map((element, index) => {
              console.log(element);
              if (element.type === "Rect") {
                return <Rect key={index} {...element.attrs} />
              } else if (element.type === "Text") {
                return <Text key={index} {...element.attrs} />
              }
            })}
          </Layer>
        );
      }
      )}
    </Stage>
  );
};

export default Dashboard;