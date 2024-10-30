from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, GiftEvent, LikeEvent, FollowEvent, JoinEvent
from flask import Flask, jsonify, render_template
import threading

# Inicialize o cliente TikTok e a aplicação Flask
client = TikTokLiveClient(unique_id="@satturnni")
app = Flask(__name__)

# Lista para armazenar eventos para exibição
event_log = []

# Função auxiliar para adicionar eventos
def add_event(event_type, message):
    event_log.append({"type": event_type, "message": message})
    if len(event_log) > 50:  # Limite de 50 eventos armazenados
        event_log.pop(0)

# Eventos TikTok
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    add_event("Conexão", f"Conectado a @{event.unique_id} (ID da sala: {client.room_id})")

@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    add_event("Presente", f"{event.user.nickname} enviou um presente: {event.gift.name}")

@client.on(LikeEvent)
async def on_like(event: LikeEvent):
    add_event("Like", f"{event.user.nickname} deu um like! Obrigado pelo like")

@client.on(FollowEvent)
async def on_follow(event: FollowEvent):
    add_event("Seguidor", f"{event.user.nickname} começou a seguir! Bem-vindo(a)")

@client.on(JoinEvent)
async def on_join(event: JoinEvent):
    add_event("Entrada", f"{event.user.nickname} entrou na live!")

# Rota para página inicial
@app.route("/")
def index():
    return render_template("index.html")

# Rota para obter eventos em JSON
@app.route("/events")
def events():
    return jsonify(event_log)

# Função para iniciar o cliente TikTok em uma nova thread
def start_tiktok_client():
    client.run()

# Iniciar o cliente TikTok e o servidor Flask
if __name__ == "__main__":
    # Inicia o cliente TikTok em uma nova thread
    threading.Thread(target=start_tiktok_client).start()
    # Inicia o servidor Flask
    app.run(debug=True)
