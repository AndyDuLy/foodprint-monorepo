const express = require('express');
const router = express.Router();

const { allUsers, createUser, deleteUser } = require('../controllers/user');

router.get('/allUsers', allUsers);
router.post('/newUser', createUser);
router.delete('/deleteUser', deleteUser);

module.exports = router;
