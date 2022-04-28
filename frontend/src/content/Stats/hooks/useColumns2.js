import { useMemo } from "react";

export default function useColumns2() {
  const columns = useMemo(
    () => [
      {
        Header: "PASILLO",
        accessor: "hall"
      },
      {
        Header: "DETÍVOSE",
        accessor: "stopped"
      }
    ],
    []
  );

  return columns;
}