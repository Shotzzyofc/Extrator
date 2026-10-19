```markdown
# 🕵️‍♂️ Extrator Telegram - PRO

Painel interativo via terminal (Termux) para extração de mídias, textos e estrutura de funis de bots do Telegram. Utiliza a API MTProto (Telethon) para contornar restrições de encaminhamento e salvar o conteúdo localmente.

## 🚀 Instalação Rápida (One-Line)

Requisito: Ter o **Termux** instalado (recomendado baixar via F-Droid).

Abra o Termux, cole o comando abaixo e aperte Enter. Ele instalará as dependências, pedirá permissão de armazenamento (aceite o pop-up) e abrirá o painel:

```bash
pkg update -y && pkg install python curl -y && pip install telethon && termux-setup-storage && curl -sL "https://raw.githubusercontent.com/Shotzzyofc/Extrator/refs/heads/main/extrator.py" -o extrator.py && python extrator.py
```

⚙️ Como usar o Painel

Ao iniciar pela primeira vez, o script solicitará:

1. Seu número de telefone (com DDI: +55...)
2. O código de verificação recebido no Telegram.
3. Senha de duas etapas (se ativada).

Menu de Opções:

· [1] Trocar Bot Alvo: Insira o @ do bot que deseja extrair.
· [2] Alterar Pasta de Salvamento: Define onde os arquivos e logs serão salvos. O padrão é /sdcard/Download/previas_extraidas.
· [3] Alterar API (ID e Hash): Permite trocar as credenciais do Telegram. (Inclui tutorial embutido de como gerar em my.telegram.org).
· [4] Iniciar Captura: O script envia /start ao bot e fica ouvindo. Abra o bot no celular, clique nos botões do funil e o script salvará tudo.
· [5] Sair: Desconecta e fecha.

Para parar uma captura, pressione Ctrl + C no teclado do Termux.

📂 Estrutura de Saída

Todo o conteúdo capturado será salvo na pasta escolhida:

· Mídias: Vídeos e fotos são baixados na pasta raiz escolhida.
· Histórico: Um arquivo historico_funil.txt é gerado e atualizado em tempo real com todos os textos e botões enviados pelo bot alvo.

⚠️ Aviso Legal

Esta ferramenta é destinada para fins de análise de concorrência e auditoria de segurança. O usuário é o único responsável pelo uso do conteúdo extraído.

---

Desenvolvido por @zetx.py

```
