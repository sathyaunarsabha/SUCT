/* import http from 'http';

const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello from Node.js with Docker!\n');
});

server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
*/

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.js';
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

