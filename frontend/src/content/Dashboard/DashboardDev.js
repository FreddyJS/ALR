import React from 'react';
import './dashboard.scss';

import { Button, Checkbox, TextInput } from 'carbon-components-react';

import { Stage, Layer, Text } from 'react-konva';
import Rectangle from './Rectangle';


const defaultTextProps = {
  type: "Text",
  x: 100,
  y: 100,
  text: 'Hello World',
  fontSize: 16,
  fill: "black",
};

const defaultRoomProps = {
  type: "Rect",
  x: 100,
  y: 100,
  width: 100,
  height: 100,
  fill: 'purple',
};

const defaultHallProps = {
  type: "Rect",
  x: 100,
  y: 100,
  width: 30,
  height: 100,
  fill: 'black',
};

const defaultStickerProps = {
  type: "Rect",
  x: 100,
  y: 100,
  width: 30,
  height: 30,
  fill: 'blue',
};

const DashboardDev = () => {
  // Stage refence to export map to JSON
  const stageRef = React.useRef();

  // List of shapes in the stage and selected shape id
  const [shapes, setShapes] = React.useState([]);
  const [selectedShape, selectShape] = React.useState();
  const [newTextData, setNewTextData] = React.useState('');
  const [stickerColor, setStickerColor] = React.useState('blue');
  const [hallOrientation, setHallOrientation] = React.useState('vertical');

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
        layer: "layer" + index,
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
        id: "room" + shapes.filter(shape => shape.id.startsWith('room')).length,
        ...defaultRoomProps,
      };

      setShapes([...shapes, newRect]);
    } else if (type === 'text') {
      const newText = {
        id: "text" + shapes.filter(shape => shape.id.startsWith('text')).length,
        ...defaultTextProps,
      };

      if (newTextData !== '') {
        newText.text = newTextData;
        setNewTextData('');
      }

      setShapes([...shapes, newText]);
    } else if (type === 'hall') {
      const newRect = {
        id: "hall" + shapes.filter(shape => shape.id.startsWith('hall')).length,
        ...defaultHallProps,
      };
      if (hallOrientation === 'vertical') {
        // Default vertical hall
      } else {
        // Default horizontal hall
        const width = newRect.width;
        newRect.width = newRect.height;
        newRect.height = width;
      }

      setShapes([...shapes, newRect]);
    } else if (type === 'sticker') {
      const newRect = {
        id: "sticker" + shapes.filter(shape => shape.id.startsWith('sticker')).length,
        ...defaultStickerProps,
      };
      newRect.fill = stickerColor;

      setShapes([...shapes, newRect]);
    }
  }

  return (
    <div style={{ display: "flex", flexDirection: "row", marginTop: "1rem" }}>
      <div style={{ display: "flex", flexDirection: "column", marginRight: "1rem" }}>
        <Button onClick={() => appendShape("room")} style={{margin: "1px"}}>New Room</Button>
        <Button onClick={() => appendShape("hall")} style={{margin: "1px"}}>New Hall</Button>
        <div>
          <Checkbox id="cb-vertical" labelText="Vertical" onChange={() => setHallOrientation("vertical")} checked={hallOrientation === "vertical"} />
          <Checkbox id="cb-horizontal" labelText="Horizontal" onChange={() => setHallOrientation("horizontal")} checked={hallOrientation === "horizontal"} />
        </div>
        <Button onClick={() => appendShape("sticker")} style={{margin: "1px"}}>New Sticker</Button>
        <div>
          <Checkbox id="cb-blue" labelText="Blue" onClick={() => setStickerColor("blue")} checked={stickerColor === "blue"} />
          <Checkbox id="cb-red" labelText="Red" onClick={() => setStickerColor("red")} checked={stickerColor === "red"} />
        </div>
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
        <Stage width={1280} height={720} ref={stageRef}>
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
              }
              return null;
            })}
          </Layer>

          <Layer>
            {shapes.map((shape, index) => {
              const isSelected = selectedShape === shape.id;
              if (shape.type === "Text") {
                return (
                  <Text
                    key={shape.id}
                    draggable
                    {...shape}
                    isSelected={isSelected}
                    onClick={() => {
                      if (selectedShape === shape.id) {
                        // Change color of the selected shape
                        const colors = ['red', 'black', 'white'];
                        const current = colors.indexOf(shape.fill);
                        const next = (current + 1) % colors.length;
                        shape.fill = colors[next];
                        selectShape(null);
                      } else {
                        selectShape(shape.id);
                      }
                    }}
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