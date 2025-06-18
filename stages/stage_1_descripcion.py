# stages/stage_1_descripcion.py

def evaluate_input_prompt(user_input):
    return f"""
Estás evaluando una frase del usuario en el contexto de una conversación difícil con un compañero de trabajo que deja su escritorio muy desordenado.

🎯 Etapa: "Descripción del problema"
Objetivo: Explicar el problema desde tu punto de vista, evitando culpas y dejando espacio para la perspectiva del otro.

---

Evaluá la frase según los principios del libro "Conversaciones Difíciles". Devolvé un JSON con el análisis.

📌 Principios a tener en cuenta (criterios comunes):

1. **Qué pasó**
   - ❌ Error: Describir el problema como un hecho absoluto (“siempre dejás todo tirado”).
   - ✅ En cambio: Hablar desde la propia observación y experiencia concreta.

2. **Emociones**
   - ❌ Error: Ocultar emociones, exagerarlas o usarlas como reproche.
   - ✅ En cambio: Reconocer cómo te afecta la situación, sin dramatizar ni culpar.

3. **Identidad**
   - ❌ Error: Juzgar al otro como persona (“sos desordenado”, “no te importa nada”).
   - ✅ En cambio: Centrarse en comportamientos observables, no en características personales.

4. **Tono general**
   - ❌ Error: Sarcástico, acusador, exasperado o pasivo-agresivo.
   - ✅ En cambio: Claro, sincero, abierto, dejando lugar a la visión del otro.

---

✅ Para que la frase cumpla con el objetivo de esta etapa, debe incluir:

- Una descripción concreta del problema (no ambigua ni evasiva).
- Una referencia a cómo eso te afecta o cómo lo percibís.
- Un tono que deje espacio para la perspectiva del otro.

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
- "Me cuesta concentrarme cuando hay muchas cosas sobre el escritorio."
- "Últimamente me frustro cuando veo tanto desorden."
- "Me afecta llegar a la oficina y encontrar todo así."

❌ No cumplen el objetivo:

🔸 **Acusatoria**:
- "Nunca ordenás nada."
  → Culpa directa, exagera, no deja espacio al otro.

🔸 **Identitaria**:
- "Sos un desastre con tus cosas."
  → Ataque a la persona.

🔸 **Emocionalmente cerrada**:
- "No es por mí, pero alguien tiene que decirlo."
  → Niega el impacto personal.

🔸 **Vaga**:
- "No me parece que esté bien esto."
  → No queda claro a qué se refiere ni cómo lo afecta.

🔸 **Pasivo-agresiva**:
- "Algunos tienen un concepto muy relajado del orden."
  → Crítica indirecta, sarcástica.

---

🧪 Frase del usuario a evaluar:
"{user_input}"
"""

def generate_reply_prompt(user_input, classification, puntaje):
    tone_map = {
        "acertada": "colaborativo y dispuesto a dialogar",
        "vaga": "frustrado o distante",
        "acusatoria": "a la defensiva o irritado",
        "emocionalmente cerrada": "confundido o cerrado",
        "identitaria": "molesto o herido",
        "confusa": "desconcertado o pidiendo aclaración",
        "insulto": "enojado o cortante",
        "pasivo_agresiva": "irónico o sarcástico",
        "evasiva": "frío o evasivo"
    }

    tono_base = tone_map.get(classification, "neutral")

    if puntaje >= 8:
        estilo = "Respondé de forma amable, receptiva y con voluntad de colaborar."
    elif puntaje >= 6:
        estilo = "Respondé con un tono algo neutral, como alguien que no se siente atacado pero tampoco entusiasmado por dialogar."
    else:
        estilo = (
            "Respondé de forma incómoda, molesta o defensiva, como alguien que no se siente cómodo con cómo fue planteado el tema. "
            "No respondas con disposición a colaborar. No suavices la tensión: respondé como lo haría una persona real en una situación tensa."
        )

    return f"""
Sos un compañero de trabajo que recibe esta frase del usuario:

"{user_input}"

Clasificación de la frase: "{classification}"
Puntaje general otorgado a esa frase: {puntaje}/10

Tu reacción debe tener un tono: {tono_base}.
{estilo}

Respondé con una sola frase natural y creíble, como alguien que reacciona espontáneamente en una conversación real.
"""
