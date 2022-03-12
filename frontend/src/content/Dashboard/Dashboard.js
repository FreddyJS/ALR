import React from 'react';

import stage from './stage.json';
import { Stage, Layer, Rect, Text } from 'react-konva';


const Dashboard = () => {
  const stageRef = React.useRef(null);
  const hall = 0;

  return (
    <Stage width={stage.stageWidth} height={stage.stageHeight} ref={stageRef}>
      {stage.layers.map((layer, index) => {
        return (
          <Layer key={index}>
            {layer.elements.map((element, index) => {
              if (element.type === "Rect") {
                return <Rect key={index} {...element.attrs} fill={element.attrs.id === "hall" + hall ? "orange" : element.attrs.fill} />;
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