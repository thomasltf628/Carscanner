import React from 'react';
import './datatable.css'

const DataTable = ({ jsonData }) => {
  if (!jsonData) {
    return null;
  }

  const tableData = jsonData.map((item, index) => ({
        id: index +1,
        source: item.source,
        price:item.price,
        year:item.year,
        mileage: item.mileage,
        location: item.location,
        link: item.link_to_buyer,
  }
  )
  );

  return (
    <div>
    <table style={{width: '100%', height: '400px', borderWidth: '2px'}}>
      <thead>
        <tr>
          <th>ID</th>
          <th>Source</th>
          <th>Price</th>
          <th>Year</th>
          <th>Mileage</th>
          <th>Location</th>
          <th>Link</th>
        </tr>
      </thead>
      <tbody>
        {tableData.map((rowData) => (
          <tr key={rowData.id}>
            <td>{rowData.id}</td>
            <td>{rowData.source}</td>
            <td>{rowData.price}</td>
            <td>{rowData.year}</td>
            <td>{rowData.mileage}</td>
            <td>{rowData.location}</td>
            <td><a href={rowData.link}>Link</a></td>
          </tr>
        ))}
      </tbody>
    </table>
    </div>
  );
};

export default DataTable;
