import asyncio
import os
import datetime
import json
from telethon import TelegramClient, events

CONFIG_FILE = "config.json"

def carregar_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
            if "filtro" not in cfg: cfg["filtro"] = "tudo"
            if "alvo" not in cfg and "bot_alvo" in cfg: cfg["alvo"] = cfg["bot_alvo"]
            return cfg
    return {
        "api_id": 35358927, 
        "api_hash": "2d06935658e2ddfd3eeeef71fb60117e",
        "alvo": "@VAZOUMC_BOT",
        "download_dir": "/sdcard/Download/previas_extraidas",
        "filtro": "tudo"
    }

def salvar_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)

config = carregar_config()
os.makedirs(config["download_dir"], exist_ok=True)

client = TelegramClient('sessao_extrator', config["api_id"], config["api_hash"])

async def processar_mensagem(msg, sender_name="Desconhecido", chat_name="Chat"):
    if not msg: return

    tem_texto = bool(msg.text)
    tem_midia = bool(msg.video or msg.photo or msg.document)
    
    if config["filtro"] == "midia" and not tem_midia: return 
    if config["filtro"] == "texto" and not tem_texto: return 
    if not tem_texto and not tem_midia: return 

    data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_texto = f"\n========================================\nDATA: {data_hora}\nCHAT: {chat_name}\nREMETENTE: {sender_name}\n----------------------------------------\n"
    print("\n" + "="*45)
    print(f"[CHAT]: {chat_name} | [DE]: {sender_name}")
    
    if tem_texto:
        print(f"[TEXTO]:\n{msg.text}")
        log_texto += f"[TEXTO]:\n{msg.text}\n"
    
    if msg.buttons:
        print("\n[BOTÕES]:")
        log_texto += "\n[BOTÕES]:\n"
        for row in msg.buttons:
            for btn in row:
                print(f"  -> [ {btn.text} ]")
                log_texto += f"  -> [ {btn.text} ]\n"
                
    if tem_midia:
        print(f"\n[MÍDIA] Baixando arquivo...")
        try:
            nome_base = f"{msg.id}"
            caminho = await msg.download_media(file=os.path.join(config["download_dir"], nome_base))
            if caminho:
                nome_arquivo = os.path.basename(caminho)
                print(f"[SALVO] {caminho}")
                log_texto += f"\n[MÍDIA SALVA]: {nome_arquivo}\n"
        except Exception as e:
            print(f"[ERRO] Falha ao baixar: {e}")
            log_texto += f"\n[ERRO DE DOWNLOAD]: {e}\n"

    try:
        log_path = os.path.join(config["download_dir"], "historico_extraido.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(log_texto)
    except Exception:
        pass

@client.on(events.NewMessage)
async def handler(event):
    chat = await event.get_chat()
    chat_username = getattr(chat, 'username', '')
    alvo_limpo = config["alvo"].replace('@', '').lower()
    
    if (chat_username and chat_username.lower() == alvo_limpo) or (str(chat.id) == alvo_limpo):
        sender = await event.get_sender()
        sender_name = getattr(sender, 'first_name', None) or getattr(sender, 'username', 'Bot')
        chat_name = getattr(chat, 'title', getattr(chat, 'first_name', 'Bot'))
        await processar_mensagem(event.message, sender_name, chat_name)

def mostrar_banner():
    verde = "\033[0;32m"
    reset = "\033[0m"

    print(f"{verde}┌──────────────────────────────────────────────────────────────────┐{reset}")
    print(f"{verde} ███████╗██╗  ██╗████████╗██████╗  █████╗  ██████╗████████╗ ██████╗ ██████╗ {reset}")
    print(f"{verde}  ██╔════╝╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗{reset}")
    print(f"{verde}  █████╗   ╚███╔╝    ██║   ██████╔╝███████║██║        ██║   ██║   ██║██████╔╝{reset}")
    print(f"{verde}  ██╔══╝   ██╔██╗    ██║   ██╔══██╗██╔══██║██║        ██║   ██║   ██║██╔══██╗{reset}")
    print(f"{verde}  ███████╗██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗   ██║   ╚██████╔╝██║  ██║{reset}")
    print(f"{verde}  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝{reset}")
    print(f"{verde}└──────────────────────────────────────────────────────────────────┘{reset}")
    print(f"{verde}               [ SYSTEM PRO V7 ] :: Criado por @zetx.py{reset}\n")

async def painel():
    while True:
        os.system('clear')
        mostrar_banner()
        
        filtro_atual = config['filtro'].upper()
        
        print("\033[0;32m--------------------------------------------------------------------\033[0m")
        print(" \033[0;32m[1]\033[0m 📱 Trocar Bot/Grupo Alvo")
        print(" \033[0;32m[2]\033[0m 📂 Alterar Pasta de Salvamento")
        print(" \033[0;32m[3]\033[0m 🔑 Alterar API (ID e Hash)")
        print(f" \033[0;32m[4]\033[0m ⚙️  Filtro de Extração: \033[1;33m[{filtro_atual}]\033[0m")
        print(" \033[0;32m[5]\033[0m 🎯 Extrair Histórico do Alvo Atual")
        print(" \033[0;32m[6]\033[0m 🌐 Extrair de TODOS os Grupos/Canais")
        print(" \033[0;32m[7]\033[0m 📋 Listar IDs dos Meus Grupos/Canais")
        print(" \033[0;32m[8]\033[0m ❌ Sair")
        print("\033[0;32m--------------------------------------------------------------------\033[0m")
        
        try:
            opcao = await asyncio.to_thread(input, " \033[0;32mEscolha uma opção:\033[0m ")
        except EOFError:
            break
            
        if opcao == '1':
            os.system('clear')
            mostrar_banner()
            print("\033[1;33mDica: Cole o @username ou o ID do grupo (ex: -100123456789)\033[0m")
            novo_alvo = await asyncio.to_thread(input, " Digite o alvo: ")
            if novo_alvo:
                if not novo_alvo.startswith('@') and not novo_alvo.startswith('http') and not novo_alvo.startswith('-'): 
                    novo_alvo = '@' + novo_alvo
                config["alvo"] = novo_alvo
                salvar_config(config)
                print(f"\n\033[0;32m[!] Alvo alterado com sucesso.\033[0m")
                await asyncio.sleep(1.5)

        elif opcao == '2':
            os.system('clear')
            mostrar_banner()
            novo_dir = await asyncio.to_thread(input, " Novo caminho completo: ")
            if novo_dir:
                try:
                    os.makedirs(novo_dir, exist_ok=True)
                    config["download_dir"] = novo_dir
                    salvar_config(config)
                    print(f"\n\033[0;32m[!] Diretório alterado com sucesso.\033[0m")
                except Exception as e:
                    print(f"\n\033[1;31m[ERRO] Caminho inválido: {e}\033[0m")
                await asyncio.sleep(2)

        elif opcao == '3':
            os.system('clear')
            mostrar_banner()
            novo_id = await asyncio.to_thread(input, " Digite o novo API_ID: ")
            novo_hash = await asyncio.to_thread(input, " Digite o novo API_HASH: ")
            if novo_id and novo_hash:
                try:
                    config["api_id"] = int(novo_id)
                    config["api_hash"] = novo_hash.strip()
                    salvar_config(config)
                    print("\n\033[0;32m[!] API salva com sucesso! O script será fechado.\033[0m")
                    await asyncio.sleep(3)
                    return 
                except ValueError:
                    print("\n\033[1;31m[ERRO] O API_ID precisa ser um número.\033[0m")
                    await asyncio.sleep(2)

        elif opcao == '4':
            os.system('clear')
            mostrar_banner()
            print("\033[0;32m--- CONFIGURAR FILTRO DE DOWNLOAD ---\033[0m")
            print(" [1] Tudo (Textos, Fotos e Vídeos)")
            print(" [2] Apenas Mídias (Fotos e Vídeos)")
            print(" [3] Apenas Textos\n")
            
            escolha_filtro = await asyncio.to_thread(input, " Escolha o filtro: ")
            if escolha_filtro == '1': config["filtro"] = "tudo"
            elif escolha_filtro == '2': config["filtro"] = "midia"
            elif escolha_filtro == '3': config["filtro"] = "texto"
            
            salvar_config(config)
            print(f"\n\033[0;32m[!] Filtro alterado para: {config['filtro'].upper()}\033[0m")
            await asyncio.sleep(1.5)

        elif opcao == '5':
            os.system('clear')
            mostrar_banner()
            try: os.makedirs(config["download_dir"], exist_ok=True)
            except: pass

            print(f"\n\033[0;32m[!] Conectando ao alvo {config['alvo']}...\033[0m")
            try:
                entidade = await client.get_entity(config["alvo"])
                print("\033[1;33m[AGUARDE] Puxando histórico (200 msgs)...\033[0m")
                
                async for msg in client.iter_messages(entidade, limit=200):
                    sender = await msg.get_sender()
                    sender_name = getattr(sender, 'first_name', None) or getattr(sender, 'username', 'Bot')
                    chat_name = getattr(entidade, 'title', getattr(entidade, 'first_name', 'Bot'))
                    await processar_mensagem(msg, sender_name, chat_name)
                
                print("\n\033[0;32m[✓] Histórico baixado!\033[0m")
                print(" \033[1;34m[!] Escutando em tempo real... (Ctrl+C para parar)\033[0m\n")
                
                if getattr(entidade, 'bot', False):
                    await client.send_message(config["alvo"], '/start')
                    
                while True: await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n\033[0;32m[!] Captura pausada. Voltando...\033[0m")
                await asyncio.sleep(1.5)
            except Exception as e:
                print(f"\n\033[1;31m[ERRO] Falha ao acessar: {e}\033[0m")
                await asyncio.sleep(4)

        elif opcao == '6':
            os.system('clear')
            mostrar_banner()
            print("\n\033[1;33m[!] Iniciando varredura em TODOS os grupos e canais...\033[0m")
            print(" Isso pode demorar. Pressione Ctrl+C para abortar.\n")
            
            try:
                async for dialog in client.iter_dialogs():
                    if dialog.is_group or dialog.is_channel:
                        print(f"\n\033[0;36m>>> Entrando no chat: {dialog.name}\033[0m")
                        async for msg in client.iter_messages(dialog.id, limit=20):
                            sender = await msg.get_sender()
                            sender_name = getattr(sender, 'first_name', None) or getattr(sender, 'username', 'Desconhecido')
                            await processar_mensagem(msg, sender_name, dialog.name)
                        await asyncio.sleep(2) # Pausa anti-ban
                print("\n\033[0;32m[✓] Varredura concluída!\033[0m")
                await asyncio.to_thread(input, "\n Pressione Enter para voltar...")
            except KeyboardInterrupt:
                print("\n\033[1;33m[!] Cancelado.\033[0m")
                await asyncio.sleep(2)
            except Exception as e:
                print(f"\n\033[1;31m[ERRO] Falha: {e}\033[0m")
                await asyncio.sleep(4)

        elif opcao == '7':
            os.system('clear')
            mostrar_banner()
            print("\n\033[1;33m[!] Buscando seus grupos e canais...\033[0m\n")
            try:
                count = 0
                async for dialog in client.iter_dialogs():
                    if dialog.is_group or dialog.is_channel:
                        count += 1
                        # Pega o link ou o username (se existir)
                        username = getattr(dialog.entity, 'username', None)
                        user_str = f"@{username}" if username else "Privado/Sem @"
                        
                        print(f"\033[1;36mNome:\033[0m {dialog.name}")
                        print(f"\033[0m  ID: \033[1;32m{dialog.id}\033[0m")
                        print(f"\033[0m  User: {user_str}")
                        print("\033[1;30m-----------------------------------\033[0m")
                
                print(f"\n Total: {count} grupos/canais encontrados.")
                print("\033[1;33m[!] Copie o ID (número) ou o @ e use na opção [1].\033[0m")
                await asyncio.to_thread(input, "\n Pressione Enter para voltar...")
            except Exception as e:
                print(f"\n\033[1;31m[ERRO] Falha ao listar: {e}\033[0m")
                await asyncio.sleep(3)

        elif opcao == '8':
            print("\n[!] Desconectando e saindo...")
            await client.disconnect()
            break

async def main():
    print(" Autenticando no Telegram...")
    try:
        await client.start()
    except Exception as e:
        print(f"\033[1;31m[ERRO] Falha ao conectar: {e}\033[0m")
        return
    
    await asyncio.sleep(1)
    await painel()

with client:
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n[!] Fechando script.")
