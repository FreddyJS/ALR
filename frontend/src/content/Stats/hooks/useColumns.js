import { useMemo } from "react";

export default function useColumns() {
  const columns = useMemo(
    () => [
      {
        Header: "ROBOT",
        accessor: "robot_id"
      },
      {
        Header: "DESTINO",
        accessor: "destiny"
      },
      {
        Header: "MINUTOS",
        accessor: "minutes"
      },
      {
        Header: "SEGUNDOS",
        accessor: "seconds"
      },
      {
        Header: "MILISEGUNDOS",
        accessor: "miliseconds"
      }
    ],
    []
  );

  return columns;
}