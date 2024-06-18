const seletorService = require("../Services/services.js");

module.exports = class validadorController {
  static async createValidator(req, res) {
    console.log(req.body);
    const { nome, ip, moedas } = req.body;
    console.log(moedas);

    if (moedas <= 50) {
      return res
        .json({
          msg: "Saldo Insuficiente... Necessario no Minimo 50 pryzyCoins",
        })
        .status(201);
    }

    const createValidatorResponse = await seletorService.createValidator(
      nome,
      ip,
      moedas,
      0
    );
    if (createValidatorResponse.status == 200) {
      return res
        .json({ msg: `Validador ${nome} criado com sucesso!` })
        .status(201);
    }
  }
};
