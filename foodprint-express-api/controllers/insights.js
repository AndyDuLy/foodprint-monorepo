require("dotenv").config({ path: "../.env" });
const db = require('../queries');

const request = require('request');

// /insights/get
const getInsights = async (req, res) => {
  try {    
    const flask_req = { "receipt_id": req.body.receipt_id }

    var clientServerOptions = {
      uri: `${FLASK_INSIGHTS_ENDPOINT}`,
      body: JSON.stringify({
        flask_req
      }),
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    }

    // Hit Flask API for emissions calculations
    request(clientServerOptions, function (error, response) {
      if (error) console.log(error)

      const resp = JSON.parse(response.body);

      db.pool.query(
        'INSERT INTO insights (receipt_id, meat, nomeat, general_1) VALUES ($1, $2, $3, $4)',
        [flask_req.receipt_id, resp.meat_insight, resp.no_meat_insight, resp.generalinsight], (error, results) => {

        if (error) console.log(error);
      })

      return res.status(200).json({
        message: "Insight Generated",
        insight: response.body 
      });
    });
  } catch (err) {
    return res.status(400).json({
      error: err.message
    });
  }
}

module.exports = { getInsights };
