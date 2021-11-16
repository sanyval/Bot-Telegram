import logging
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
from matplotlib import pyplot as plt
import sympy

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger=logging.getLogger()
logger.setLevel(logging.INFO)

def start(update,context):
    logger.info('El usuario ha iniciado el bot')
    name=update.message.chat["first_name"]
    update.message.reply_text(f"HOLA {name}, es un gusto tenerte por aca")
    logger.info("Saludo enviado")

def ayuda(update,context):
    logger.info("El usuario solicito ayuda")
    options=[
        [InlineKeyboardButton("Saludo",callback_data="m1")],
        [InlineKeyboardButton("Grafo",callback_data="m2")],
        [InlineKeyboardButton("Secuencia",callback_data="m3")],
        [InlineKeyboardButton("Recibir imagen",callback_data="m4")],
        [InlineKeyboardButton("Recibir documentos",callback_data="m5")],
    ]
    reply_markup=InlineKeyboardMarkup(options)
    update.message.reply_text("Usted solicito ayuda",reply_markup=reply_markup)

def resolverRR(sec):
    n=sympy.symbols('n')
    return 2**(n-1)+sympy.binomial(n,2)

def secuencia(update,context):
    logger.info("El usuario envio una secuencia de numeros")
    text=update.message.text
    text=text.replace("/secuencia","").strip()
    try:
        sec=eval(text)
        f_n=resolverRR(sec)
        lat=""+sympy.latex(f_n)+""
        fn = f"${lat}$"
        latex_img=plt.figure(figsize=[((len(fn) / 2) * 0.15), 1], dpi=200)
        latex_img.text(0.5, 0.5, str(fn), horizontalalignment='center', verticalalignment='center', fontsize='xx-large', wrap=True)
        latex_img.savefig("src/images/solucion_rr.png")
        plt.clf()
        plt.close()
        update.message.reply_text(f_n)
        img=open("src/images/solucion_rr.png","rb")
        chat_id=update.message.chat.id
        update.message.bot.sendPhoto(chat_id=chat_id ,photo=img)
    except Exception as e :
        logger.info("Ocurrio un error al enviar la secuencia")
        update.message.reply_text("Los parametros enviados en la secuencia deben ser numeros")

def grafo(update,context):
    name=update.message.chat.first_name
    logger.info(f"El usuario {name} generar un grafo")
    grafo_info=update.message.text
    grafo_info=grafo_info.replace("/grafo","")
    try:
        valores=eval(grafo_info)
        if len(valores)>3:
            update.message.reply_text("Los parametros superan a los esperados")
        else:
            #[]
            aristas=valores[0]
            vertices=valores[1]
            grado=valores[2]
            update.message.reply_text(f"Sus parametros son:\n\n1\. *Numero de aristas:* {aristas}\n2\. *Numero de vertices:* {vertices}\n3\. *Grado:* {grado} ",parse_mode="MarkdownV2")
            #graph(aristas, vertives, grado)
            img=open("src/images/graph.png","rb")
            chat_id=update.message.chat.id
            update.message.bot.sendPhoto(chat_id=chat_id,photo=img)
    except Exception as e:
        logger.info("Ha ocurrido un error generando un grafo")
        update.message.reply_text("Lo sentimos ha ocurrido un error. Intente de nuevo y revise los paramentros")
        print(e)

def send_doc(query):
    logger.info("El usuario ha solicitado un documento")
    chat_id=query.message.chat.id
    doc=open("src/docs/doc.pdf","rb")
    query.message.reply_text("Cargando documento, por favor espere")
    query.bot.sendDocument(chat_id=chat_id,document=doc,timeout=300)

def send_image(query):
    logger.info("El usuario ha solicitado una imagen")
    chat_id=query.message.chat.id
    img=open("src/images/uninorte.jpg","rb")
    query.message.reply_text("Cargando imagen, por favor espere")
    query.bot.sendPhoto(chat_id=chat_id,photo=img,timeout=120)

def saludo(query):
    name = query.message.chat.first_name
    logger.info(f"El usuario {name} solicito un saludo")
    query.message.reply_text(f"Hola, {name} &#x1F44B . Un gusto tenerte por aca &#x1F601 .",parse_mode="HTML")

def help_grafo(query):
    name=query.message.chat.first_name
    logger.info(f"El usuario {name} solicito ayuda sobre el comando grafo")
    info=f"""
    Bienvenido {name} a continuacion se ve a explicar como generar un grafo y los atributos que se necesitan\.
    
    \- E: Numero de aristas\.
    \- V: Numero de vertices\.
    \-K: Grado maximo del grafo\.
    
    Para correr este comando debes escribir:
    /grafo E,V,K
    
    *Ejemplos*
    1\. /grafo \[1,2,3\]
    2\. /grafo \(1,2,3\)
    3\. /grafo 1,2,3   
    
    """
    query.message.reply_text(info,parse_mode="MarkdownV2")


def help_sec(query):
    name = query.message.chat.first_name
    logger.info(f"El usuario {name} solicito ayuda sobre el comando secuencia")
    info = f"""
    Bienvenido {name} a continuacion se ve a explicar como resolver una relacion de recurrencia y los atributos que se necesitan\.

    \- RR: Coeficientes de la relacion de recurrencia normalizada\.

    Para correr este comando debes escribir:
    /secuencia RR

    *Ejemplos*
    1\. /secuencia \[1,2,3,4,5\]
    2\. /secuencia \(1,2,3\)
    3\. /secuencia 1,2   

    """
    query.message.reply_text(info, parse_mode="MarkdownV2")

def menu_ayuda(update, context):
    query = update.callback_query
    query.answer()
    callback=query.data
    if callback == "m1":
        saludo(query)
    elif callback == "m2":
        help_grafo(query)
    elif callback == "m3":
        help_sec(query)
    elif callback == "m4":
        send_image(query)
    elif callback == "m5":
        send_doc(query)