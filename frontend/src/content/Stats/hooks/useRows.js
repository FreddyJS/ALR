import { useMemo } from "react";

export default function useRows() {
  const rows = useMemo(
    () => [
      {
        robot: "Picar-S",
        destino: "Room 2",
        salida: "12/03/2021 12:05:48",
        llegada: "12/03/2021 12:07:36"
      },
      {
        robot: "Picar-S",
        destino: "Room 7",
        salida: "10/03/2021 14:36:12",
        llegada: "10/03/2021 14:38:43"
      },
      {
        robot: "Picar-S",
        destino: "Room 4",
        salida: "11/03/2021 11:23:33",
        llegada: "11/03/2021 11:26:54"
      },
      {
        robot: "Picar-S",
        destino: "Room 1",
        salida: "11/03/2021 11:33:33",
        llegada: "11/03/2021 11:35:54"
      }
    ],
    []
  );

  return rows;
}
