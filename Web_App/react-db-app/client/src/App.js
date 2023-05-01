import React, { useState, useEffect } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import DataTable from './components/DataTable';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import {
  BrowserRouter,
  Routes, // instead of "Switch"
  Route,
} from "react-router-dom";
import History from './components/History';
import { API_BASE_URL, API_DATA_ENDPOINT } from './config';




function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchData();

    // Fetch new data every 5 seconds
    const intervalId = setInterval(() => {
      fetchData();
    }, 5000);

    // Cleanup function to clear interval on unmount
    return () => clearInterval(intervalId);
  }, []);

  const fetchData = () => {
    fetch(`${API_BASE_URL}${API_DATA_ENDPOINT}`)
      .then(response => response.json())
      .then(data => setData(data));
  }

  const handleDelete = (id) => {
    fetch(`${API_BASE_URL}${API_DATA_ENDPOINT}/${id}`, {
      method: 'DELETE'
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to delete the entry');
      }
      return response.json();
    })
    .then(() => {
      setData(data.filter(item => item.id !== id));
      toast.success("Entry has been deleted", {
        position: "top-right",
        autoClose: 2000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
    })
    .catch(error => {
      console.error(error);
      toast.error("Failed to delete the entry", {
        position: "top-right",
        autoClose: 2000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
    });
  }
  
  return (
    <div className="App">
      <Navbar />
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<DataTable data={data} handleDelete={handleDelete} />}/>
      </Routes>
      <Routes>
          <Route exact path="/data/history" element={<History />}/>
      </Routes>
      
      </BrowserRouter>
      
      
    </div>
  );
}

export default App;
