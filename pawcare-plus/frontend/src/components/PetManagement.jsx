import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PET_API_BASE = process.env.REACT_APP_PET_API_BASE || 'http://localhost:8001';

const PetManagement = () => {
  const [owners, setOwners] = useState([]);
  const [pets, setPets] = useState([]);
  const [newOwner, setNewOwner] = useState({ name: '', email: '', phone: '' });
  const [newPet, setNewPet] = useState({ name: '', species: '', breed: '', age: '', owner_id: '' });

  useEffect(() => {
    fetchOwners();
    fetchPets();
  }, []);

  const fetchOwners = async () => {
    try {
      const response = await axios.get(`${PET_API_BASE}/owners/`);
      setOwners(response.data);
    } catch (error) {
      console.error('Error fetching owners:', error);
    }
  };

  const fetchPets = async () => {
    try {
      const response = await axios.get(`${PET_API_BASE}/pets/`);
      setPets(response.data);
    } catch (error) {
      console.error('Error fetching pets:', error);
    }
  };

  const createOwner = async () => {
    try {
      await axios.post(`${PET_API_BASE}/owners/`, newOwner);
      setNewOwner({ name: '', email: '', phone: '' });
      fetchOwners();
    } catch (error) {
      console.error('Error creating owner:', error);
    }
  };

  const createPet = async () => {
    try {
      await axios.post(`${PET_API_BASE}/pets/`, newPet);
      setNewPet({ name: '', species: '', breed: '', age: '', owner_id: '' });
      fetchPets();
    } catch (error) {
      console.error('Error creating pet:', error);
    }
  };

  return (
    <div>
      <h1>Pet Management</h1>
      <div>
        <h2>Owners</h2>
        <ul>
          {owners.map(owner => (
            <li key={owner.id}>{owner.name} - {owner.email}</li>
          ))}
        </ul>
        <input
          type="text"
          placeholder="Name"
          value={newOwner.name}
          onChange={(e) => setNewOwner({ ...newOwner, name: e.target.value })}
        />
        <input
          type="email"
          placeholder="Email"
          value={newOwner.email}
          onChange={(e) => setNewOwner({ ...newOwner, email: e.target.value })}
        />
        <input
          type="text"
          placeholder="Phone"
          value={newOwner.phone}
          onChange={(e) => setNewOwner({ ...newOwner, phone: e.target.value })}
        />
        <button onClick={createOwner}>Add Owner</button>
      </div>
      <div>
        <h2>Pets</h2>
        <ul>
          {pets.map(pet => (
            <li key={pet.id}>{pet.name} - {pet.species} (Owner ID: {pet.owner_id})</li>
          ))}
        </ul>
        <input
          type="text"
          placeholder="Name"
          value={newPet.name}
          onChange={(e) => setNewPet({ ...newPet, name: e.target.value })}
        />
        <input
          type="text"
          placeholder="Species"
          value={newPet.species}
          onChange={(e) => setNewPet({ ...newPet, species: e.target.value })}
        />
        <input
          type="text"
          placeholder="Breed"
          value={newPet.breed}
          onChange={(e) => setNewPet({ ...newPet, breed: e.target.value })}
        />
        <input
          type="number"
          placeholder="Age"
          value={newPet.age}
          onChange={(e) => setNewPet({ ...newPet, age: e.target.value })}
        />
        <select
          value={newPet.owner_id}
          onChange={(e) => setNewPet({ ...newPet, owner_id: e.target.value })}
        >
          <option value="">Select Owner</option>
          {owners.map(owner => (
            <option key={owner.id} value={owner.id}>{owner.name}</option>
          ))}
        </select>
        <button onClick={createPet}>Add Pet</button>
      </div>
    </div>
  );
};

export default PetManagement;