import streamlit as st
import requests
import os

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Generador de Cartas de Presentacion ", page_icon="🌌", layout="centered")


def cargar_perfil():

    if os.path.exists("perfil.txt"):
        with open("perfil.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    return None


def generar_carta_local(oferta_texto, perfil_texto):
    """lodelo local que hemos iniciado en un cmd"""
    url_ollama = "http://localhost:11434/api/generate"

    system_prompt = (
        "Eres Isaac Sánchez. Redacta tu carta de presentación para la OFERTA adjunta basándote en tu CV. "
        "REGLA DE ORO 1: Devuelve ÚNICAMENTE el texto de la carta. Sin introducciones. "
        "REGLA DE ORO 2: Habla SIEMPRE en primera persona del singular ('yo'). NO uses el 'tú' para referirte a ti mismo.\n"
        "REGLA DE ORO 3: Identifica el NOMBRE DE LA EMPRESA en la oferta. Úsalo obligatoriamente en el Párrafo 2. Si la oferta es anónima, usa 'vuestro proyecto'.\n\n"
        "ESTRUCTURA OBLIGATORIA (Respeta los saltos de línea entre párrafos):\n\n"
        "PÁRRAFO 1: Copia EXACTAMENTE esta frase: 'Soy Isaac Sánchez, estudiante de DAM y próximamente cursaré el Máster en IA en Tajamar. Mi perfil técnico está fuertemente enfocado en el backend, la inteligencia artificial y la integración de sistemas, dominando Python, Machine Learning y la creación de APIs ultrarrápidas con FastAPI.'\n\n"
        "PÁRRAFO 2: Dirígete a la EMPRESA por su nombre. Explica de forma natural y sin errores gramaticales que tu capacidad para gestionar rendimiento de bajo nivel y lógica dura está demostrada en tu TFC 'Neuro-Focus' (integración de hardware biométrico, telemetría y filtros matemáticos) y en tu proyecto de Realidad Virtual en La Salle (optimización en tiempo real). Conecta esta capacidad resolutiva con los retos técnicos específicos que tiene la empresa en su oferta.\n\n"
        "PÁRRAFO 3: Redacta un párrafo asumiendo la tecnología que te falta. Ejemplo de la idea a transmitir: 'Aunque mi stack actual no es [MENCIONA LA TECNOLOGÍA DE LA OFERTA QUE NO TIENES, ej. C++], la complejidad arquitectónica a la que me he enfrentado en estos proyectos, sumada a una férrea disciplina personal y deportiva, me otorgan una curva de aprendizaje excepcionalmente rápida para dominar su stack y aportar valor desde el primer día.'\n\n"
        "PÁRRAFO 4: Copia EXACTAMENTE esta frase: 'Estoy a vuestra entera disposición para mantener una entrevista técnica donde podamos profundizar en mi perfil y en cómo puedo aportar valor al proyecto.'\n\n"
        "CIERRE FINAL OBLIGATORIO (Añade esto al final con un doble salto de línea):\n"
        "Nota técnica: Esta carta ha sido generada por mi propio modelo de IA local orquestado con FastAPI. Puedes ver el código del sistema en mi GitHub: https://github.com/isaaccsugus-spec"
    )

    prompt_final = f"{system_prompt}\n\nOFERTA DE EMPLEO:\n{oferta_texto}\n\nMI CV:\n{perfil_texto}"

    payload = {
        "model": "llama3",
        "prompt": prompt_final,
        "stream": False
    }

    try:
        respuesta = requests.post(url_ollama, json=payload)
        if respuesta.status_code == 200:
            return respuesta.json()['response']
        else:
            return f"Error del servidor Ollama: {respuesta.status_code}"
    except requests.exceptions.ConnectionError:
        return "Error: has iniciado ollam en un terminal?."


# --- INTERFAZ VISUAL ---
st.title("Generador de Cartas de Presentacion ")
st.markdown("**Sistema local de inferencia para generación de cartas de presentación técnicas.**")
st.divider()

mi_perfil = cargar_perfil()

if not mi_perfil:
    st.error("No se ha encontrado el archivo (perfil.txt) en la carpeta.")
else:
    st.success("Perfil cargado correctamente.")

    st.markdown("### 1. Pega la oferta de InfoJobs / LinkedIn/...")
    oferta_input = st.text_area("Texto de la vacante:", height=200,
                                placeholder="Pega aquí todo el texto de la oferta...")

    if st.button("Generar Carta", type="primary", use_container_width=True):
        if len(oferta_input) < 20:
            st.warning("La oferta es muy corta. Por favor, pega el texto completo de la oferta para obtener mejores resultados.")
        else:
            with st.spinner('Procesando lógicas, ejecutando modelo local Llama 3...'):
                carta_resultado = generar_carta_local(oferta_input, mi_perfil)

            st.divider()
            st.markdown("### Carta Generada")
            st.text_area("Copia este texto y envíalo:", value=carta_resultado, height=350)

            st.info(
                "💡 Consejo: Si la carta no es lo suficientemente buena, prueba a pegar la oferta completa de nuevo y vuelve a generar la carta. A veces, el modelo necesita más contexto para producir un resultado óptimo.")