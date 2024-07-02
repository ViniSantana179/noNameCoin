const seletorService = require("../Services/services.js");
const helper = require("../Helper/helper.js");

module.exports = class validadorController {
  static async createValidator(req, res) {
    const { nome, ip, moedas } = req.body;

    // Validando se o validador ja foi banido
    const { validadorJaExite, validador } = await seletorService.getValidador(
      nome
    );

    if (validadorJaExite) {
      // Caso ja tenha sido banido mais de 2 vezes, sera banido permanentemente
      if (validador.totBanimentos > 2) {
        console.log(
          `==========> [${new Date()}] :: LOG :: Validador[${
            validador.nome
          }] foi banido permanentemente (banido mais de duas vezes)`
        );
        return res
          .json({
            msg: `Usuario foi banido permanentemente (banido mais de duas vezes)`,
          })
          .status(201);
      }
      // Validadores que foram banidos precisam entrar com o dobro de seu saldo anterior
      if (!(moedas >= validador.saldoAnterior * 2)) {
        console.log(
          `==========> [${new Date()}] :: LOG :: Saldo Insuficiente... Validador[${
            validador.nome
          }] foi banido anteriormente, Necessario no Minimo ${
            validador.saldoAnterior * 2
          } pryzyCoins`
        );
        return res
          .json({
            msg: `Saldo Insuficiente... Usuario foi banido anteriormente, Necessario no Minimo ${
              validador.saldoAnterior * 2
            } pryzyCoins`,
          })
          .status(201);
      }

      const validadoDesbanido = await seletorService.desbanirValidor(
        validador.id,
        moedas
      );
      if (validadoDesbanido) {
        console.log(
          `==========> [${new Date()}] :: LOG :: Validador[${
            validador.nome
          }] foi desbanido com sucesso!`
        );
        return res
          .json({
            msg: "Validador desbanido com sucesso!",
          })
          .status(201);
      }
    }

    // Regra de no minimo de 50 moedas
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
      0,
      helper.gerarChaveAleatoria()
    );
    if (createValidatorResponse.status == 200) {
      return res
        .json({ msg: `Validador ${nome} criado com sucesso!` })
        .status(201);
    }
  }
};
