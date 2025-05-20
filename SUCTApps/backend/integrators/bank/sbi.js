import axios from 'axios';

const authUrl = 'https://sandbox.sbi/api/auth/token'; // Replace with real URL
const clientId = 'your-client-id';
const clientSecret = 'your-client-secret';

async function getAccessToken() {
  const response = await axios.post(authUrl, {
    client_id: clientId,
    client_secret: clientSecret,
    grant_type: 'client_credentials',
  });

  return response.data.access_token;
}


async function getAccountBalance(token) {
    const response = await axios.get('https://sandbox.sbi/api/account/balance', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
  
    console.log(response.data);
  }
  