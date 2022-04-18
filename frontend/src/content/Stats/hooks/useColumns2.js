import { useMemo } from "react";

export default function useColumns2() {
  const columns = useMemo(
    () => [
      {
        Header: "PASILLO",
        accessor: "hall"
      },
      {
        Header: "SE HA DETENIDO",
        accessor: "stopped"
      }
    ],
    []
  );

  return columns;
}