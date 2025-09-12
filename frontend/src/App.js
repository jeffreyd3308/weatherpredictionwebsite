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

const BASE_URL = 'https://weatherpredictionwebsite.onrender.com/api';

function DataForm() {
  const [data, setData] = useState({temperature: '', pressure: '', humidity: '', dewpoint: '', wind_speed: '', precipitation_prediction: '0'});
  const [prediction, setPrediction] = useState('No prediction')

  function handleChange(e) {
    const {name, value} = e.target;
    setData((prevState) => ({...prevState, [name]: value}));
  }

  function handleSubmit(e) {
    e.preventDefault();
    console.log(data);
    axios.post(`${BASE_URL}/weather/`, data, config)
        .then(res => {console.log(res)})
        .catch(err => console.log(err));
    setTimeout(function() {
        axios.get(`${BASE_URL}/prediction/`, config)
          .then(res => {
            console.log(res.data[0].prediction);
            setPrediction(res.data[0].prediction + 'mm');
          })
          .catch(err => {
            console.error("Prediction fetch error:", err);
            setPrediction('Invalid input values');
          })
    }, 1000);

  }

  return (
      <div>
        <form onSubmit={handleSubmit}>
            <div className='container'>
                <div className='section'>
                    <label>Temperature:</label>
                    <input
                      onChange={handleChange}
                      type="number"
                      name="temperature"
                      value={data.temperature}
                    />
                </div>
                <div className='section'>
                    <label>Pressure:</label>
                  <input
                      onChange={handleChange}
                      type="number"
                      name="pressure"
                      value={data.pressure}
                  />
                </div>
                <div className='section'>
                    <label>Humidity:</label>
                      <input
                          onChange={handleChange}
                          type="number"
                          name="humidity"
                          value={data.humidity}
                      />
                </div>
                <div className='section'>
                    <label>Dewpoint:</label>
                      <input
                          onChange={handleChange}
                          type="number"
                          name="dewpoint"
                          value={data.dewpoint}
                      />
                </div>
                <div className='section'>
                    <label>Wind speed:</label>
                      <input
                          onChange={handleChange}
                          type="number"
                          name="wind_speed"
                          value={data.wind_speed}
                      />
                </div>
            </div>
            <div className='submitdiv'>
                <button type="submit">Submit</button>
            </div>
        </form>

        <div>
          <h1>
            {prediction}
          </h1>
        </div>
      </div>
  )
}

export default function App() {
  return (
    <div>
        <div className="Title">
            <h1>Precipitation Prediction Website</h1>
        </div>
        <div className='Description'>
            <p>This website predicts the amount of precipitation in millimeters with temperature (celsius), humidity percentage, pressure in hectopascals (hPa), dewpoint, and wind speed in meter/seconds. </p>
        </div>
      <DataForm />
        <div className="Description">
            <p>The predicted prediction is typically off by about 0.2082 millimeters from the actual precipitation.</p>
        </div>
    </div>
  );
}
