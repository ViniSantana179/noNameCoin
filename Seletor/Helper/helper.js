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
    let totValidadoresRecompensa = 0;
    // Contabilizar os validadores que acertaram para divir a recompensa
    resultados.map((ele) => {
      if (ele.resultado_status == status) totValidadoresRecompensa += 1;
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
      if (ele.resultado_status == status) {
        await seletorService.recompensaValidador(
          ele.id_validador,
          recompensaTotalValidador.toFixed(2)
        );
      } else {
        const validadorPunido = await seletorService.punirValidador(
          ele.id_validador
        );

        if (validadorPunido.data.flag_alerta == 3) {
          console.log(
            `==========> [${new Date()}] :: LOG :: Validador de ID [${
              ele.id_validador
            }] foi banido.`
          );
          await seletorService.banirValidador(ele.id_validador);
        }
      }
    });
  }

  static selecionarValidadores(validadores) {
    // estrutura que ira armazenar o validador e sua chance de escolha
    let validadorChances = [];

    // Encontrar o máximo de moedas disponível entre os validadores
    const maxMoedas = Math.max(
      ...validadores.map((validador) => validador.qtdMoeda)
    );

    // Calcular o percentual de escolha para cada validador
    validadores.forEach((validador) => {
      validadorChances.push(
        helper.calcularPercentualEscolha(validador, maxMoedas)
      );
    });

    // Selecionar validadores baseado no percentual de escolha
    let selecionados = [];
    while (selecionados.length < 3 || selecionados.length > 5) {
      selecionados = helper.weightedRandomChoices(
        validadorChances.map((vc) => vc.validador),
        validadorChances.map((vc) => vc.chance)
      );

      if (selecionados.length < 3) {
        // Adicionar validadores com os maiores percentuais até ter no mínimo 3
        const restantes = validadorChances.filter(
          (vc) => !selecionados.includes(vc)
        );
        restantes.sort((a, b) => b.chance - a.chance);
        const aAdicionar = restantes.slice(0, 3 - selecionados.length);
        selecionados = selecionados.concat(
          aAdicionar.map((vc) => vc.validador)
        );
      } else if (selecionados.length > 5) {
        // Remover validadores até ter no máximo 5
        selecionados.sort((a, b) => b.chance - a.chance);
        selecionados = selecionados.slice(0, 5);
      }
    }
    return selecionados;
  }

  static calcularPercentualEscolha(validador, maxMoedas) {
    // Calcular percentual base com base nas moedas
    let percentualBase = (validador.qtdMoeda / maxMoedas) * 20;

    // Ajustar percentual com base na flag_alerta
    if (validador.flag_alerta === 1) {
      percentualBase *= 0.5; // Redução de 50%
    } else if (validador.flag_alerta === 2) {
      percentualBase *= 0.25; // Redução de 75%
    }

    // Garantir que o percentual máximo não exceda 20%
    const percentualEscolha = Math.min(percentualBase, 20).toFixed(2);
    console.log(
      `==========> [${new Date()}] :: LOG :: Validador[${
        validador.nome
      }] tem ${percentualEscolha}% chance de ser escolhido.`
    );
    return { validador: validador, chance: percentualEscolha };
  }

  static weightedRandomChoices(items, weights) {
    const totalWeight = weights.reduce((sum, weight) => sum + weight, 0);
    const randomNum = Math.random() * totalWeight;
    let weightSum = 0;
    let chosen = [];

    for (let i = 0; i < items.length; i++) {
      weightSum += weights[i];
      if (randomNum <= weightSum) {
        chosen.push(items[i]);
        if (chosen.length >= 5) break; // Limite superior de 5 validadores
      }
    }
    return chosen;
  }
};
