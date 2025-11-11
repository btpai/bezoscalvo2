#!/usr/bin/env python3
import requests
import json
import re
import time
from urllib.parse import quote
import os
from typing import List, Dict, Optional

class TwitchIPTVGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko'  # Client-ID público de Twitch
        })
    
    def get_channel_info(self, username: str) -> Optional[Dict]:
        """Obtiene información del canal usando la API de Twitch"""
        try:
            # Query GraphQL de Twitch
            query = {
                "operationName": "ChannelVideoLength",
                "variables": {"login": username.lower()},
                "extensions": {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "eecf815273d3d949e5cf0085cc5084cd8a1b5b7b6e4c27c68a9e9fade1a5f7f6"
                    }
                }
            }
            
            response = self.session.post(
                "https://gql.twitch.tv/gql",
                json=query,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'user' in data['data']:
                    return data['data']['user']
            return None
            
        except Exception as e:
            print(f"Error obteniendo info de {username}: {e}")
            return None
    
    def get_stream_playlist(self, username: str) -> Optional[str]:
        """Intenta obtener la URL del stream m3u8"""
        try:
            # Método 1: Usando la API de streams
            url = f"https://twitch.tv/{username}"
            response = self.session.get(url, timeout=10)
            
            # Buscar en el HTML
            patterns = [
                r'"playbackAccessToken":{"value":"([^"]+)"',
                r'"accessToken":"([^"]+)"',
                r'm3u8.*?url":"([^"]+)"'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, response.text)
                if matches:
                    token = matches[0]
                    # Construir URL del stream
                    stream_url = f"https://usher.ttvnw.net/api/channel/hls/{username}.m3u8?token={token}&sig=123"
                    return stream_url
            
            # Método 2: Usar servicio externo como Twitch API
            api_url = f"https://api.ttv.live/playlist/{username}.m3u8"
            response = self.session.get(api_url, timeout=5)
            if response.status_code == 200:
                return api_url
                
            return None
            
        except Exception as e:
            print(f"Error obteniendo stream de {username}: {e}")
            return None
    
    def generate_m3u_playlist(self, channels: List[str]) -> str:
        """Genera la lista M3U completa"""
        playlist = "#EXTM3U\n"
        playlist += "# Playlist IPTV generada automáticamente desde Twitch\n"
        playlist += "# Actualizado: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n"
        
        for username in channels:
            username = username.strip().lower()
            if not username:
                continue
                
            print(f"Procesando canal: {username}")
            
            channel_info = self.get_channel_info(username)
            stream_url = self.get_stream_playlist(username)
            
            if channel_info and stream_url:
                title = channel_info.get('displayName', username)
                description = channel_info.get('description', 'Stream de Twitch')
                is_live = channel_info.get('stream') is not None
                
                # Formato M3U
                playlist += f'#EXTINF:-1 tvg-id="{username}" tvg-name="{title}" group-title="Twitch",{title}\n'
                playlist += f'#EXTVLCOPT:network-caching=1000\n'
                playlist += stream_url + "\n\n"
                
                print(f"✓ {title} - Añadido a la lista")
            else:
                print(f"✗ {username} - No disponible")
            
            time.sleep(1)  # Rate limiting
        
        return playlist
    
    def save_playlist(self, playlist: str, filename: str = "twitch_iptv.m3u"):
        """Guarda la lista en un archivo"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(playlist)
        print(f"Lista guardada en: {filename}")

def main():
    # Leer lista de canales
    channels_file = "channels/channels.txt"
    if not os.path.exists(channels_file):
        print(f"Error: No se encuentra {channels_file}")
        return
    
    with open(channels_file, 'r', encoding='utf-8') as f:
        channels = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"Procesando {len(channels)} canales...")
    
    # Generar lista IPTV
    generator = TwitchIPTVGenerator()
    playlist = generator.generate_m3u_playlist(channels)
    
    # Guardar lista
    output_file = "twitch_iptv.m3u"
    generator.save_playlist(playlist, output_file)
    
    # Guardar también en el directorio docs para GitHub Pages
    docs_dir = "docs"
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    
    generator.save_playlist(playlist, f"{docs_dir}/{output_file}")
    
    print("¡Lista IPTV generada exitosamente!")

if __name__ == "__main__":
    main()
