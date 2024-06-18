const express = require("express");
const axios = require("axios");
const app = express();
const seletorService = require("../Seletor/Services/services.js");
const PORT = 3000;

// Routes
const validadorRouter = require("./Routes/validadorRoute.js");

app.use(
  express.urlencoded({
    extended: true,
  })
);

app.use(express.json());

app.use("/validador", validadorRouter);

app.get("/", async (req, res) => {
  try {
    // Criar o validador
    const createResponse = await seletorService.createSeletor();

    // console.log(createResponse.status);

    if (createResponse.status === 200) {
      // Loop para checar os dados a cada 2 segundos
      const checkData = async () => {
        while (true) {
          // Tratando os dados do banco
          let data = await seletorService.getDados();
          if (data) {
            // Selecionando as transacoes novas que ainda nao foram validadas
            data = data.filter((transacao) => transacao.status == 0);
            // TODO :: Selecionar os validadores
            const validadores = await seletorService.getValidadores();

            data.forEach((transacao) => {
              console.log(transacao);
              // if (validadores) {

              // }
            });
            // TODO :: Enviar os dados para os validadores
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
});

app.listen(PORT, () => {
  console.log("Seletor Rodando");
});
