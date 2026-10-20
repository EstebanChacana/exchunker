# ARCHIVO DE INICIALIZACIÓN DEL PAQUETE
# expone las funciones principales y define la informacion del paquete

# importamos las funciones del modulo core para que se puedan usar directamente desde el paquete
from .core import DEFAULT_CHUNK_SIZE, chunk_bytes, read_chunks, to_hex

# version actual de la librería
__version__ = "0.1.0"

# lista de elementos públicos que se exportan cuando alguien usa esta librería
__all__ = ["DEFAULT_CHUNK_SIZE", "chunk_bytes", "read_chunks", "to_hex"]