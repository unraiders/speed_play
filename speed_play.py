import requests
import time

# Configuración
TAUTULLI_API_KEY = 'TU_TAUTULLI_API_KEY'
TAUTULLI_URL = 'TU_TAUTULLI_URL/api/v2' # formato: http://IP:PUERTO/api/v2
QBITTORRENT_URL = 'TU_QBITTORRENT_URL' # formato: http://IP:PUERTO
QBITTORRENT_USER = 'TU_QBITTORRENT_USER'
QBITTORRENT_PASSWORD = 'TU_QBITTORRENT_PASSWORD'
WAIT_TIME = 10  # Tiempo en segundos antes de desactivar la velocidad alternativa tras detener la reproducción
WAIT_CHECK = 10 # Tiempo entre comprobaciones si hay medios en reproducción

# Sesión para qBittorrent
session = requests.Session()

# Función para iniciar sesión en qBittorrent
def iniciar_sesion_qbittorrent():
    login_url = f"{QBITTORRENT_URL}/api/v2/auth/login"
    data = {'username': QBITTORRENT_USER, 'password': QBITTORRENT_PASSWORD}
    response = session.post(login_url, data=data)
    if response.status_code == 200 and "Ok." in response.text:
        print("Sesión iniciada en qBittorrent.")
    else:
        print(f"Error iniciando sesión en qBittorrent: {response.status_code} - {response.text}")

# Función para verificar si la velocidad alternativa está activa
def comprobar_estado_velocidad_alternativa():
    url = f"{QBITTORRENT_URL}/api/v2/transfer/speedLimitsMode"
    response = session.get(url)
    if response.status_code == 200:
        modo_alternativo = response.json()
        print(f"Modo de velocidad alternativa: {'Activo' if modo_alternativo else 'Desactivado'}")
        return modo_alternativo
    else:
        print(f"Error comprobando el modo de velocidad alternativa: {response.status_code} - {response.text}")
        return None

# Funciones para alternar el modo de velocidad alternativa
def activar_velocidad_alternativa():
    url = f"{QBITTORRENT_URL}/api/v2/transfer/toggleSpeedLimitsMode"
    response = session.post(url)
    if response.status_code == 200:
        print("Velocidad alternativa activada en qBittorrent.")
    else:
        print(f"Error activando velocidad alternativa: {response.status_code} - {response.text}")

def desactivar_velocidad_alternativa():
    url = f"{QBITTORRENT_URL}/api/v2/transfer/toggleSpeedLimitsMode"
    response = session.post(url)
    if response.status_code == 200:
        print("Velocidad alternativa desactivada en qBittorrent.")
    else:
        print(f"Error desactivando velocidad alternativa: {response.status_code} - {response.text}")

# Verificar si hay reproducción en curso en Plex a través de Tautulli
def verificar_reproduccion_en_curso():
    url = f"{TAUTULLI_URL}?apikey={TAUTULLI_API_KEY}&cmd=get_activity"
    response = requests.get(url)
    data = response.json()
    streams = data['response']['data']['sessions']
    print(f"Reproducción en curso: {len(streams) > 0}")
    return len(streams) > 0  # True si hay reproducción en curso, False si no

def main():
    iniciar_sesion_qbittorrent()
    reproduccion_en_curso = False

    while True:
        en_reproduccion = verificar_reproduccion_en_curso()

        if en_reproduccion and not reproduccion_en_curso:
            activar_velocidad_alternativa()
            # Confirmación del estado
            if comprobar_estado_velocidad_alternativa():
                print("Velocidad alternativa activada en qBittorrent.")
            reproduccion_en_curso = True

        elif not en_reproduccion and reproduccion_en_curso:
            time.sleep(WAIT_TIME)
            desactivar_velocidad_alternativa()
            # Confirmación del estado
            if not comprobar_estado_velocidad_alternativa():
                print("Velocidad alternativa desactivada en qBittorrent.")
            reproduccion_en_curso = False

        time.sleep(WAIT_CHECK)  # Espera antes de verificar de nuevo el estado de reproducción

if __name__ == "__main__":
    main()