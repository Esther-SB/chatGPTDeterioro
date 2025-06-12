from flask import Flask, render_template, request
import random
import time
import pyttsx3
import threading
import serial
import serial.tools.list_ports

app = Flask(__name__)

# Diccionario de respuestas
respuestas = {
    "clima": "El cambio climático es la alteración a largo plazo del clima de la Tierra, especialmente en temperaturas, lluvias, vientos y fenómenos extremos.",
    "einstein": "Albert Einstein fue un físico teórico alemán, considerado uno de los científicos más importantes y conocidos de la historia.",
    "arduino": "Arduino es una plataforma de electrónica abierta que permite crear proyectos interactivos de forma fácil, combinando hardware (placas electrónicas) y software (un programa para escribir y cargar código).",
    "cielo": "El color del cielo suele ser azul durante el día, debido a un fenómeno llamado dispersión de Rayleigh: las moléculas del aire dispersan la luz solar, y el azul es el color que más se dispersa en la atmósfera.",
    "china": "La Gran Muralla China mide aproximadamente 21,196 kilómetros de largo, según estudios realizados por la Administración Estatal del Patrimonio Cultural de China en 2012.",
    "hormigas": "No, una persona no puede sobrevivir solo comiendo hormigas y sin agua. A corto plazo puede resistir unos días, pero sufrirá deshidratación severa y desnutrición.",
    "sanidad": "Las largas esperas se deben a la alta demanda de pacientes y servicios, falta de personal sanitario, recortes presupuestarios, gestión ineficiente y desigualdad geográfica.",
    "tusi": "El tusi es una droga sintética y peligrosa, que mezcla varias sustancias psicoactivas. Su consumo es muy riesgoso porque no se controla qué contiene ni cómo afecta.",
    "sudar": "Sí, puedes sudar bajo el agua, pero no lo notas ni te enfría como en el aire, porque el sudor se mezcla con el agua enseguida.",
    "caballos": "Los caballos duermen de pie para descansar ligeramente, pero necesitan acostarse un rato cada día para un sueño profundo y reparador.",
    "trabajo": "Monje. Tenías comida, techo, acceso a libros y educación. Además no ibas a la guerra ni trabajabas en el campo. Muchos monjes eran los intelectuales de su época.",
    "amor": "El amor es una fuerza emocional profunda que nos conecta con otros, da sentido a nuestras relaciones y muchas veces, a la vida misma.",
    "chiste": "¿Cuál es el colmo de un preso?........................................¡Tener libertad de expresión!",
    "youtube": "NO VAS A CREER QUIÉN TE INVITA A UN CAFÉ, ¡QUÉDATE HASTA EL FINAL!” “¡Hola, qué tal, bienvenidos al canal! Hoy te traigo algo diferente...YouTube quiere invitarte a un café , pero antes… ¡dale like, suscríbete y activa la campanita!",
    "opinion": "Tu opinión es como una pestaña en el ojo: molesta, inesperada y completamente innecesaria.",
    "insultame": "Vuestra presencia es como la peste: nadie la desea, todos la notan, y pocos sobreviven ilesos.",
    "relaciones": "Las relaciones personales influyen profundamente en nuestra salud emocional y mental.",
    "amistad": "La amistad verdadera implica apoyo mutuo, confianza y momentos compartidos.",
    "familia": "La familia es un núcleo fundamental para el desarrollo emocional y social.",
    "educación": "La educación es la base del progreso individual y colectivo.",
    "dinero fácil": "No existen métodos garantizados para conseguir dinero fácil; cuidado con estafas.",
    "criptomonedas": "Las criptomonedas son monedas digitales que usan criptografía para transacciones seguras.",
    "bitcoin": "Bitcoin es una criptomoneda descentralizada creada en 2009 como alternativa al dinero tradicional.",
    "blockchain": "Blockchain es una tecnología de registro descentralizado que da soporte a criptomonedas y contratos inteligentes.",
    "cómo ahorrar": "Ahorrar requiere disciplina financiera y metas claras de corto y largo plazo.",
    "finanzas personales": "Llevar un control de ingresos, gastos y ahorro es clave para unas finanzas saludables.",
    "invertir": "Invertir sabiamente ayuda a crecer tu dinero, pero requiere información y gestión del riesgo.",
    "bienes raíces": "Invertir en bienes raíces puede ser una opción estable y rentable a largo plazo.",
    "mentalidad positiva": "Cultivar una mentalidad positiva influye en tu bienestar y en cómo enfrentas los desafíos.",
    "resiliencia": "La resiliencia es la capacidad de adaptarse y recuperarse frente a la adversidad.",
    "inteligencia emocional": "Es la habilidad de reconocer y gestionar tus emociones y las de los demás.",
    "liderazgo": "El liderazgo efectivo inspira, guía y potencia a otros hacia objetivos comunes.",
    "emprendimiento": "Emprender implica crear un proyecto propio, con riesgos y recompensas significativos.",
    "negocios online": "Los negocios online permiten generar ingresos usando plataformas digitales.",
    "freelance": "Ser freelance es trabajar de forma autónoma ofreciendo tus servicios a distintos clientes.",
    "marketing digital": "El marketing digital abarca estrategias para promocionar productos online.",
    "instagram": "Instagram es una red social para compartir fotos y videos, también usada para marketing.",
    "tiktok": "TikTok es una plataforma de videos cortos popular entre jóvenes y creadores de contenido.",
    "youtube ingresos": "YouTube permite monetizar videos mediante publicidad, membresías y patrocinios.",
    "cómo tener éxito": "El éxito requiere constancia, enfoque, adaptación y aprender de los errores.",
    "cómo superar una ruptura": "Aceptar, expresarse y enfocarse en uno mismo es clave para superar una ruptura.",
    "motivación": "La motivación impulsa la acción hacia objetivos personales o profesionales.",
    "dejar de procrastinar": "Superar la procrastinación requiere hábitos, planificación y reducir distracciones.",
    "propósito de vida": "Descubrir tu propósito da dirección, motivación y sentido a tu vida.",
    "salud mental": "La salud mental es tan importante como la física y requiere cuidado constante.",
    "medicina natural": "La medicina natural se basa en remedios de origen vegetal o tradicional.",
    "hábitos saludables": "Dormir bien, moverse, comer equilibrado y tener relaciones sanas son hábitos clave.",
    "mindfulness": "El mindfulness es atención plena en el presente, útil para reducir el estrés.",
    "rutina diaria": "Una rutina diaria da estructura, eficiencia y mejora tu bienestar general.",
    "organización": "La organización personal aumenta la productividad y reduce el estrés.",
    "cómo ser inteligente": "La inteligencia se puede desarrollar con lectura, reflexión y aprendizaje continuo.",
    "lectura rápida": "Técnicas como escaneo visual y eliminación de subvocalización pueden mejorar tu lectura.",
    "cómo estudiar": "Estudiar eficazmente implica repasar, usar mapas mentales y practicar activamente.",
    "idiomas": "Aprender idiomas mejora tu memoria, oportunidades laborales y comprensión cultural.",
    "viajar barato": "Viajar barato es posible con planificación, flexibilidad y herramientas digitales.",
    "apps útiles": "Existen apps para organización, finanzas, salud, aprendizaje y productividad.",
    "cocina fácil": "La cocina fácil se basa en ingredientes simples y pasos accesibles para todos.",
    "vida saludable": "Una vida saludable combina cuerpo activo, mente tranquila y relaciones positivas.",
    "cómo dormir mejor": "Dormir mejor requiere higiene del sueño, rutina fija y reducir pantallas antes de acostarse.",
    "ansiedad social": "La ansiedad social es común y tratable con terapia, práctica y autoaceptación.",
    "superación personal": "El desarrollo personal implica esfuerzo consciente por mejorar tu vida y tu entorno.",
    "libros recomendados": "Leer libros de desarrollo, novelas o ciencia puede transformar tu perspectiva.",
    "documentales": "Los documentales ofrecen aprendizaje visual y profundo sobre temas variados.",
    "cómo ser creativo": "La creatividad se nutre de curiosidad, experimentación y conexiones nuevas.",
    "apps para aprender": "Plataformas como Duolingo, Khan Academy y Coursera hacen el aprendizaje accesible.",
    "salud emocional": "La salud emocional es tu capacidad para gestionar tus sentimientos de forma equilibrada.",
    "productividad": "Ser productivo es lograr más con menos, usando tiempo y energía eficientemente.",
    "felicidad": "La felicidad es un estado emocional positivo que surge al sentir satisfacción, bienestar o realización personal.",
    "estrés": "El estrés es una respuesta del cuerpo ante situaciones percibidas como amenazantes o desafiantes, y puede ser físico o emocional.",
    "ejercicio": "Hacer ejercicio regularmente mejora la salud física, mental y emocional, además de aumentar la energía.",
    "naturaleza": "Estar en contacto con la naturaleza puede reducir el estrés, mejorar el estado de ánimo y promover la salud general.",
    "meditación": "La meditación es una práctica que entrena la mente para enfocarse, reducir el estrés y aumentar la claridad mental.",
    "alimentación": "Una alimentación equilibrada proporciona los nutrientes necesarios para un buen funcionamiento del cuerpo y la mente.",
    "respeto": "El respeto es reconocer el valor de otras personas, sus ideas, decisiones y límites.",
    "honestidad": "La honestidad implica decir la verdad, actuar con integridad y ser coherente con los valores personales.",
    "valentía": "La valentía es actuar con determinación ante el miedo, el riesgo o la incertidumbre.",
    "empatía": "La empatía es la capacidad de ponerse en el lugar del otro y comprender sus emociones y perspectivas.",
    "paciencia": "La paciencia es la capacidad de mantener la calma y perseverar ante dificultades o demoras.",
    "humildad": "La humildad consiste en reconocer nuestras limitaciones y valorar a los demás sin arrogancia.",
    "confianza": "La confianza se construye con el tiempo mediante acciones coherentes, honestas y respetuosas.",
    "autoestima": "Tener buena autoestima es valorarse a uno mismo, aceptar virtudes y defectos con realismo.",
    "rutina": "Tener una rutina diaria ayuda a estructurar el tiempo, mantener hábitos y reducir la ansiedad.",
    "soledad": "La soledad puede ser una oportunidad para el autoconocimiento o una experiencia difícil si es no deseada.",
    "esperanza": "La esperanza es la creencia de que las cosas pueden mejorar, incluso en tiempos difíciles.",
    "sabiduría": "La sabiduría va más allá del conocimiento; implica saber aplicar lo aprendido con juicio y compasión.",
    "gratitud": "Practicar la gratitud mejora el estado de ánimo, fortalece las relaciones y reduce el estrés.",
    "perdón": "Perdonar no siempre es olvidar, pero sí liberar el rencor para sanar emocionalmente.",
    "historia": "La historia estudia los acontecimientos pasados de la humanidad para entender el presente y proyectar el futuro.",
    "geografia" : "La geografía analiza las características físicas de la Tierra y cómo los humanos interactúan con su entorno.",
"agua" :"El agua es un recurso natural esencial para la vida, presente en ríos, mares, lagos y atmósfera.",
"montaña": "Una montaña es una elevación natural del terreno que suele superar los 600 metros de altura respecto a su base.",
"respiración" : "La respiración es el proceso biológico mediante el cual los seres vivos obtienen oxígeno y liberan dióxido de carbono.",
"democracia" : "La democracia es un sistema político en el que el poder reside en el pueblo, que lo ejerce mediante el voto.",
"planeta" : "Un planeta es un cuerpo celeste que gira alrededor de una estrella y no emite luz propia.",
"bosque" : "Un bosque es un ecosistema con alta densidad de árboles, esencial para la biodiversidad y el clima.",
"energía" : "La energía es la capacidad de realizar un trabajo o producir un cambio, y existe en diversas formas como térmica, eléctrica y solar.",
"célula" : "La célula es la unidad básica de la vida, que constituye todos los seres vivos y realiza funciones vitales.",


    

}

#
contador = 0
ultimo_tiempo = time.time()
nivel = 0.0
TIEMPO_LIMITE = 20  # segundos sin preguntas para iniciar descenso

# 🔍 Función para detectar Arduino automáticamente
def detectar_arduino():
    print("Buscando puertos serie...")
    puertos = serial.tools.list_ports.comports()
    for puerto in puertos:
        print(f"- {puerto.device}: {puerto.description}")
        if "Arduino" in puerto.description or "CH340" in puerto.description or "USB" in puerto.description:
            try:
                arduino = serial.Serial(puerto.device, 9600, timeout=1)
                time.sleep(2)
                print(f"✅ Arduino detectado en {puerto.device}")
                return arduino
            except Exception as e:
                print(f"⚠️ No se pudo abrir {puerto.device}: {e}")
    print("❌ No se detectó ningún Arduino.")
    return None

arduino = detectar_arduino()

# 🔊 Enviar nivel de intensidad al buzzer (PWM)
def enviar_a_arduino(nivel_actual):
    if arduino and arduino.is_open:
        intensidad = int(nivel_actual * 255)
        intensidad = max(0, min(intensidad, 255))
        try:
            arduino.write(bytes([intensidad]))
            print(f"🎵 Buzzer -> nivel {nivel_actual:.2f}, intensidad {intensidad}")
        except Exception as e:
            print("⚠️ Error al enviar al Arduino:", e)

# 🧠 Deteriorar texto según el nivel
def deteriorar(texto, nivel):
    return ' '.join([
        palabra[::-1] + random.choice(["@", "#", "*", "~"]) if random.random() < nivel else palabra
        for palabra in texto.split()
    ])

# ⏬ Hilo que baja el nivel si no se pregunta
def decrementar_nivel():
    global nivel
    while True:
        time.sleep(1)
        ahora = time.time()
        if ahora - ultimo_tiempo > TIEMPO_LIMITE:
            if nivel > 0:
                nivel = max(0, nivel - 0.05)
                enviar_a_arduino(nivel)

threading.Thread(target=decrementar_nivel, daemon=True).start()

@app.route("/", methods=["GET", "POST"])
def index():
    global contador, ultimo_tiempo, nivel

    respuesta_final = ""
    ahora = time.time()

    if request.method == "POST":
        pregunta = request.form["pregunta"].lower().strip()
        base = "No tengo una respuesta para eso."

        for clave in respuestas:
            if clave in pregunta:
                base = respuestas[clave]
                break

        contador += 1
        ultimo_tiempo = ahora
        nivel = min(contador * 0.1, 1.0)  # Sube máximo a 100%
        enviar_a_arduino(nivel)

        respuesta_final = deteriorar(base, nivel)

        def hablar(texto):
            motor = pyttsx3.init()
            motor.setProperty('rate', 150)
            motor.say(texto)
            motor.runAndWait()

        threading.Thread(target=hablar, args=(respuesta_final,)).start()

    return render_template("index.html", respuesta=respuesta_final, nivel=int(nivel * 100))

if __name__ == "__main__":
    app.run(debug=True)

    
try:
    # Abrir el puerto COM3 a 9600 baudios (ajusta si usas otro puerto o velocidad)
    ser = serial.Serial('COM4', 9600, timeout=1)
    print("Puerto abierto")

    # Aquí haces la comunicación con el Arduino
    ser.write(b'Hola Arduino\n')  # ejemplo de envío
    time.sleep(1)
    respuesta = ser.readline()
    print("Respuesta:", respuesta)

finally:
    # Esto siempre se ejecuta: cierra el puerto para liberar el recurso
    if ser.is_open:
        ser.close()
        print("Puerto cerrado")