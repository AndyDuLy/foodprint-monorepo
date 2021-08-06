const db = require('../queries');

// /search/food
const searchFood = async (req, res) => {
  const { nlp_search } = req.body;

  db.pool.query('SELECT * FROM individual_food_emissions WHERE display_name = ($1)', [nlp_search], (error, results) => {
    if (error) return res.status(400).json({ message: error });
    
    return res.status(200).json({
      message: results.rows
    });
  })
}

module.exports = { searchFood };
