# 🤖 Bot Discord Multifuncional

Um bot Discord poderoso e versátil, criado para tornar seu servidor mais interativo e divertido!

## ✨ Funcionalidades

### 🎵 Sistema de Música
- `!tocar` - Toca música do YouTube
- `!pausar` - Pausa a música atual
- `!retomar` - Retoma a música pausada
- `!pular` - Pula para a próxima música
- `!fila` - Mostra a fila de músicas
- `!sair` - Sai do canal de voz

### 🎲 Diversão
- `!moeda` - Cara ou coroa
- `!dado [lados]` - Rola um dado (padrão: 6 lados)
- `!sorteio` - Realiza um sorteio
- `!enquete` - Cria uma enquete interativa

### 📊 Informações
- `!ping` - Mostra a latência do bot
- `!serverinfo` - Exibe informações do servidor
- `!userinfo` - Mostra informações de um usuário
- `!seguidores` - Exibe contagem de seguidores das redes sociais
- `!avatar` - Mostra o avatar de um usuário

### 🛠️ Moderação
- `!limpar [quantidade]` - Limpa mensagens do chat
- Sistema automático de boas-vindas
- Notificação de saída de membros

## 🚀 Configuração

1. Clone este repositório
2. Crie um arquivo `.env` com as seguintes variáveis:
```env
DISCORD_BOT_TOKEN=seu_token_aqui
YOUTUBE_API_KEY=sua_chave_api_youtube
RAPIDAPI_KEY=sua_chave_rapidapi
```

3. Instale as dependências:
```bash
pip install discord.py python-dotenv yt-dlp requests beautifulsoup4
```

4. Execute o bot:
```bash
python bot.py
```

## 🔧 Requisitos
- Python 3.8 ou superior
- FFmpeg (baixado automaticamente)
- Conexão com internet

## 🔑 APIs Utilizadas
- Discord API
- YouTube Data API
- RapidAPI (para Instagram e TikTok)

## 📝 Notas
- O bot utiliza FFmpeg para streaming de áudio
- Suporte automático para download do FFmpeg
- Sistema de fila de músicas otimizado
- Recursos de moderação integrados

## 🤝 Contribuição
Sinta-se à vontade para contribuir com o projeto! Abra uma issue ou envie um pull request.

## 📜 Licença
Este projeto está sob a licença MIT.
