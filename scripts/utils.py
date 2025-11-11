import requests
import re

def get_twitch_stream_url(username):
    """
    Método alternativo para obtener URLs de stream de Twitch
    """
    try:
        # Usar servicio de terceros para obtener m3u8
        services = [
            f"https://twitch.projects.zabs.pro/{username}.m3u8",
            f"https://api.ttv.live/playlist/{username}.m3u8",
            f"https://twitch.facepunch.com/{username}.m3u8"
        ]
        
        for service_url in services:
            try:
                response = requests.get(service_url, timeout=5)
                if response.status_code == 200 and '.m3u8' in response.text:
                    return service_url
            except:
                continue
                
        return None
    except Exception as e:
        print(f"Error en método alternativo: {e}")
        return None
