import yt_dlp
import os
from pydub import AudioSegment

download_folder = "downloads"
os.makedirs(download_folder, exist_ok=True)

def baixar_musica(nome_musica):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'quiet': True  
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_url = f"ytsearch:{nome_musica}"
        info_dict = ydl.extract_info(search_url, download=True)
        
        if 'entries' not in info_dict or len(info_dict['entries']) == 0:
            print(f'Erro: Música "{nome_musica}" não encontrada.')
            return
        
        titulo = info_dict['entries'][0]['title']
        arquivo_original = os.path.join(download_folder, f"{titulo}.webm") 
        
        if not os.path.exists(arquivo_original):
            print(f'Erro: O arquivo "{arquivo_original}" não foi encontrado.')
            return
        
        arquivo_mp3 = os.path.join(download_folder, f"{titulo}.mp3")
        audio = AudioSegment.from_file(arquivo_original)
        audio.export(arquivo_mp3, format="mp3")

        os.remove(arquivo_original)

        print(f'Música baixada e salva como MP3: {arquivo_mp3}')

def baixar_lista_musicas(arquivo_txt):
    if not os.path.exists(arquivo_txt):
        print(f'Erro: O arquivo "{arquivo_txt}" não foi encontrado.')
        return
    
    with open(arquivo_txt, 'r', encoding='utf-8') as file:
        musicas = [linha.strip() for linha in file.readlines() if linha.strip()]

    if not musicas:
        print('Erro: O arquivo de músicas está vazio.')
        return

    for musica in musicas:
        print(f'Baixando: {musica}')
        baixar_musica(musica)

arquivo_musicas = "app/input/musicas.txt"
baixar_lista_musicas(arquivo_musicas)
