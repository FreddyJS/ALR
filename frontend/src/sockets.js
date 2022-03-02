const RobotSocket = new WebSocket('ws://localhost:8000/ws/robot/R01/');
RobotSocket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("RobotSocket Received: ", data);
};

const UISocket = new WebSocket('ws://localhost:8000/ws/ui/R01/');
UISocket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("UISocket Received: ", data);
};


export { UISocket, RobotSocket };