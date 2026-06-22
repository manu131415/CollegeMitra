const express = require('express');
const cors = require('cors');
const pool = require('./db');

const app = express();


app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
    res.send('CollegeMitra Backend Running');
});

app.get('/test-db', async (req, res) => {
    try {
        const result = await pool.query(
            'SELECT COUNT(*) FROM institutes'
        );

        res.json(result.rows[0]);
    } catch (err) {
        console.error(err);
        res.status(500).json({
            error: err.message
        });
    }
});

const predictorRoutes = require('./routes/predictor');
app.use('/api', predictorRoutes);

app.listen(5000, () => {
    console.log('Server running on port 5000');
});