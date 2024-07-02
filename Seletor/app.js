const express = require("express");
const axios = require("axios");
const app = express();
const seletorService = require("../Seletor/Services/services.js");
const PORT = 3000;

// Routes
const validadorRouter = require("./Routes/validadorRoute.js");
const helper = require("./Helper/helper.js");

app.use(
  express.urlencoded({
    extended: true,
  })
);

app.use(express.json());

app.use("/validador", validadorRouter);

async function run() {
  try {
    // Criar o validador
    const seletor = await seletorService.createSeletor();
    if (seletor.status === 200) {
      // Loop para checar os dados a cada 2 segundos
      const checkData = async () => {
        while (true) {
          // Tratando os dados do banco
          let data = await seletorService.getDados();
          if (data) {
            // Selecionando as transacoes novas que ainda nao foram validadas
            data = data.filter((transacao) => transacao.status == 0);

            // Se houver transacoes, eu repasso para os validadadores
            if (data.length > 0) {
              // TODO :: Selecionar os validadores
              let validadores = await seletorService.getValidadores();
              // Validadando o numero minimo de validadores e se estao em numero impar de validacoes (mantendo voto de minerva)
              if (validadores.length >= 3 && validadores.length % 2) {
                // Escolhendo os validadores de acordo com o total de moedas
                validadores = helper.selecionarValidadores(validadores);
                // TODO :: Enviar os dados para os validadores
                for (const transacao of data) {
                  console.log(
                    `==========> [${new Date()}] :: LOG :: (Transacao[${
                      transacao.id
                    }]) remetente[${transacao.remetente}] transferindo [${
                      transacao.valor
                    }] para recebedor[${transacao.recebedor}]`
                  );
                  let status = 0;
                  let valida = 0;
                  let invalida = 0;
                  let resultados = [];
                  for (const validador of validadores) {
                    const result = await seletorService.sendDados(
                      transacao,
                      validador
                    );
                    // Aramazenando as resposta dos validadores
                    resultados.push({
                      id_validador: validador.id,
                      resultado_status: result.data.status,
                    });

                    console.log(
                      `==========> [${new Date()}] :: LOG :: Validador [${
                        validador.nome
                      }] validou como [${result.data.status}]`
                    );

                    // Validando se a key que o validador retornou e a mesma que foi dada pelo seletor
                    if (validador.transaction_key == result.data.key) {
                      // Contabilizando as respostas dos validadores
                      if (result.data.status == 1) valida += 1;
                      else invalida += 1;
                    } else {
                      invalida += 1;
                    }
                  }

                  // Validando o status da minha transacao
                  if (valida > invalida) {
                    // Transacao aprovada
                    status = 1;
                    helper.recompensar(
                      status,
                      transacao.valor,
                      resultados,
                      seletor
                    );
                  } else if (valida < invalida) {
                    // Transacao nao aprovada
                    status = 2;
                    helper.recompensar(
                      status,
                      transacao.valor,
                      resultados,
                      seletor
                    );
                  }

                  // Atualizando minha transacao
                  await seletorService.updateTransactionStatus(
                    transacao.id,
                    status
                  );
                }
              } else {
                console.log(
                  `==========> [${new Date()}] :: LOG :: Não há validadores suficientes ou ha um numero par de validadores. Colocando a transação em espera.`
                );
              }
            } else {
              console.log(
                `==========> [${new Date()}] :: LOG :: Sem transacoes no momento ...`
              );
            }
          }
        }
      };
      checkData();
    } else {
      res.status(500).json({ error: "Failed to create data" });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}

app.listen(PORT, () => {
  run();
  console.log("Seletor Rodando");
});
