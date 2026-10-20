
#importar librerias 
from __future__ import annotations

import argparse
import sys 
from typing import Iterable, Iterator, Sequence, TextIO

from . import __version__
from .core import DEFAULT_CHUNK_SIZE, chunk_bytes, read_chunks, to_hex

#definimos las opciones y hara o recibira cada una 
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hexchunker",
        description="convierte archivos o texto a hexadecimal en bloques configurables",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "-f", "--file", 
        help="ruta del archivo a convertir."
    )
    source.add_argument(
        "-t", "--text", 
        help="texto a convertir (UTF-8)."
    )
    parser.add_argument(
        "-b", "--bytes", type=int, default=DEFAULT_CHUNK_SIZE, dest="chunk_size",
        help=f'bytes por bloque (por defecto {DEFAULT_CHUNK_SIZE}).',
    )
    parser.add_argument(
        "-s", "--separator", default="",
        help="caracter separador entre bytes (ej. ' ' o ':')."
    )
    parser.add_argument(
        "-u", "--uppercase", action="store_true", 
        help="hex en mayusculas"
    )
    parser.add_argument(
        "--offset", action="store_true",
        help="antepone el desplazamiento (offset) a cada linea, estilo hexdump." 
    )
    parser.add_argument(
        "-o", "--output", 
        help="archivo de salida (por defecto: stdout)."
    )
    parser.add_argument(
        "-v", "--version", action="version", 
        version=f'%(prog)s {__version__}'
    )
    return parser

#convierte cada bloque de bytes en una linea de texto hexadecimal
def render_lines(chunks: Iterable[bytes], separator: str, uppercase: bool, with_offset: bool) -> Iterator[str]:
    offset = 0
    for chunk in chunks: #<- toma un bloque de bytes a la vez
        line = to_hex(chunk, separator, uppercase) #<- convierte bytes a hexadecimal
        if with_offset:
            line = f'{offset:08x}: {line}'
        yield line
        offset += len(chunk) 

#recibe las lineas de texto que produjo render_lines
def _write(lines: Iterable[str], stream: TextIO) -> None:
    for line in lines:
        stream.write(line + "\n")#<- escribe cada linea y agrega un salto de linea
