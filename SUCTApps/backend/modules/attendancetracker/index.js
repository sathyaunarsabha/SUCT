

export default function attendanceAdd() {
    // ...
  }

import { isProduction } from '../util.js';

console.log('Guruve Saranam ! Running in ', isProduction() ? 'Production' : 'Development', ' mode');
// console.log('API URL:', API_URL);

// You can use isProduction() for conditional logic
if (isProduction()) {
  // Do production-specific setup
} else {
  // Do development-specific setup
}