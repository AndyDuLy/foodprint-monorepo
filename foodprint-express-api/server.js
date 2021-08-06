require("dotenv").config({ path: "./.env" });

const express = require("express");
const cors = require('cors');
const http = require('http');

const routes = require('./routes/index');

const PORT = `${process.env.PORT}`;

const app = express();
const server = http.createServer(app);

app.use(express.json());
app.options('*', cors());

app.use(routes);
app.use("/api", (req, res, next) => {
  res.send("base endpoint");
});

server.listen(PORT, () => {
  console.log(`server listening on port ${PORT}`);
});
