const express = require('express');
const router = express.Router();

const { getInsights } = require('../controllers/insights');

router.post('/get', getInsights);

module.exports = router;
