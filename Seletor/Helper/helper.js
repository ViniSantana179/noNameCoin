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
};
