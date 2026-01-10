import React, { useState, useEffect } from 'react';
import axios from 'axios';

const APPOINTMENT_API_BASE = process.env.REACT_APP_APPOINTMENT_API_BASE || 'http://localhost:8002';

const AppointmentManagement = () => {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    try {
      const response = await axios.get(`${APPOINTMENT_API_BASE}/appointments/`);
      setAppointments(response.data);
    } catch (error) {
      console.error('Error fetching appointments:', error);
    }
  };

  const updateStatus = async (id, status) => {
    try {
      await axios.put(`${APPOINTMENT_API_BASE}/appointments/${id}/status`, { status });
      fetchAppointments();
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  const getStatusBadge = (status) => {
    const colors = {
      REQUESTED: 'gray',
      CONFIRMED: 'blue',
      IN_PROGRESS: 'yellow',
      COMPLETED: 'green',
      CANCELLED: 'red'
    };
    return <span style={{ backgroundColor: colors[status], padding: '2px 8px', borderRadius: '4px', color: 'white' }}>{status}</span>;
  };

  return (
    <div>
      <h1>Appointment Management</h1>
      <ul>
        {appointments.map(appointment => (
          <li key={appointment.id}>
            Pet ID: {appointment.pet_id}, Date: {new Date(appointment.appointment_date).toLocaleString()}, Doctor: {appointment.doctor_name}, Reason: {appointment.reason}, Status: {getStatusBadge(appointment.status)}
            <select onChange={(e) => updateStatus(appointment.id, e.target.value)}>
              <option value="">Change Status</option>
              <option value="CONFIRMED">CONFIRMED</option>
              <option value="IN_PROGRESS">IN_PROGRESS</option>
              <option value="COMPLETED">COMPLETED</option>
              <option value="CANCELLED">CANCELLED</option>
            </select>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AppointmentManagement;