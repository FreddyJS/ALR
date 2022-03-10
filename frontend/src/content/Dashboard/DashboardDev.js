import React from 'react';
import './dashboard.scss';

import { Button, TextInput } from 'carbon-components-react';

import { Stage, Layer, Text } from 'react-konva';
import Rectangle from './Rectangle';


const defaultRectProps = {
  type: "Rect",
  x: 100,
  y: 100,
  width: 100,
  height: 100,
  fill: 'red',
};

const defaultTextProps = {
  type: "Text",
  x: 100,
  y: 100,
  text: 'Hello World',
  fontSize: 15,
  fill: "black",
};

const DashboardDev = () => {
  // Stage refence to export map to JSON
  const stageRef = React.useRef(null);

  // List of shapes in the stage and selected shape id
  const [shapes, setShapes] = React.useState([]);
  const [selectedShape, selectShape] = React.useState(null);
  const [newTextData, setNewTextData] = React.useState('');

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
        if (element.className === "Rect") {
          return {
            type: element.className,
            attrs: {
              id: element.id(),
              x: element.x(),
              y: element.y(),
              width: element.width(),
              height: element.height(),
              fill: element.fill(),
            }
          }
        } else if (element.className === "Text") {
          return {
            type: element.className,
            attrs: {
              id: element.id(),
              x: element.x(),
              y: element.y(),
              text: element.text(),
              fontSize: element.fontSize(),
              fill: element.fill(),
            }
          }
        }

        return null;
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
    if (type === 'room') {
      const newRect = {
        id: "room" + shapes.length,
        ...defaultRectProps,
      };
      newRect.fill = "purple";

      setShapes([...shapes, newRect]);
    } else if (type === 'text') {
      const newText = {
        id: "text" + shapes.length,
        text: "Text " + shapes.length,
        ...defaultTextProps,
      };

      if (newTextData !== '') {
        newText.text = newTextData;
        setNewTextData('');
      }

      setShapes([...shapes, newText]);
    } else if (type === 'hall') {
      const newRect = {
        id: "hall" + shapes.length,
        ...defaultRectProps,
      };
      newRect.fill = "black";
      newRect.width = newRect.height / 2;

      setShapes([...shapes, newRect]);
    }
  }

  return (
    <div style={{ display: "flex", flexDirection: "row", marginTop: "1rem" }}>
      <div style={{ display: "flex", flexDirection: "column" }}>
        <Button onClick={() => appendShape("room")} style={{margin: "1px"}}>New Room</Button>
        <Button onClick={() => appendShape("hall")} style={{margin: "1px"}}>New Hall</Button>
        <Button onClick={() => appendShape("text")} style={{margin: "1px"}}>New Text</Button>
        <div>
          <TextInput id="text-input" labelText="" placeholder="Hello World" onChange={(e) => setNewTextData(e.target.value)} value={newTextData}/>
        </div>
        <Button onClick={() => setShapes(shapes.slice(0, shapes.length-1))} style={{margin: "1px"}}>Del Last</Button>
        <Button onClick={() => exportCanvasToJSON()} style={{margin: "1px"}}>Export</Button>
        {stageRef.current &&
          <>
            <div>Stage width: {stageRef.current.width()}</div>
            <div>Stage height: {stageRef.current.height()}</div>
          </>
        }
      </div>

      <div style={{ border: "1px solid" }}>
        <Stage width={window.innerWidth} height={window.innerHeight} ref={stageRef}>
          <Layer>
            {shapes.map((shape, index) => {
              const isSelected = selectedShape === shape.id;
              if (shape.type === "Rect") {
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
              } else if (shape.type === "Text") {
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

              return null;
            })}
          </Layer>
        </Stage>
      </div>
    </div>
  );
};

export default DashboardDev;