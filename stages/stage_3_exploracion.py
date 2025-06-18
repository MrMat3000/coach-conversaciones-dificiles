def evaluate_input_prompt(user_input):
    return f"""
Estás evaluando una frase escrita por alguien que practica una conversación difícil en el trabajo.

🎯 *Etapa actual: Exploración conjunta*
Objetivo: Mostrar interés genuino por la perspectiva del otro y abrir un espacio de comprensión compartida.

La persona acaba de escribir la siguiente frase:
\"\"\"{user_input}\"\"\"

Tu tarea es analizar si esa frase:
- Muestra apertura a la visión del otro.
- Invita a explorar las causas del problema en conjunto.
- Evita juicios, acusaciones o supuestos sobre el otro.
- Usa un tono curioso y colaborativo.

---

📌 Criterios de evaluación comunes a todas las etapas:

1. **Qué pasó**
   - ❌ Error: Afirmar verdades absolutas o suposiciones sobre lo que ocurrió.
   - ✅ En cambio: Reconocer que puede haber múltiples perspectivas.

2. **Emociones**
   - ❌ Error: Evitar por completo las emociones o manipularlas.
   - ✅ En cambio: Reconocer emociones propias o abrir espacio para las del otro.

3. **Identidad**
   - ❌ Error: Poner en duda la competencia, responsabilidad o intención del otro.
   - ✅ En cambio: Cuidar que la frase no amenace la imagen del otro.

4. **Tono general**
   - ❌ Error: Tono defensivo, irónico, sarcástico o evasivo.
   - ✅ En cambio: Curioso, constructivo, con disposición real a dialogar.

---

✅ Para que la frase cumpla el objetivo de esta etapa, debe cumplir al menos **dos** de estos elementos:
- Contener una pregunta abierta o una frase que explícitamente invite a conocer la perspectiva del otro.
- Mostrar disposición a escuchar, sin dar por sentado lo que pasó ni acusar.
- Tener un tono de apertura, interés o colaboración.

❌ No cumple el objetivo si:
- No hay señal de querer entender al otro.
- Usa preguntas que encubren juicios (“¿Por qué siempre hacés esto?”).
- El tono es frío, impaciente o evasivo.

---

📦 Respondé con el siguiente formato JSON:

{{
  "objetivo": "Mostrar interés por la visión del otro y buscar una comprensión conjunta de lo que está pasando.",
  "cumple_objetivo": true/false,
  "clasificacion": "...",
  "criterios": {{
    "que_paso": {{"puntaje": 0-10, "comentario": "..."}},
    "emociones": {{"puntaje": 0-10, "comentario": "..."}},
    "identidad": {{"puntaje": 0-10, "comentario": "..."}},
    "tono_general": {{"puntaje": 0-10, "comentario": "..."}}
  }},
  "mejora": "Frase alternativa o sugerencia concreta para mejorar."
}}

---

🎯 Ejemplos de frases que sí cumplen el objetivo:
- “Me interesa entender cómo ves vos esta situación.”
- “¿Cómo te sentís vos con todo esto?”
- “Quizás hay cosas que no estoy viendo. ¿Querés contarme cómo lo vivís vos?”
- “Capaz estoy interpretando mal algo, y quiero entender tu lado.”
- “No quiero sacar conclusiones sin saber tu parte.”

🚫 Ejemplos que NO cumplen el objetivo:
🔸 **Acusatoria**:
- “Siempre hacés lo mismo y después decís que no entendés.” → Asume culpa, cierra diálogo.

🔸 **Juicio encubierto**:
- “No entiendo por qué hacés esto.” → Parece pregunta, pero implica juicio.

🔸 **Cerrada**:
- “Bueno, vos verás.” o “Ya está, no me importa lo que digas.” → Niega interés.

🔸 **Sarcástica / evasiva**:
- “¿Y ahora qué excusa vas a poner?”

🔸 **Vaga**:
- “Hablemos.” → No da contexto ni muestra interés real.

🔸 **Fría**:
- “Me gustaría discutirlo.” → Podría ser amable, pero no transmite curiosidad ni apertura real.

---

🔍 Importante: Si la frase parece neutral pero no invita activamente a la perspectiva del otro, no cumple el objetivo. Sé exigente.

Respondé solo con el JSON.
"""

def generate_reply_prompt(user_input, classification, puntaje):
    tone_map = {
        "acertada": "abierto y dispuesto a dialogar",
        "monólogo": "algo distante o confundido",
        "acusatoria": "a la defensiva",
        "cerrada": "con desinterés o fastidio",
        "juicio_encubierto": "sarcástico o enojado",
        "vaga": "neutro o desconcertado",
        "fría": "corto o seco"
    }

    tono_base = tone_map.get(classification, "neutral")

    if puntaje >= 8:
        matiz = "El tono debe ser constructivo, interesado y colaborativo."
    elif puntaje >= 6:
        matiz = "El tono puede ser neutro, algo confuso, sin mucho entusiasmo."
    else:
        matiz = "El tono debe mostrar incomodidad, molestia o evasión."

    return f"""
Sos un compañero de trabajo en una oficina. Un colega quiere hablar con vos porque dejás tu escritorio muy desordenado y eso le está trayendo problemas.

Ahora ese colega te dice esta frase:

\"{user_input}\"

Clasificación de la frase: \"{classification}\"
Puntaje global otorgado a esa frase: {puntaje}/10

Tu respuesta debe tener un tono: {tono_base}.
{matiz}

Respondé con una sola frase realista, como alguien que no está actuando, sino reaccionando espontáneamente a ese comentario.
"""
