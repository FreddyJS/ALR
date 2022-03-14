import { useTable, useSortBy } from "react-table";
import useRows from "./hooks/useRows";
import useColumns from "./hooks/useColumns";

import "./styles.css";

export default function Stats() {
  const columns = useColumns();
  const data = useRows();
  const table = useTable({ columns, data }, useSortBy);

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow
  } = table;

  return (
    <div className="container">
      {/* Aplicamos las propiedades de la tanña */}
      <table {...getTableProps()}>
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                // Aplicamos las propiedades de ordenación a cada columna
                <th
                  {...column.getHeaderProps(column.getSortByToggleProps())}
                  className={
                    column.isSorted
                      ? column.isSortedDesc
                        ? "desc"
                        : "asc"
                      : ""
                  }
                >
                  {column.render("Header")}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        {/* Aplicamos las propiedades de la tabla */}
        <tbody {...getTableBodyProps()}>
          {
            // Bucle sobre las filas
            rows.map((row) => {
              // Prepara la fila para mostrar
              prepareRow(row);
              return (
                // Aplicamos las propiedades de las columnas
                <tr {...row.getRowProps()}>
                  {
                    // Bucle sobre las celdas
                    row.cells.map((cell) => {
                      // Aplicamos las propiedades de las celdas
                      return (
                        <td {...cell.getCellProps()}>
                          {
                            cell.render("Cell")
                          }
                        </td>
                      );
                    })
                  }
                </tr>
              );
            })
          }
        </tbody>
      </table>
    </div>
  );
}
