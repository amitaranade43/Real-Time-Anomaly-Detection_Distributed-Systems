import React from 'react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
// import Navbar from './Navbar';



function DataTable({ data, handleDelete }) {
  return (
    <>
      <h1 className="title">Faulty Server Data</h1>
      <ToastContainer />
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Server ID</th>
            <th>Temperature</th>
            <th>Status</th>
            <th>Created At</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {data.map(item => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.server_id}</td>
              <td>{item.temp}</td>
              <td>{item.status}</td>
              <td>{item.created_at}</td>
              <td><button onClick={() => handleDelete(item.id)}>Fixed</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

export default DataTable;
