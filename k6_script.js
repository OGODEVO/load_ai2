import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 100 }, // Ramp-up to 100 virtual users over 1 minute
    { duration: '3m', target: 100 }, // Stay at 100 virtual users for 3 minutes
    { duration: '1m', target: 0 },   // Ramp-down to 0 virtual users over 1 minute
  ],
};

export default function () {
  const url = 'http://localhost:8000/';
  const payload = JSON.stringify({
    question: 'What is the meaning of life?',
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  http.post(url, payload, params);
  sleep(1);
}
