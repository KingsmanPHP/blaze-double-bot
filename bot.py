import requests
import json
import telebot
import time


api = "5676361702:AAH6B7WZ8DAn3H36cFmo8Z-1yOUqq4LAUP8"
chat_id = "-1001909066800"

bot = telebot.TeleBot(api)
    
analise_sinal = False
entrada = 0
max_gale = 2 ##quantia de gale
sinal_enviado = False
resultado = []
check_resultado = []

## win / loss

def ler_win():
    try:
        with open("win.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0
def salvar_win(win):
    with open("win.txt", "w") as f:
        f.write(str(win))
def adicionar_win():
    win = ler_win()
    win += 1
    salvar_win(win)
##loss
def ler_loss():
    try:
        with open("loss.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0
def salvar_loss(loss):
    with open("loss.txt", "w") as f:
        f.write(str(loss))
def adicionar_loss():
    loss = ler_loss()
    loss += 1
    salvar_loss(loss)
## enviar mensagem das win / loss

def msg_win_los():
    total_win = ler_win()
    total_loss = ler_loss()
    total = total_win + total_loss

    if total > 0:
        percent_win = (total_win / total) * 100
        percent_loss = (total_loss / total) * 100
    else:
        percent_win = 0
        percent_loss = 0
    text = f"""<b>✅ (<code>{total_win}</code>) ⛔️ (<code>{total_loss}</code>) 👻 (<code>{percent_win:.2f}%</code>) de Acertividade.</b>"""
    bot.send_message(chat_id, text=text, parse_mode="HTML")


def reset():
    global analise_sinal
    global entrada
    global sinal_enviado
    
    entrada = 0
    analise_sinal = False
    sinal_enviado = False
    return


def martingale():
    global entrada
    entrada += 1
    
    if entrada <= max_gale:
        bot.send_message(chat_id, text=f"<b>Gale {entrada}</b>", parse_mode="HTML")
    else:
        loss()
        reset()
    return

# msg_win_los()                    

def api():
    global resultado
    req = requests.get('https://blaze.com/api/roulette_games/recent')
    a = json.loads(req.content)
    jogo = [x['roll'] for x in a]
    resultado = jogo
    return jogo

def win():
    adicionar_win()
    msg_win_los()                    
    bot.send_sticker(chat_id, sticker="CAACAgEAAxkBAAEhdjZkarLjU7dh00rw1dKg1o0PeFg3MQACjgIAAoPJiUUrsFkyTUav6S8E")      
    return 
def win_white():
    adicionar_win()
    msg_win_los()                    
    bot.send_sticker(chat_id, sticker="CAACAgEAAxkBAAEhdoVkar7sQWgQht1jLxUq-Il2Kvcn7wAC_AEAAra7kUUTPIl8kN0Shy8E")
    return
def loss():
    adicionar_loss()
    msg_win_los()                                            
    bot.send_sticker(chat_id, sticker="CAACAgEAAxkBAAEhdjhkarMywUoYX3lvHaWlcFCCeO6ChgACHgIAAlrJiEV5qikLWrbyqS8E")  
    return
 

def correcao(results, color):
    if results[0:1] == ['P'] and color == '⚫️':
        win()
        reset()
        return
    
    elif results[0:1] == ['V'] and color == '🔴':
        win()
        reset()
        return
    
    elif results[0:1] == ['P'] and color == '🔴':
        martingale()
        return
    
    elif results[0:1] == ['V'] and color == '⚫️':
        martingale()
        return
    
    
    elif results[0:1] == ['B']:
        win_white()
        reset()

def enviar_sinal(cor, padrao):         
    text = f"""
✅𝗘𝗻𝘁𝗿𝗮𝗿 𝗡𝗼:✅ ➡️ {cor}➕⚪️
👻𝗣𝗮𝗱𝗿𝗮𝗼: {padrao}
    """ 
    bot.send_message(chat_id, text=text)
    return


def estrategy(resultado):
    global analise_sinal
    global cor_sinal
    global cores
    global sinal_enviado

    
    cores = []
    for x in resultado:
        if x >= 1 and x <= 7:
            color = 'V'
            cores.append(color)
        elif x >= 8 and x <= 14:
            color = 'P'
            cores.append(color)
        else:
            color = 'B'
            cores.append(color)
    print(cores)
    global sinal_enviado

    
    if analise_sinal == True:
        correcao(cores, cor_sinal)
    else:
        if cores[0:6] == ['V','V','V','V','P','V'] and not sinal_enviado:
            cor_sinal = '⚫️'
            padrao = '🔴🔴🔴🔴⚫🔴'
            enviar_sinal(cor_sinal, padrao)
            analise_sinal = True
            print('sinal enviado')
            sinal_enviado = True

        if cores[0:6] == ['P','V','P','P','V','V'] and not sinal_enviado:
            cor_sinal = '⚫️'
            padrao = '⚫🔴⚫⚫🔴🔴'
            enviar_sinal(cor_sinal, padrao)
            analise_sinal = True
            print('sinal enviado')
            sinal_enviado = True

        if cores[0:4] == ['P','V','P','V'] and not sinal_enviado:
            cor_sinal = '🔴'
            padrao = '⚫🔴⚫🔴'
            enviar_sinal(cor_sinal, padrao)
            analise_sinal = True
            print('sinal enviado')
            sinal_enviado = True

        if cores[0:3] == ['V','P','V'] and not sinal_enviado:
            cor_sinal = '⚫️'
            padrao = '🔴⚫🔴'
            enviar_sinal(cor_sinal, padrao)
            analise_sinal = True
            print('sinal enviado')
            sinal_enviado = True

        if cores[0:2] == ['V','P'] and not sinal_enviado:
            cor_sinal = '⚫️'
            padrao = '🔴⚫'
            enviar_sinal(cor_sinal, padrao)
            analise_sinal = True
            print('sinal enviado')
            sinal_enviado = True


while True:
    api()
    if resultado != check_resultado:
        check_resultado = resultado
        #print(resultado)
        estrategy(resultado)