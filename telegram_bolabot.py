# -*- coding: utf-8 -*-

import telebot
import random
import argparse
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("key", help="AUTH Key do telegram bot")
parser.add_argument("-v", "--verbose", action="store_true", help="Mostra mais informação na tela")
parser.add_argument("-p", "--private_only", action="store_true", help="Considera apenas mensagens enviadas em conversa privada")

args = parser.parse_args()

bot = telebot.TeleBot(args.key)

#Mensagens que começam com alguma dessas strings serão consideradas comandos
command_strings = '!', '/', '.'

updating = False #Flag pra quando for updatear
admins = "Ystah", "Lzimann" #Temporario, será substuido por config.ini depois
def print_verbose(string):
	if args.verbose:
		print string
		
def obv(msg):
    if random.randint(1,4) == 1:
        msg += ', obviamente'
    return msg + '.'
		
@bot.message_handler(content_types=['text'])
def handle_messages(message):
	global updating
	
	#Pra não ficar floodando o canal enquanto estivermos testando
	if (message.chat.type != "private") and args.private_only:
		return

	print_verbose("%s: %s" % (message.from_user.username, message.text))
	command = None
	texto = message.text
	for string in command_strings:
		if message.text.startswith(string):
			command = message.text[len(string):].split()[0]
			texto = ' '.join(message.text.split()[1:])
			break
			
	print_verbose("CMD: %s: %s\n" % (command, texto))
	
	if command == "alt":
		if ':' not in texto:
			msg = texto.strip('?')
		else:
			msg = texto.split(':')[-1].strip().strip('?')
		alternativas = msg.split(' ou ')
		if len(alternativas) > 1:
			bot.send_message(message.chat.id, obv(random.choice(alternativas).capitalize()))
	
	if command == "bola" or texto.startswith('@' + bot.get_me().username):
		bot.send_message(message.chat.id, obv(random.choice(("Sim", "Não"))))
	
	if command == "update" and message.from_user.username in admins:
		bot.send_message(message.chat.id, "Fazendo update!")
		subprocess.call("git pull origin master", shell = True)
		updating = True
		bot.stop_polling()

bot.skip_pending = True

print_verbose("Iniciando: %s" % sys.argv)
bot.polling()

if updating:
	print_verbose("Atualizando...")
	subprocess.Popen(["python"] + sys.argv)
