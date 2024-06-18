const express = require("express");
const router = express.Router();
const validadorController = require("../Controllers/validadorController.js");

router.post("/create", validadorController.createValidator);

module.exports = router;
