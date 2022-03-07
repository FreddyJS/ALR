import React from 'react';
import { Stage, Layer, Rect, Text } from 'react-konva';

const Dashboard = () => {
  const pasillo = 1;
  return (
    <Stage width={window.innerWidth} height={window.innerHeight}>
      <Layer>
        <Rect
          x={0}
          y={0}
          width={150}
          height={150}
          fill="purple"
          shadowBlur={10}
        />
        <Text text="Room 1" fill='white' fontSize={15} />
        <Rect
          x={200}
          y={0}
          width={150}
          height={150}
          fill="purple"
          shadowBlur={10}
        />

        <Rect
          id='p1'
          x={165}
          y={0}
          width={20}
          height={400}
          fill={pasillo === 1 ? 'yellow' : 'black'}
          shadowBlur={10}
        />
      
        <Rect
          x={165}
          y={60}
          width={20}
          height={20}
          fill="green"
          shadowBlur={10}
        />

        <Rect
          x={0}
          y={200}
          width={350}
          height={20}
          fill="black"
          shadowBlur={10}
        />
  
        <Rect
          x={165}
          y={200}
          width={20}
          height={20}
          fill="red"
          shadowBlur={10}
        />

        <Rect
          x={65}
          y={200}
          width={20}
          height={20}
          fill="green"
          shadowBlur={10}
        />

        <Rect
          x={255}
          y={200}
          width={20}
          height={20}
          fill="green"
          shadowBlur={10}
        />

        <Rect
          x={0}
          y={250}
          width={150}
          height={150}
          fill="purple"
          shadowBlur={10}
        />
        
        <Rect
          x={200}
          y={250}
          width={150}
          height={150}
          fill="purple"
          shadowBlur={10}
        />

        <Rect
          x={150}
          y={400}
          width={50}
          height={50}
          fill="cyan"
          shadowBlur={10}
        />

        <Text
          x={150}
          y={400}
          text="Hall"
          fill='black'
          fontSize={15}
        />

      </Layer>
    </Stage>
  );
};

export default Dashboard;