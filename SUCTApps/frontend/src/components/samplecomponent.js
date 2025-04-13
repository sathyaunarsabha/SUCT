import axios from "axios";

const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:5000";

axios.get(`${apiUrl}/api/attendance`)
  .then(response => console.log(response.data))
  .catch(error => console.error("Error fetching data:", error));

  import React, { useEffect, useState } from 'react';
import axios from 'axios';

const samplecomponent = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Make an HTTP GET request to your backend or external API
    axios.get('http://localhost:5000/api/data')  // Your backend API endpoint
      .then(response => {
        setData(response.data);  // Store the response data
      })
      .catch(error => {
        console.error('There was an error!', error);
      });
  }, []);

  return (
    <div>
      <h1>Data from Backend:</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
};

export default samplecomponent;