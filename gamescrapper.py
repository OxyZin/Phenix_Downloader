import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import re

# URL do site
BASE_URL = "https://myrient.erista.me/files/Redump/Nintendo%20-%20Wii%20-%20NKit%20RVZ%20%5Bzstd-19-128k%5D/"

# Fazendo a requisição HTTP
try:
    response = requests.get(BASE_URL)
    response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
except requests.exceptions.RequestException as e:
    print(f"Erro ao acessar a URL: {e}")
    exit()

# Analisando o HTML
soup = BeautifulSoup(response.text, "html.parser")

games = []

# Iterando sobre as linhas da tabela
table_rows = soup.find_all("tr")
for row in table_rows:
    # Encontrando o link e o tamanho do arquivo
    link_tag = row.find("a")
    size_tag = row.find("td", class_="size")
    
    if link_tag and size_tag:
        filename = link_tag.text.strip()
        if filename.endswith(".zip"):  # Apenas arquivos ZIP
            
            # Decodificando o nome do jogo
            decoded_name = urllib.parse.unquote(filename).replace(".zip", "")
            
            # Extraindo região do nome do jogo
            region = "Unknown"
            region_match = re.search(r"\((USA|Europe|Japan|Canada|Germany|Korea|Australia)\)", decoded_name)
            if region_match:
                region = region_match.group(1)
                decoded_name = decoded_name.replace(region_match.group(0), "").strip()
            
            # Removendo revisões do nome (ex: "Rev 1")
            decoded_name = re.sub(r"\(Rev \d+\)", "", decoded_name).strip()
            
            # Removendo informações de idioma (ex: "(En,Fr,De,Es,It)")
            decoded_name = re.sub(r"\([^)]*\)", "", decoded_name).strip()  # Remove tudo entre parênteses
            decoded_name = re.sub(r"\s+", " ", decoded_name).strip()  # Remove espaços extras
            
            # Criando o objeto do jogo
            game_data = {
                "title": decoded_name,
                "console": "Nintendo Wii",
                "downloadlink": urllib.parse.urljoin(BASE_URL, link_tag["href"]),
                "image": "https://placehold.co/320x180",  # Placeholder para a imagem
                "size": size_tag.text.strip(),
                "region": region,
            }
            
            games.append(game_data)

# Salvando o JSON
try:
    with open("wii_games.json", "w", encoding="utf-8") as f:
        json.dump(games, f, indent=4, ensure_ascii=False)
    print("Arquivo wii_games.json gerado com sucesso!")
except Exception as e:
    print(f"Erro ao salvar o arquivo JSON: {e}")