const cadastrar = document.querySelector('#cadastrar');

function exibirAlerta() {
    alert("Pergunta cadastrada com sucesso!");
}

cadastrar.addEventListener('click', exibirAlerta);

document.querySelector(".cadastro-form").addEventListener("submit", async function (event) {
  event.preventDefault(); 
  const selectedCategoryId = document.getElementById("categoria").value;

  try {
    const response = await fetch(`/perguntas/${selectedCategoryId}`);
    const data = await response.json();

    const listaPerguntas = document.getElementById("lista-perguntas");
    listaPerguntas.innerHTML = "";

    data.forEach((item) => {
      const itemDaLista = document.createElement("li");
      itemDaLista.textContent = item.conteudo; 
      listaPerguntas.appendChild(itemDaLista);
    });
  } catch (error) {
    console.error("Erro ao buscar os dados da tabela:", error);
  }
});
