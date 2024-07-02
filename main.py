import pandas as pd
import folium
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# Caminho do arquivo CSV
CSV_PATH = "./data.csv"

# Localização inicial do mapa
INITIAL_LOCATION = [ -5.08921, -42.8016]
INITIAL_ZOOM = 12

def carregar_dados_clinicas():
    try:
        dados = pd.read_csv(CSV_PATH)
        return dados
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao carregar os dados das clínicas: " + str(e))

app = FastAPI()

# Configuração do CORS
origins = ["*"]  # Permite todas as origens. Para mais segurança, especifique as URLs permitidas.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/clinicas")
def obter_clinicas():
    """
    Retorna uma lista de clínicas com suas respectivas localizações.
    """
    dados_clinicas = carregar_dados_clinicas()
    clinicas = []
    for index, row in dados_clinicas.iterrows():
        clinicas.append({
            'nome': row['nome'],
            'latitude': row['latitude'],
            'longitude': row['longitude']
        })
    return clinicas

@app.get("/mapa", response_class=HTMLResponse)
def visualizar_mapa():
    """
    Retorna um mapa HTML com a localização das clínicas.
    """
    dados_clinicas = carregar_dados_clinicas()
    html_mapa = gerar_mapa_com_clinicas(dados_clinicas)
    return html_mapa

def gerar_mapa_com_clinicas(dados_clinicas):
    mapa = folium.Map(location=INITIAL_LOCATION, zoom_start=INITIAL_ZOOM)

    for index, row in dados_clinicas.iterrows():
        nome_clinica = row['nome']
        latitude = row['latitude']
        longitude = row['longitude']

        folium.Marker([latitude, longitude], popup=nome_clinica).add_to(mapa)

    return mapa._repr_html_()

