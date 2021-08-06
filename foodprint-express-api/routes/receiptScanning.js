const express = require('express');
const router = express.Router();

const { uploadReceipt } = require('../controllers/receiptScanning');

router.post('/upload', uploadReceipt);

module.exports = router;
