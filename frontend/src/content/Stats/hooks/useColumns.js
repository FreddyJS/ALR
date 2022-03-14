import { useMemo } from "react";

export default function useColumns() {
  const columns = useMemo(
    () => [
      {
        Header: "ROBOT",
        accessor: "robot"
      },
      {
        Header: "DESTINO",
        accessor: "destino"
      },
      {
        Header: "HORA SALIDA",
        accessor: "salida"
      },
      {
        Header: "HORA LLEGADA",
        accessor: "llegada"
      }
    ],
    []
  );

  return columns;
}