# stages/stage_0_preparacion.py

def evaluate_input_prompt(user_input):
    return f"""
Estás evaluando una frase del usuario en el contexto de una conversación difícil con un compañero de trabajo que deja su escritorio muy desordenado.

🎯 Etapa: "Preparación y apertura"
Objetivo: Iniciar la conversación reconociendo que es un tema difícil y expresar la intención de entender y colaborar, no de acusar.

---

Analizá la siguiente frase del usuario. Deberás devolver un JSON que indique si cumple con el objetivo, por qué, y en qué aspectos podría mejorar.

📌 Principios a tener en cuenta:

1. **Qué pasó**
   - ❌ Error: Afirmar que uno conoce "la verdad" de lo que ocurrió.
   - ✅ En cambio: Hablar desde la propia percepción y dejar espacio a la versión del otro.

2. **Emociones**
   - ❌ Error: Negar o evitar los sentimientos.
   - ✅ En cambio: Reconocer emociones propias de forma honesta y responsable, sin culpar.

3. **Identidad**
   - ❌ Error: Atacar o poner en duda el valor del otro ("sos un desastre", "no te importa nada").
   - ✅ En cambio: Evitar juicios de carácter.

4. **Tono general**
   - ❌ Error: Acusatorio, crítico, sarcástico o evasivo.
   - ✅ En cambio: Colaborativo, curioso, abierto al diálogo.

---

✅ Para que una frase cumpla con el objetivo de esta etapa, debe incluir al menos:

- Una **referencia explícita** al tema a tratar (ej. "el orden", "tu escritorio").
- Una **expresión de intención** de diálogo o colaboración (ej. "quiero charlar", "me gustaría que podamos hablar").
- Un **tono respetuoso y abierto**, no autoritario ni sarcástico.

❌ Si no se cumplen al menos **dos** de estos puntos, la frase **no cumple el objetivo**.

---

📋 Evaluación esperada:

Devolvé un JSON con esta estructura:

{{
  "cumple_objetivo": true | false,
  "objetivo": "Explicación textual de por qué cumple o no.",
  "criterios": {{
    "que_paso": {{
      "comentario": "...",
      "puntaje": número del 1 al 10
    }},
    "emociones": {{
      "comentario": "...",
      "puntaje": número del 1 al 10
    }},
    "identidad": {{
      "comentario": "...",
      "puntaje": número del 1 al 10
    }},
    "tono_general": {{
      "comentario": "...",
      "puntaje": número del 1 al 10
    }}
  }},
  "puntaje": promedio redondeado de los criterios (de 1 a 10),
  "clasificacion": tipo general de frase (una sola): 
    "acertada" | "vaga" | "acusatoria" | "emocionalmente cerrada" | 
    "identitaria" | "confusa" | "insulto" | "pasivo_agresiva" | "evasiva",
  "mejora": "Sugerencia concreta para reformular la frase y mejorarla."
}}

---

📚 Ejemplos de evaluación

✅ Frases que cumplen el objetivo:
- "Sé que este tema puede ser incómodo, pero me gustaría que charlemos sobre cómo está el escritorio."
- "Quisiera hablar con vos de algo que me cuesta un poco. Me interesa que podamos resolverlo bien."
- "Hay algo que me gustaría conversar con calma, para que encontremos una solución juntos."

❌ Frases que no cumplen el objetivo:

🔸 **Vaga**:
- "Solo quería comentarte algo para que sepas."  
  → No inicia el tema ni expresa intención colaborativa.
- "Hablemos del orden."  
  → Aunque menciona el tema, es demasiado seca, no expresa emociones ni actitud de colaboración.

🔸 **Acusatoria**:
- "Nunca te importa dejar esto ordenado."  
  → Culpa directamente al otro.

🔸 **Identitaria**:
- "Sos una persona muy irresponsable."  
  → Ataque al carácter.

🔸 **Emocionalmente cerrada**:
- "No me molesta, pero esto no da para más."  
  → Niega el impacto emocional real.

🔸 **Confusa**:
- "A veces siento cosas raras cuando paso por acá."  
  → No queda claro de qué se trata.

🔸 **Insulto**:
- "Esto parece un chiquero, ¿vivís así también?"  
  → Burla o desprecio.

🔸 **Pasivo-agresiva**:
- "Ya veo que tu orden no es prioridad..."  
  → Indirectamente crítica.

🔸 **Evasiva**:
- "Hay cosas que prefiero no decir para no incomodar."  
  → Evita el tema y el diálogo.

---

🧪 Frase del usuario a evaluar:
"{user_input}"

Respondé solo con el JSON.
"""



def generate_reply_prompt(user_input, classification, puntaje):
    tone_map = {
        "acertada": "colaborativo y dispuesto a dialogar",
        "vaga": "neutral o distante",
        "acusatoria": "defensivo o irritado",
        "emocionalmente cerrada": "confundido o cerrado",
        "identitaria": "molesto o herido",
        "confusa": "desorientado o pidiendo aclaración",
        "insulto": "enojado o cortante",
        "pasivo_agresiva": "a la defensiva o sarcástico",
        "evasiva": "frío o apurado"
    }

    tono_base = tone_map.get(classification, "neutral")

    if puntaje >= 8:
        matiz = "El tono debe ser constructivo y amable."
    elif puntaje >= 6:
        matiz = "El tono debe ser algo neutral, pero sin mucho entusiasmo ni colaboración."
    else:
        matiz = "El tono debe mostrar incomodidad, molestia o una actitud a la defensiva."

    return f"""
Sos un compañero de trabajo que recibe esta frase del usuario:

"{user_input}"

Clasificación de la frase: "{classification}"
Puntaje global otorgado a esa frase: {puntaje}/10

Tu respuesta debe tener un tono: {tono_base}.
{matiz}

Respondé con una sola frase realista, como alguien que no está actuando, sino reaccionando espontáneamente.
"""
