from flask import Flask, request, jsonify, render_template, session
import openai
import os
from dotenv import load_dotenv
import json
import importlib

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")

openai.api_key = os.getenv("OPENAI_API_KEY")

STAGES = [
    "Preparación y apertura",
    "Descripción del problema",
    "Reconocimiento emocional",
    "Exploración conjunta",
    "Búsqueda de solución"
]

STAGE_OBJECTIVES = [
    "Iniciá la conversación reconociendo que es un tema difícil y expresá tu intención de entender y colaborar, no de acusar.",
    "Explicá el problema desde tu punto de vista, evitando culpas y dejando espacio para la perspectiva del otro.",
    "Expresá de forma clara y honesta cómo te sentís respecto a la situación, sin exagerar ni usar el enojo como defensa.",
    "Mostrá interés por la visión del otro y buscá una comprensión conjunta de lo que está pasando.",
    "Proponé posibles soluciones y mostrá disposición a encontrar un acuerdo que funcione para ambos."
]

def get_stage_module(stage_index):
    module_names = [
        "stage_0_preparacion",
        "stage_1_descripcion",
        "stage_2_emociones",
        "stage_3_exploracion",
        "stage_4_solucion"
    ]
    try:
        return importlib.import_module(f"stages.{module_names[stage_index]}")
    except (IndexError, ModuleNotFoundError) as e:
        print(f"❌ Error al cargar módulo para la etapa {stage_index}: {e}")
        return None

def calcular_promedio_puntaje(feedback_json):
    criterios = feedback_json.get("criterios", {})
    total = 0
    count = 0
    for key, data in criterios.items():
        try:
            puntaje = int(data.get("puntaje", 0))
            criterios[key]["puntaje"] = puntaje
            total += puntaje
            count += 1
        except:
            criterios[key]["puntaje"] = 0
    promedio = round(total / count) if count > 0 else 0
    feedback_json["criterios"] = criterios
    feedback_json["puntaje"] = promedio
    return feedback_json

@app.route("/")
def index():
    if 'stage' not in session:
        session['stage'] = 0
    if 'scores' not in session:
        session['scores'] = []
    if 'dialogue' not in session:
        session['dialogue'] = []

    stage = session['stage']
    return render_template("index.html", stage_name=STAGES[stage], stage_description=STAGE_OBJECTIVES[stage])

@app.route("/analyze", methods=["POST"])
def analyze():
    user_input = request.json.get("message", "")
    stage = session.get("stage", 0)
    stage_name = STAGES[stage]

    stage_module = get_stage_module(stage)
    if not stage_module:
        return jsonify({"error": f"No se encontró la lógica para la etapa {stage}"}), 500

    try:
        openai_client = openai.OpenAI()

        # EVALUACIÓN
        evaluation_prompt = stage_module.evaluate_input_prompt(user_input)
        eval_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": evaluation_prompt}],
            temperature=0.4
        )

        eval_raw = eval_response.choices[0].message.content.strip()
        try:
            feedback_json = json.loads(eval_raw)
        except json.JSONDecodeError:
            return jsonify({"error": "No se pudo procesar la evaluación. Reformulá la frase e intentá de nuevo."}), 400

        feedback_json = calcular_promedio_puntaje(feedback_json)
        if feedback_json.get("puntaje", 0) < 6:
            feedback_json["cumple_objetivo"] = False

        # RESPUESTA DEL COMPAÑERO
        classification = feedback_json.get("clasificacion", "neutral")
        puntaje = feedback_json.get("puntaje", 0)
        reply_prompt = stage_module.generate_reply_prompt(user_input, classification, puntaje)

        reply_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": reply_prompt}],
            temperature=0.7
        )
        reply_text = reply_response.choices[0].message.content.strip()
        feedback_json["respuesta_companero"] = reply_text

        dialogue = session.get('dialogue', [])
        dialogue.append({
            "stage": stage_name,
            "user": user_input,
            "reply": reply_text
        })
        session['dialogue'] = dialogue

        scores = session.get('scores', [])
        passed = feedback_json["cumple_objetivo"] and feedback_json["puntaje"] >= 8
        if passed and len(scores) < len(STAGES):
            scores.append(feedback_json["puntaje"])
            session['scores'] = scores

        if passed and stage + 1 < len(STAGES):
            session['stage'] = stage + 1
            next_stage = STAGES[session['stage']]
            return jsonify({
                "feedback": feedback_json,
                "next_stage": next_stage
            })
        elif passed:
            return jsonify({
                "feedback": feedback_json,
                "next_stage": None,
                "show_report": True
            })
        else:
            return jsonify({
                "feedback": feedback_json,
                "next_stage": STAGES[stage]
            })

    except Exception as e:
        return jsonify({"error": f"Ocurrió un error inesperado: {str(e)}"}), 500

@app.route("/report", methods=["GET"])
def report():
    scores = session.get("scores", [])
    if not scores:
        return jsonify({"error": "No hay resultados disponibles."}), 400

    average = sum(scores) / len(scores)
    if average >= 9:
        summary = "Excelente manejo de la conversación. Mostraste una comunicación empática, clara y colaborativa en cada etapa."
    elif average >= 8:
        summary = "Muy buen trabajo. Lograste comunicarte efectivamente, aunque podrías pulir algunos detalles."
    else:
        summary = "Tuviste avances valiosos, pero hay margen para mejorar la claridad, el tono o el reconocimiento emocional."

    dialogue = session.get("dialogue", [])
    return jsonify({
        "scores": scores,
        "average": round(average, 2),
        "summary": summary,
        "dialogue": dialogue
    })

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=False)
