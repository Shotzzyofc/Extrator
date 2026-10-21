import asyncio
import os
import datetime
import json
from telethon import TelegramClient, events

CONFIG_FILE = "config.json"

def carregar_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "api_id": 35358927, 
        "api_hash": "2d06935658e2ddfd3eeeef71fb60117e",
        "bot_alvo": "@VAZOUMC_BOT",
        "download_dir": "/sdcard/Download/previas_extraidas"
    }

def salvar_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)

config = carregar_config()
os.makedirs(config["download_dir"], exist_ok=True)

client = TelegramClient('sessao_extrator', config["api_id"], config["api_hash"])

@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    sender_user = getattr(sender, 'username', '')
    
    if not sender_user or sender_user.lower() != config["bot_alvo"].replace('@', '').lower():
        return

    msg = event.message
    data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    log_texto = f"\n========================================\nDATA: {data_hora}\n----------------------------------------\n"
    print("\n" + "="*45)
    
    if msg.text:
        print(f"[TEXTO]:\n{msg.text}")
        log_texto += f"[TEXTO]:\n{msg.text}\n"
    
    if msg.buttons:
        print("\n[BOTÕES]:")
        log_texto += "\n[BOTÕES]:\n"
        for row in msg.buttons:
            for btn in row:
                print(f"  -> [ {btn.text} ]")
                log_texto += f"  -> [ {btn.text} ]\n"
                
    if msg.media:
        if msg.video or msg.photo or msg.document:
            print(f"\n[MÍDIA] Baixando arquivo...")
            try:
                caminho = await msg.download_media(file=config["download_dir"])
                nome_arquivo = os.path.basename(caminho)
                print(f"[SALVO] {caminho}")
                log_texto += f"\n[MÍDIA SALVA]: {nome_arquivo}\n"
            except Exception as e:
                print(f"[ERRO] Falha ao baixar: {e}")
                log_texto += f"\n[ERRO DE DOWNLOAD]: {e}\n"

    try:
        log_path = os.path.join(config["download_dir"], "historico_funil.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(log_texto)
    except Exception as e:
        pass

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
    print(f"{verde}               [ SYSTEM PRO V4 ] :: Criado por @zetx.py{reset}\n")

async def painel():
    while True:
        os.system('clear')
        mostrar_banner()
        
        print("\033[0;32m--------------------------------------------------------------------\033[0m")
        print(" \033[0;32m[1]\033[0m 📱 Trocar Bot Alvo")
        print(" \033[0;32m[2]\033[0m 📂 Alterar Pasta de Salvamento")
        print(" \033[0;32m[3]\033[0m 🔑 Alterar API (ID e Hash)")
        print(" \033[0;32m[4]\033[0m 🎯 Iniciar Captura (Ouvir o bot)")
        print(" \033[0;32m[5]\033[0m ❌ Sair")
        print("\033[0;32m--------------------------------------------------------------------\033[0m")
        
        try:
            opcao = await asyncio.to_thread(input, " \033[0;32mEscolha uma opção:\033[0m ")
        except EOFError:
            break
            
        if opcao == '1':
            os.system('clear')
            mostrar_banner()
            novo_bot = await asyncio.to_thread(input, " Digite o @ do novo bot: ")
            if novo_bot:
                if not novo_bot.startswith('@'): novo_bot = '@' + novo_bot
                config["bot_alvo"] = novo_bot
                salvar_config(config)
                print(f"\n\033[0;32m[!] Alvo alterado com sucesso.\033[0m")
                await asyncio.sleep(1.5)

        elif opcao == '2':
            os.system('clear')
            mostrar_banner()
            print(" Dica: Use /sdcard/Download/sua_pasta")
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
            print("\033[0;32m--- TUTORIAL: COMO PEGAR UMA API DO TELEGRAM ---\033[0m")
            print(" 1. Acesse: my.telegram.org")
            print(" 2. Faça login com o seu número.")
            print(" 3. Clique em 'API development tools'.")
            print(" 4. Crie um App e copie o 'api_id' e 'api_hash'.\n")
            
            novo_id = await asyncio.to_thread(input, " Digite o novo API_ID: ")
            novo_hash = await asyncio.to_thread(input, " Digite o novo API_HASH: ")
            
            if novo_id and novo_hash:
                try:
                    config["api_id"] = int(novo_id)
                    config["api_hash"] = novo_hash.strip()
                    salvar_config(config)
                    print("\n\033[0;32m[!] API salva com sucesso! O script será fechado.\033[0m")
                    print("\033[0;32m[!] Rode 'python extrator.py' novamente para logar.\033[0m")
                    await asyncio.sleep(3)
                    return 
                except ValueError:
                    print("\n\033[1;31m[ERRO] O API_ID precisa ser um número.\033[0m")
                    await asyncio.sleep(2)

        elif opcao == '4':
            os.system('clear')
            mostrar_banner()
            try: os.makedirs(config["download_dir"], exist_ok=True)
            except: pass

            print(f"\n\033[0;32m[!] Iniciando captura...\033[0m")
            print(" Abra o bot no celular e clique nos botões.")
            print(" \033[1;31mPressione Ctrl+C para parar e voltar ao menu.\033[0m\n")
            
            try:
                await client.send_message(config["bot_alvo"], '/start')
                while True: await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n\033[0;32m[!] Captura pausada. Voltando...\033[0m")
                await asyncio.sleep(1.5)
                
        elif opcao == '5':
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
