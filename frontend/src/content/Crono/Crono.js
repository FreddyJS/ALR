
import "./Crono.css";

import { useEffect, useReducer } from "react";

const stopWatchState = {
  running: false,
  currentTime: 0,
  lastTime: 0
};
function stopWatchReducer(state, action) {
  switch (action.type) {
    case "reset":
      return { running: false, currentTime: 0, lastTime: 0 };
    case "start":
      return { ...state, running: true, lastTime: Date.now() };
    case "stop":
      return { ...state, running: false };
    case "tick":
      if (!state.running) return state;
      return {
        ...state,
        currentTime: state.currentTime + (Date.now() - state.lastTime),
        lastTime: Date.now()
      };
    default:
      return state;
  }
}
function timeConverter(duration) {
  let date = new Date(duration);
  let hours = date.getHours() + date.getTimezoneOffset() / 60;
  let minutes = date.getMinutes();
  let seconds = date.getSeconds();
  let milliseconds = date.getMilliseconds();
  hours = hours.toString().padStart(2, "0");
  minutes = minutes.toString().padStart(2, "0");
  seconds = seconds.toString().padStart(2, "0");
  milliseconds = milliseconds.toString().padStart(3, "0");

  return {
    seconds,
    minutes,
    hours,
    milliseconds
  };
}


export default function Crono() {
  const [state, dispatch] = useReducer(stopWatchReducer, stopWatchState);
  const time = timeConverter(state.currentTime);

  useEffect(() => {
    let frame;
    function tick() {
      dispatch({ type: "tick" });
      frame = requestAnimationFrame(tick);
    }
    frame = requestAnimationFrame(tick);

    return () => cancelAnimationFrame(frame);
  }, []);

  /*if (cuenta){
    console.log("EI");
    const contar = (e)=>{
      dispatch({type:"start"});
    }
    contar();
  }*/

  return (
    <div className="ppal">
      <div className="text"> Tiempo en ruta : </div>
      <span className="timer">
        {time.hours}:{time.minutes}:{time.seconds}.{time.milliseconds}
      </span>
      <div className="p-4 space-x-4 ">
        <button id="restart" hidden
          onClick={() => dispatch({ type: "reset" })}
          className="bg-yellow-500 border-4 border-yellow-700 rounded-full w-16 h-16 hover:bg-yellow-600"
        >
          Reset{" "}
        </button>
        {!state.running ? (
          <button id="start" hidden
            onClick={() => dispatch({ type: "start" })}
            className="bg-green-500 border-4 border-green-700 rounded-full w-16 h-16 hover:bg-green-600"
          >
            start{" "}
          </button>
        ) : (
          <button id="stop" hidden
            onClick={() => dispatch({ type: "stop" })}
            className="bg-red-500 border-4 border-red-700 rounded-full w-16 h-16 hover:bg-red-600"
          >
            stop{" "}
          </button>
        )}
      </div>
    </div>
  );
}