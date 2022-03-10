import React from 'react';

import { Button } from 'carbon-components-react';

import { Stage, Layer, Rect, Text } from 'react-konva';
import Rectangle from './Rectangle';


const defaultRectProps = {
  x: 100,
  y: 100,
  width: 100,
  height: 100,
  fill: 'red',
};

const defaultTextProps = {
  x: 100,
  y: 100,
  text: 'Hello World',
  fontSize: 15,
  fill: "white",
};

const DashboardDev = () => {
  // Stage refence to export map to JSON
  const stageRef = React.useRef(null);

  // List of shapes in the stage and selected shape id
  const [shapes, setShapes] = React.useState([]);
  const [selectedShape, selectShape] = React.useState(null);
  const pasillo = 1;

  function downloadJSON(object, name) {
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(object, null, 2));
    var link = document.createElement('a');
    link.download = name;
    link.href = dataStr;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  const exportCanvasToJSON = () => {
    const stage = stageRef.current;
    const stageLayers = stage.children;

    // For each layer we are going to save the attrs of its childrens
    const layers = stageLayers.map((layer, index) => {
      const layerElements = layer.children;
      const layerElementsAttrs = layerElements.filter(element => element.className !== "Transformer").map(element => {
        return {
          type: element.className,
          attrs: element.className === "Text" ? element.attrs : {
            x: Math.round(element.x()),
            y: Math.round(element.y()),
            width: Math.round(element.width()),
            height: Math.round(element.height()),
            fill: element.fill(),
          }
        };
      });

      return {
        layer: "Layer " + index,
        elements: layerElementsAttrs
      }
    });

    const exportedStage = {
      stageWidth: stage.width(),
      stageHeight: stage.height(),
      layers: layers,
    }

    downloadJSON(exportedStage, "stage.json");
  };

  function appendShape(type) {
    console.log(stageRef.current);

    if (type === 'rect') {
      const newRect = {
        id: "rect" + shapes.length,
        ...defaultRectProps,
      };

      setShapes([...shapes, newRect]);
    } else if (type === 'text') {
      const newText = {
        id: "text" + shapes.length,
        text: "Text " + shapes.length,
        ...defaultTextProps,
      };

      setShapes([...shapes, newText]);
    }
  }

  return (
    <div>
      <div style={{ display: "flex", flexDirection: "row", justifyContent: "center"}}>
        <Button onClick={() => appendShape("rect")} style={{margin: "1px"}}>New Rect</Button>
        <Button onClick={() => appendShape("text")} style={{margin: "1px"}}>New Text</Button>
        <Button onClick={() => exportCanvasToJSON()} style={{margin: "1px"}}>Export</Button>
      </div>
      <p>To change a shape color double click, click to select and drag or resize</p>

      <div>
        <Stage width={window.innerWidth} height={window.innerHeight} ref={stageRef}>
          <Layer>
            {shapes.map((shape, index) => {
              const isSelected = selectedShape === shape.id;
              if (shape.id.startsWith("rect")) {
                return (
                  <Rectangle
                    key={shape.id}
                    shapeProps={shape}
                    onSelect={() => {
                      if (selectedShape === shape.id) {
                        // Change color of the selected shape
                        const colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'black'];
                        const current = colors.indexOf(shape.fill);
                        const next = (current + 1) % colors.length;
                        shape.fill = colors[next];
                        selectShape(null);
                      } else {
                        selectShape(shape.id);
                      }
                    }}
                    onChange={(newShape) => {
                      setShapes(shapes.map((s) => (s.id === shape.id ? newShape : s)));
                    }}
                    isSelected={isSelected}
                  />
                );
              } else if (shape.id.startsWith("text")) {
                return (
                  <Text
                    key={shape.id}
                    {...shape}
                    isSelected={isSelected}
                    onClick={() => {
                      if (selectedShape === shape.id) {
                        // Change color of the selected shape
                        const colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'black', 'white'];
                        const current = colors.indexOf(shape.fill);
                        const next = (current + 1) % colors.length;
                        shape.fill = colors[next];
                        selectShape(null);
                      } else {
                        selectShape(shape.id);
                      }
                    }}
                    draggable
                  />
                );
              }
            })}
          </Layer>
        </Stage>
      </div>
    </div>
  );
};

export default DashboardDev;