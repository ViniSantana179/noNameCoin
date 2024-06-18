const axios = require("axios");
const { json } = require("express");

module.exports = class SeletorService {
  static async getDados() {
    try {
      // Verificando as trasancoes
      await new Promise((resolve) => setTimeout(resolve, 10000));
      try {
        const checkResponse = await axios.get(
          "http://127.0.0.1:5000/transacoes"
        );

        if (checkResponse.status === 200) {
          return checkResponse.data;
        }
      } catch (error) {
        console.log("Dados não encontrados, tentando novamente...");
      }
    } catch (error) {
      console.log("OPS");
    }
  }

  static async createSeletor() {
    // Criar o seletor
    const createResponse = await axios.post(
      "http://127.0.0.1:5000/seletor/sel1/127.0.0.1:3000"
    );
    return createResponse;
  }

  static async createValidator(nome, ip, qtdMoedas, alertas) {
    // Criar o validador
    const createResponse = await axios.post(
      `http://127.0.0.1:5000/validador/${nome}/${ip}/${qtdMoedas}/${alertas}`
    );
    return createResponse;
  }

  static async getValidadores() {
    // Busca os validadores
    let validadores = await axios.get(`http://127.0.0.1:5000/validador`);
    // Selecionando apenas validadores que nao foram banidos
    validadores = validadores.data.filter(
      (validador) => validador.flag_alerta < 3
    );
    console.log(validadores);
    return validadores;
  }

  static async sendDados() {
    // Envia os dados para os validadores
  }
};
