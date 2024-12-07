# SPEED PLAY

Script para comprobar a través de la API de Tautulli si hay medios en reproducción para poner qBittorrent en el modo de velocidad 'Alternativa', desde la config de qBittorrent definimos cual será la velocidad alternativa a aplicar.

Variables a configurar dentro del script speed_play.py:

  - TAUTULLI_API_KEY = 'TU_TAUTULLI_API_KEY'
  - TAUTULLI_URL = 'TU_TAUTULLI_URL/api/v2' # formato: http://IP:PUERTO/api/v2
  - QBITTORRENT_URL = 'TU_QBITTORRENT_URL' # formato: http://IP:PUERTO
  - QBITTORRENT_USER = 'TU_QBITTORRENT_USER'
  - QBITTORRENT_PASSWORD = 'TU_QBITTORRENT_PASSWORD'
  - WAIT_TIME = 10  # Tiempo en segundos antes de desactivar la velocidad alternativa tras detener la reproducción
  - WAIT_CHECK = 10 # Tiempo entre comprobaciones si hay medios en reproducción

En mi caso ejecuto el script con un cron.

Ejemplo: _python3 /mnt/user/appdata/qbittorrent/scripts/speed_play.py_

En el caso de Unraid a través de Nerdtools hay que activar los siguientes complementos: python-pip, python-setuptools, python3.

Funcionando en qBittorrent v4.6.5
