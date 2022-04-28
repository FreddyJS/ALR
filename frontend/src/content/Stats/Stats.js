import StatsHalls from "./StatsHalls";
import StatsRoutes from "./StatsRoutes";

import "./styles.css";

export default function Stats() {
  return (
    <>
    <div></div>
    <div className="text">Estadísticas das rutas</div>
    <StatsRoutes></StatsRoutes>
    <div className="text">Pasillos noss que se parou debido a obstáculos</div>
    <StatsHalls></StatsHalls>
    </>
  );
}
