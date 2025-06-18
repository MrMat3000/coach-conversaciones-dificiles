let etapaSuperada = false;

async function sendMessage() {
  const input = document.getElementById("userMessage");
  const enviarBtn = document.getElementById("enviarBtn");
  const message = input.value.trim();
  const feedbackBox = document.getElementById("feedback");
  const reportBox = document.getElementById("reporteFinal");
  const actionBtn = document.getElementById("actionBtn");
  const respuestaDiv = document.getElementById("respuestaBot");
  const imagen = document.getElementById("imagenCompanero");
  const textoCompanero = document.getElementById("textoCompanero");
  const inputContainer = document.getElementById("userInputDisplay");

  if (!message) {
    feedbackBox.textContent = "Por favor escribí una frase antes de enviar.";
    return;
  }

  input.style.display = "none";
  enviarBtn.style.display = "none";

  if (inputContainer) {
    inputContainer.innerHTML = `<p style="font-weight:bold;">🙋‍♂️ Usuario:</strong> ${message}</p>`;
  }

  feedbackBox.innerHTML = "Analizando...";
  reportBox.innerHTML = "";
  actionBtn.style.display = "none";
  respuestaDiv.style.display = "none";
  respuestaDiv.classList.remove("positivo", "negativo");

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await response.json();

    if (data.error) {
      feedbackBox.innerHTML = `<span style="color: red;">${data.error}</span>`;
      return;
    }

    const f = data.feedback;
    etapaSuperada = f.cumple_objetivo && f.puntaje >= 8;

    textoCompanero.innerText = f.respuesta_companero || "[El compañero no respondió]";
    respuestaDiv.style.display = "block";

    if (etapaSuperada) {
      respuestaDiv.classList.add("positivo");
      imagen.src = "/static/bien.jpg";
    } else {
      respuestaDiv.classList.add("negativo");
      imagen.src = "/static/mal.jpg";
    }

    let html = `<strong>🎯 Objetivo:</strong><p>${f.objetivo}</p>`;

    html += `<strong>📋 Evaluación por criterio:</strong><ul>`;
    html += `<li><strong>Qué pasó:</strong> ${f.criterios.que_paso.comentario} <em>(${f.criterios.que_paso.puntaje}/10)</em></li>`;
    html += `<li><strong>Emociones:</strong> ${f.criterios.emociones.comentario} <em>(${f.criterios.emociones.puntaje}/10)</em></li>`;
    html += `<li><strong>Identidad:</strong> ${f.criterios.identidad.comentario} <em>(${f.criterios.identidad.puntaje}/10)</em></li>`;
    html += `<li><strong>Tono general:</strong> ${f.criterios.tono_general.comentario} <em>(${f.criterios.tono_general.puntaje}/10)</em></li>`;
    html += `</ul>`;

    html += `<strong>🧮 Puntuación general:</strong> ${f.puntaje}/10<br><br>`;
    html += `<strong>🔧 Sugerencia para mejorar:</strong><p>${f.mejora}</p>`;

    feedbackBox.innerHTML = html;

    if (data.next_stage === null && data.show_report) {
      mostrarBoton("Ver reporte");
    } else {
      mostrarBoton(etapaSuperada ? "Siguiente etapa" : "Volver a intentarlo");
    }
  } catch (err) {
    feedbackBox.innerHTML = `<span style="color:red;">Error de conexión. Por favor, volvé a intentarlo.</span>`;
  }
}

function mostrarBoton(texto) {
  const actionBtn = document.getElementById("actionBtn");
  actionBtn.textContent = texto;
  actionBtn.style.display = "inline-block";
}

function accionEtapa() {
  const input = document.getElementById("userMessage");
  const enviarBtn = document.getElementById("enviarBtn");
  const feedbackBox = document.getElementById("feedback");
  const actionBtn = document.getElementById("actionBtn");
  const reportBox = document.getElementById("reporteFinal");
  const respuestaDiv = document.getElementById("respuestaBot");
  const inputContainer = document.getElementById("userInputDisplay");

  if (actionBtn.textContent === "Ver reporte") {
    verReporte();
    actionBtn.style.display = "none";
    return;
  }

  if (etapaSuperada) {
    location.reload();
  } else {
    input.value = "";
    input.focus();
    input.style.display = "block";
    enviarBtn.style.display = "inline-block";
    feedbackBox.innerHTML = "";
    reportBox.innerHTML = "";
    respuestaDiv.style.display = "none";
    respuestaDiv.classList.remove("positivo", "negativo");
    actionBtn.style.display = "none";
    if (inputContainer) inputContainer.innerHTML = "";
  }
}

async function verReporte() {
  const reportBox = document.getElementById("reporteFinal");
  reportBox.textContent = "Generando reporte...";

  const response = await fetch("/report");
  const data = await response.json();

  if (data.error) {
    reportBox.textContent = "Error: " + data.error;
    return;
  }

  let html = `<h3>📊 Reporte final</h3>`;
  html += `<p><strong>Puntajes por etapa:</strong></p><ul>`;
  data.scores.forEach((score, index) => {
    html += `<li><strong>Etapa ${index + 1}:</strong> ${score}/10</li>`;
  });
  html += `</ul>`;
  html += `<p><strong>Promedio:</strong> ${data.average}/10</p>`;
  html += `<p><strong>Análisis general:</strong> ${data.summary}</p>`;

  if (data.dialogue && data.dialogue.length > 0) {
    html += `<h4>🗨️ Transcripción:</h4><div style="border-left: 4px solid #ccc; padding-left: 10px;">`;
    data.dialogue.forEach((entry, i) => {
      html += `<p><strong>Etapa ${i + 1} – ${entry.stage}</strong></p>`;
      html += `<p><strong>Usuario:</strong> ${entry.user}</p>`;
      if (entry.reply) html += `<p><strong>Compañero:</strong> ${entry.reply}</p>`;
      html += `<hr>`;
    });
    html += `</div>`;
  }

  reportBox.innerHTML = html;
}

async function reiniciarPractica() {
  const confirmReset = confirm("¿Estás seguro de que querés reiniciar la práctica desde cero?");
  if (!confirmReset) return;

  const response = await fetch("/reset", { method: "POST" });
  const data = await response.json();

  if (data.success) {
    location.reload();
  }
}

window.onload = () => {
  const input = document.getElementById("userMessage");
  const enviarBtn = document.getElementById("enviarBtn");

  input.focus();

  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
};
