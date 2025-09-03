import logo from './logo.svg';
import './App.css';
import { useState } from "react";
import axios from 'axios';
import Cookies from 'js-cookie';
const csrftoken = Cookies.get('csrftoken');
const config = {
  headers: {
    'X-CSRFToken': csrftoken,
    'Content-Type': 'application/json',
  }
}

function DataForm() {
  const [data, setData] = useState({temperature: '', pressure: '', humidity: '', dewpoint: '', wind_speed: ''});

  function handleChange(e) {
    const {name, value} = e.target;
    setData((prevState) => ({...prevState, [name]: value}));
  }

  function handleSubmit(e) {
    e.preventDefault();
    console.log(data);
    axios.post("http://localhost:8000/api/weather/", data, config)
        .then(res => {console.log(res)})
        .catch(err => console.log(err));
  }

  return (
      <div>
        <form onSubmit={handleSubmit}>
          <input
              onChange={handleChange}
              type="number"
              name="temperature"
              value={data.temperature}
          />
          <input
              onChange={handleChange}
              type="number"
              name="pressure"
              value={data.pressure}
          />
          <input
              onChange={handleChange}
              type="number"
              name="humidity"
              value={data.humidity}
          />
          <input
              onChange={handleChange}
              type="number"
              name="dewpoint"
              value={data.dewpoint}
          />
          <input
              onChange={handleChange}
              type="number"
              name="wind_speed"
              value={data.wind_speed}
          />
          <button type="submit">Submit</button>
        </form>
      </div>
  )
}

export default function App() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <DataForm />
    </div>
  );
}
