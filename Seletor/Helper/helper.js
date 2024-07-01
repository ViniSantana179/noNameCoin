const seletorService = require("../Services/services.js");

module.exports = class helper {
  static gerarChaveAleatoria() {
    // Metodo para gerar uma trasaction key para o validador
    const caracteres =
      "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let chave = "";
    for (let i = 0; i < 9; i++) {
      const indiceAleatorio = Math.floor(Math.random() * caracteres.length);
      chave += caracteres.charAt(indiceAleatorio);
    }
    return chave;
  }

  static async recompensar(status, valor, resultados, seletor) {
    // Validando o status da minha transacao

    console.log(status);
    console.log(valor);
    console.log(seletor.data);
    console.log(resultados);

    status = status;
    let totValidadoresRecompensa = 0;

    // Contabilizar os validadores que acertaram para divir a recompensa
    resultados.map((ele) => {
      if (ele.resultado_status == 1) totValidadoresRecompensa += 1;
    });

    // Recompensa do seletor (1.5% do to valor da transacao)
    let recompensaTotal = Math.round(valor * 0.015);
    //await seletorService.recompensaSeletor()

    // Recompensa do validor
    let recompensaSeletor = recompensaTotal / 3;
    let recompensaTotalValidador =
      (recompensaTotal - recompensaSeletor) / totValidadoresRecompensa;

    // Recompensando os seletores
    await seletorService.recompensaSeletor(
      seletor.data.id,
      recompensaSeletor.toFixed(2)
    );

    // Recompensando os validadores que acertaram e punindo os que erraram
    resultados.map(async (ele) => {
      if (ele.resultado_status == 1) {
        await seletorService.recompensaValidador(
          ele.id_validador,
          recompensaTotalValidador.toFixed(2)
        );
      } else {
        await seletorService.punirValidador(ele.id_validador);
      }
    });
  }
};
