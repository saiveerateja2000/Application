import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import PetManagement from './components/PetManagement';
import AppointmentManagement from './components/AppointmentManagement';
import './App.css';

function App() {
  return (
    <div className="App">
      <nav>
        <ul>
          <li><Link to="/">Dashboard</Link></li>
          <li><Link to="/pets">Pet Management</Link></li>
          <li><Link to="/appointments">Appointment Management</Link></li>
        </ul>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/pets" element={<PetManagement />} />
        <Route path="/appointments" element={<AppointmentManagement />} />
      </Routes>
    </div>
  );
}

export default App;
