// backend/routes/predictor.js
const express = require('express');
const router = express.Router();

const FASTAPI_URL = process.env.PREDICTOR_SERVICE_URL || 'http://localhost:8000';

router.post('/predict', async (req, res) => {
  try {
    const response = await fetch(`${FASTAPI_URL}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body),
    });

    if (!response.ok) {
      return res.status(502).json({ error: 'Predictor service error' });
    }

    const data = await response.json();
    res.json(data);
  } catch (err) {
    console.error('FastAPI call failed:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;