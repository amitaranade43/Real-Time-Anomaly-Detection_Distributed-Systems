import React, { useState, useEffect } from 'react';
import { API_BASE_URL, API_DATA__HISTORY_ENDPOINT } from '../config';
function History() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = () => {
    fetch(`${API_BASE_URL}${API_DATA__HISTORY_ENDPOINT}`)
      .then(response => response.json())
      .then(data => setData(data));
  }

  return (
    <div className="History">
      <h1 className="title">Server History</h1>
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Server ID</th>
            <th>Temperature</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          {data.map(item => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.server_id}</td>
              <td>{item.temp}</td>
              <td>{item.created_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default History;
