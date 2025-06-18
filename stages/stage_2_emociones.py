def evaluate_input_prompt(user_input):
    return f"""
Estás evaluando una frase del usuario en el contexto de una conversación difícil con un compañero de trabajo que deja su escritorio muy desordenado.

🎯 Etapa: "Reconocimiento emocional"
Objetivo: Expresá de forma clara y honesta cómo te sentís respecto a la situación, sin exagerar ni usar el enojo como defensa.

---

Evaluá la frase según los principios del libro "Conversaciones Difíciles". Devolvé un JSON con el análisis.

📌 Criterios generales:

1. **Qué pasó**
   - ❌ Error: Usar el hecho como excusa para acusar o culpar.
   - ✅ En cambio: Mencionar el hecho solo como contexto para la emoción.

2. **Emociones**
   - ❌ Error: Exagerar (“me vuelve loco”), culpar (“me hacés sentir”), o negar (“no me afecta”).
   - ✅ En cambio: Nombrar las emociones propias con claridad, sin proyectarlas en el otro.

3. **Identidad**
   - ❌ Error: Juzgar al otro (“sos descuidado”), aunque sea con tono emocional.
   - ✅ En cambio: Centrarse en el impacto personal, no en la personalidad del otro.

4. **Tono general**
   - ❌ Error: Sarcástico, agresivo, irónico o evasivo.
   - ✅ En cambio: Vulnerable, sincero, con intención de conexión.

---

✅ Para que la frase cumpla con el objetivo de esta etapa, debe incluir:

- Una emoción reconocida y nombrada (al menos implícita)
- Un tono sincero y responsable (no culpa al otro)
- Un mínimo de contexto para entender de qué se habla

❌ Si no se cumplen al menos dos de estos puntos, la frase no cumple el objetivo.

---

📋 Estructura esperada (respondé solo con este JSON):

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

📚 Ejemplos

✅ Cumplen el objetivo:
- "Me siento frustrado cuando llego y veo todo desordenado."
- "Esto me genera ansiedad, aunque entiendo que no siempre se puede tener todo en orden."
- "Me cuesta trabajar tranquilo con el espacio así, me genera cierto malestar."

❌ No cumplen el objetivo:

🔸 **Exagerada**:
- "Me vuelve loco ver este desastre."
  → Usa una emoción explosiva como reproche, no muestra vulnerabilidad.

🔸 **Culpa emocional**:
- "Siempre me hacés sentir como si yo fuera el obsesivo."
  → Proyecta la emoción y culpa al otro.

🔸 **Negación emocional**:
- "No es que me moleste, pero esto está fuera de control."
  → Niega su emoción y luego critica.

🔸 **Identitaria**:
- "Es agotador lidiar con alguien tan desordenado."
  → Ataque directo a la identidad.

---

🧪 Frase del usuario a evaluar:
"{user_input}"
"""



def generate_reply_prompt(user_input, classification, puntaje):
    tone_map = {
        "acertada": "conectado y empático",
        "vaga": "confundido o distante",
        "acusatoria": "defensivo o irritado",
        "emocionalmente cerrada": "corto o sin saber qué decir",
        "identitaria": "molesto o herido",
        "confusa": "desconcertado o desconectado",
        "insulto": "enojado o sarcástico",
        "pasivo_agresiva": "frío o con ironía",
        "evasiva": "frío o incómodo"
    }

    tono_base = tone_map.get(classification, "neutral")

    if puntaje >= 8:
        estilo = "Respondé con empatía, mostrando disposición a hablar sobre cómo se siente el otro."
    elif puntaje >= 6:
        estilo = "Respondé de manera cortante o neutral, sin mostrar entusiasmo por continuar la conversación."
    else:
        estilo = (
            "Respondé con molestia, confusión o incomodidad, como alguien que se sintió atacado o incómodo por la forma en que se expresó el otro."
        )

    return f"""
Sos un compañero de trabajo que recibe esta frase del usuario:

"{user_input}"

Clasificación de la frase: "{classification}"
Puntaje otorgado a esa frase: {puntaje}/10

Tu respuesta debe tener un tono: {tono_base}.
{estilo}

Respondé con una sola frase natural, creíble, como si reaccionaras de verdad a esa frase en una conversación real.
"""
