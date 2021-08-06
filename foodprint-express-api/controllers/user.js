const db = require('../queries');

// /users/allUsers
const allUsers = async (req, res) => {
  db.pool.query('SELECT * FROM users ORDER BY id ASC', (error, results) => {
    if (error) return res.status(400).json({ message: error });
    
    return res.status(200).json({
      message: results.rows
    });
  })
}

// /users/newUser
const createUser = (req, res) => {
  const { name } = req.body

  db.pool.query('INSERT INTO users (name) VALUES ($1)', [name], (error, results) => {
    if (error) return res.status(400).json({ message: error });

    return res.status(201).send({
      message: `User added`,
    })
  })
}

// /users/deleteUser
const deleteUser = (req, res) => {
  const { id } = (req.body);

  db.pool.query('DELETE FROM users WHERE id = ($1)', [id], (error, results) => {
    if (error) return res.status(400).json({ message: error });

    return res.status(200).json({
      message: `User deleted`
    })
  })
}

module.exports = { allUsers, createUser, deleteUser };
