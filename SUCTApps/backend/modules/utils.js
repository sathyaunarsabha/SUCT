import dotenv from 'dotenv';

// Load correct .env file based on current NODE_ENV or default to 'development'
const envFile = `.env.${process.env.NODE_ENV || 'development'}`;
dotenv.config({ path: envFile });

// Utility to check if the environment is production
export const isProduction = () => process.env.NODE_ENV === 'production';

// Utility to get any environment variable safely
export const getEnv = (key, defaultValue = '') => {
  return process.env[key] || defaultValue;
};

// Optional: expose commonly used variables
// export const API_URL = getEnv('API_URL');