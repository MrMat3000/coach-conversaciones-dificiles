def evaluate_input_prompt(user_input):
    return f"""
Estás evaluando una frase escrita por alguien que practica una conversación difícil en el trabajo.

🎯 *Etapa actual: Búsqueda de solución*
Objetivo: Proponer posibles soluciones y mostrar disposición a encontrar un acuerdo que funcione para ambos.

La persona acaba de escribir la siguiente frase:
\"\"\"{user_input}\"\"\"

Tu tarea es analizar si esa frase:
- Incluye una propuesta tentativa, flexible o una invitación a encontrar soluciones en conjunto.
- Evita imponer, acusar o dar órdenes.
- Transmite apertura a negociar, colaborar y ajustar la solución según lo que el otro pueda decir.

---

📌 Criterios de evaluación comunes a todas las etapas:

1. **Qué pasó**
   - ❌ Error: Usar la propuesta como excusa para reiterar el problema o resaltar la culpa del otro.
   - ✅ En cambio: Referirse al problema solo como base para buscar una solución conjunta.

2. **Emociones**
   - ❌ Error: Formular la propuesta desde el enojo, la resignación o el sarcasmo.
   - ✅ En cambio: Mostrar voluntad de resolver, apertura y empátía.

3. **Identidad**
   - ❌ Error: Hacer sugerencias que implican que el otro es incapaz, infantil o perezoso.
   - ✅ En cambio: Asumir responsabilidad compartida sin señalar defectos del otro.

4. **Tono general**
   - ❌ Error: Imperativo, irónico, sárquico, pasivo-agresivo o derrotado.
   - ✅ En cambio: Tentativo, colaborativo, respetuoso y abierto a adaptar la solución.

---

✅ La frase cumple el objetivo si:
- Contiene una sugerencia o invitación a pensar juntos una solución.
- No suena impositiva, definitiva o autoritaria.
- Deja espacio para que el otro participe, responda o adapte la idea.

❌ No cumple el objetivo si:
- Ordena lo que el otro debe hacer.
- Usa amenazas, advertencias o ultimátums.
- No contiene ninguna propuesta ni apertura al cambio.

---

📦 Respondé con el siguiente formato JSON:

{{
  "objetivo": "Proponer posibles soluciones y mostrar disposición a encontrar un acuerdo que funcione para ambos.",
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

🎯 Ejemplos que SÍ cumplen el objetivo:
- “¿Te parece si antes de irnos dejamos cada uno su espacio ordenado?”
- “Se me ocurre que podríamos acordar una rutina para ordenar. ¿Vos qué pensás?”
- “No tengo una solución cerrada, pero me gustaría que pensemos juntos algo que funcione.”
- “Tal vez podría empezar dejando mis cosas listas cada viernes. ¿Hay algo que podrías hacer vos también?”

🚫 Ejemplos que NO cumplen el objetivo:

🔸 **Orden directa / imperativo**:
- “Tenés que ordenar todos los días antes de irte.”
  → Tono autoritario, no hay espacio para el otro.

🔸 **Amenaza / advertencia**:
- “Si no cambiás esto, voy a hablar con el jefe.”
  → Cierra la conversación con una condición punitiva.

🔸 **Resignación**:
- “Hacé lo que quieras, yo ya me cansé.”
  → No hay propuesta ni apertura.

🔸 **Manipulación emocional**:
- “Ya que no te importa cómo me siento, al menos podrías ordenar un poco.”
  → Usa culpa, no construcción conjunta.

🔸 **Falsa solución**:
- “Bueno, tratá de no dejar todo tirado, así estamos bien.”
  → Frase vaga, impersonal, no construye diálogo.

---

🔍 Importante: Una frase puede sonar amable pero seguir siendo impositiva o cerrada. No solo evalúes el tono, sino la verdadera disposición al acuerdo.

Respondé solo con el JSON.
"""

def generate_reply_prompt(user_input, classification, puntaje):
    tone_map = {
        "acertada": "colaborativo y dispuesto a negociar",
        "vaga": "cortante o desinteresado",
        "acusatoria": "defensivo",
        "amenaza": "enojado o reactivo",
        "orden": "molesto o desafiante",
        "resignada": "frustrado o cerrando el tema",
        "evasiva": "indiferente o sin compromiso"
    }

    tono_base = tone_map.get(classification, "neutral")

    if puntaje >= 8:
        matiz = "El tono debe mostrar interés genuino por encontrar una solución conjunta."
    elif puntaje >= 6:
        matiz = "El tono puede ser neutro, algo confuso, sin entusiasmo pero sin rechazo."
    else:
        matiz = "El tono debe ser cerrado, molesto, evasivo o desafiante."

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
