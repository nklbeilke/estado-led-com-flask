const ledBtn = document.getElementById("ledBtn");
const statusTxt = document.getElementById("statusTxt");
const nomeAlunoInput = document.getElementById("nomeAluno");

let estadoAtual = 0;

// Carrega estado ao perder foco
nomeAlunoInput.addEventListener("blur", async () => {
  const nomeAluno = nomeAlunoInput.value.trim();
  if (!nomeAluno) return;

  try {
    const res = await fetch(`/api/led/${encodeURIComponent(nomeAluno)}`);
    const data = await res.json();
    estadoAtual = Number(data.estado_led); // força número
    atualizarInterface();
  } catch (err) {
    console.error("Erro ao buscar estado do LED:", err);
  }
});

// Alterna LED ao clicar
ledBtn.addEventListener("click", async () => {
  const nomeAluno = nomeAlunoInput.value.trim();
  if (!nomeAluno) {
    alert("Digite o nome do aluno!");
    return;
  }

  estadoAtual = estadoAtual === 1 ? 0 : 1; // alterna 0/1
  atualizarInterface();

  try {
    await fetch("/api/led", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nome_aluno: nomeAluno, estado_led: Number(estadoAtual) })
    });
  } catch (err) {
    console.error("Erro ao atualizar LED:", err);
  }
});

function atualizarInterface() {
  if (estadoAtual === 1) {
    ledBtn.textContent = "Ligado";
    ledBtn.style.backgroundColor = "#4CAF50";
    statusTxt.textContent = "LED está ligado";
  } else {
    ledBtn.textContent = "Desligado";
    ledBtn.style.backgroundColor = "#F44336";
    statusTxt.textContent = "LED está desligado";
  }
}
