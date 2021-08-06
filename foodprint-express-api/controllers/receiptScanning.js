require("dotenv").config({ path: "../.env" });
const db = require('../queries');

const request = require('request');
const fuzz = require('fuzzball');
const csv = require('csv-parser');
const fs = require('fs');
const { v4 : uuidv4 } = require('uuid');

const Client = require("@veryfi/veryfi-sdk");
const client_id = process.env.CLIENT_ID;
const client_secret = process.env.CLIENT_SECRET;
const username = process.env.USERNAME;
const api_key = process.env.API_KEY;


// /receipt/upload
const uploadReceipt = async (req, res) => {
  try {    
    let VERYFI_CLIENT = new Client(client_id, client_secret, username, api_key);
    let response = await VERYFI_CLIENT.process_document(req.body.file_path);
    
    const emissions = await lineItemCleaner(response)
    const receiptID = uuidv4();
    const vendorName = response.vendor.name;
    const receiptDate = response.date;

    const obj = {
      message: "test",
      emission: emissions
    }

    var clientServerOptions = {
      uri: `${FLASK_EMISSIONS_UNWEIGHED_ENDPOINT}`,
      body: JSON.stringify({
        obj
      }),
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    }

    // Hit Flask API for emissions calculations
    request(clientServerOptions, function (error, response) {
      const ems = response.body;
      const parsed = JSON.parse(ems);
      
      // PSQL write for each line item and relevant emissions data
      parsed.list.forEach(item => {
        db.pool.query(
          'INSERT INTO receipt (receipt_date, user_id, receipt_id, merchant_name, item_name, item_amount, item_emissions, item_category, item_sku) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
          [receiptDate, "-1", receiptID, vendorName, item.product, item.amount, item.rounded_emissions, item.product_category, item.sku], (error, results) => {

          if (error) console.log(error);
        })
      });
    });

    return res.status(200).json({
      message: "Receipt Upload Successful",
      receipt_id: receiptID
    });
  } catch (err) {
    return res.status(400).json({
      error: err.message
    });
  }
}

// FuzzyWuzzy string matching with .csv and line_items
const lineItemCleaner = (veryfi_response) => {
  const line_items = veryfi_response.line_items;

  var choices = [],
      matches;
      
  const options = {
    scorer: fuzz.token_set_ratio,
    returnObjects: true
  };

  return new Promise((res, rej) => {
    fs.createReadStream(`${process.env.fuzzywuzzy_nlp_csv}`)
    .pipe(csv())
    .on('data', (data) => {
      choices.push(data.display_name)
    })
    .on('end', () => {
      let emissions = [];

      line_items.forEach((line) => {
        const slug = line.description.split("\n");

        matches = fuzz.extract(slug[0], choices, options);

        let temp = {
          ...matches[0],
          price: line.total,
          sku: line.sku
        };

        emissions.push(temp);
      });

      res(emissions);
    });
  })
}

module.exports = { uploadReceipt };
