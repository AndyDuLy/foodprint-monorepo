const express = require('express');
const router = express.Router();

const receiptScannerRoutes = require('./receiptScanning');
const insightRoutes = require('./insightRoutes');
const userRoutes = require('./user');
const searchRoutes = require('./search');

router.use('/receipt', receiptScannerRoutes);
router.use('/insights', insightRoutes);
router.use('/users', userRoutes);
router.use('/search', searchRoutes);

module.exports = router;
