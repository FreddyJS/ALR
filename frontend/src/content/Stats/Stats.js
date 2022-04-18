import StatsHalls from "./StatsHalls";
import StatsRoutes from "./StatsRoutes";

import "./styles.css";

export default function Stats() {
  return (
    <>
    <div className="textt">Estadísticas de las rutas</div>
    <StatsRoutes></StatsRoutes>
    <div className="text">Pasillos en los que se ha parado debido a obstaculos</div>
    <StatsHalls></StatsHalls>
    </>
  );
}
