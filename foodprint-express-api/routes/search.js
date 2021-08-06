const express = require('express');
const router = express.Router();

const { searchFood } = require('../controllers/search');

router.get('/food', searchFood);

module.exports = router;
