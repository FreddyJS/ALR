import React from "react";

import './room-input.scss';

import { Button } from "carbon-components-react";
import { ImExit } from "react-icons/im";
import { MdStairs } from "react-icons/md";
import { FaBluetooth } from "react-icons/fa";

const RoomInput = ({ onSubmit, onChange, value }) => {
  return (
    <div className="room-page__keyboard">
          <div className="room-page__keyboard-row">
            <Button className="room-page__keyboard-button" onClick={() => onChange(value + "1")}>1</Button>
            <Button className="room-page__keyboard-button" onClick={() => onChange(value + "2")}>2</Button>
            <Button className="room-page__keyboard-button" onClick={() => onChange(value + "3")}>3</Button>
          </div>
          <div className="room-page__keyboard-row">
            <Button className="room-page__keyboard-button" onClick={() => onChange(value + "4")}>4</Button>
            <Button className="room-page__keyboard-button" onClick={() => onChange(value + "5")}>5</Button>
            <Button className="room-page__keyboard-button" onClick={() => onChange(value + "6")}>6</Button>
          </div>
          <div className="room-page__keyboard-row">
            <Button className="room-page__keyboard-button" onClick={() => onChange(value + "7")}>7</Button>
            <Button className="room-page__keyboard-button" onClick={() => onChange(value + "8")}>8</Button>
            <Button className="room-page__keyboard-button" onClick={() => onChange(value + "9")}>9</Button>
          </div>
          <div className="room-page__keyboard-row">
            <Button className="room-page__keyboard-button" onClick={() => onChange("06")}><ImExit /></Button>
            <Button className="room-page__keyboard-button" onClick={() => onChange("07")}><MdStairs /></Button>
            <Button className="room-page__keyboard-button" onClick={() => onChange("BLE")}><FaBluetooth /></Button>
          </div>
          <div className="room-page__keyboard-row">
            <Button className="room-page__keyboard-button" onClick={() => onChange("")}>Reset</Button>
            <Button className="room-page__keyboard-button" onClick={() => onChange(value + "0")}>0</Button>
            <Button className="room-page__keyboard-button" onClick={() => onSubmit()}>OK</Button>
          </div>
        </div>
  );
};

export default RoomInput;