import pytest

from exchunker.cli import main
from exchunker.core import chunk_bytes, read_chunks, to_hex


def test_to_hex_basic():
    assert to_hex(b"\x00\xff\x10") == "00ff10"


def test_to_hex_separator_and_uppercase():
    assert to_hex(b"\xab\xcd", ":", uppercase=True) == "AB:CD"


def test_chunk_bytes_sizes():
    assert list(chunk_bytes(b"abcdefg", 3)) == [b"abc", b"def", b"g"]


def test_invalid_chunk_size():
    with pytest.raises(ValueError):
        list(chunk_bytes(b"abc", 0))


def test_read_chunks(tmp_path):
    f = tmp_path / "data.bin"
    f.write_bytes(bytes(range(10)))
    chunks = list(read_chunks(f, 4))
    assert [len(c) for c in chunks] == [4, 4, 2]
    assert b"".join(chunks) == bytes(range(10))


def test_read_chunks_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        list(read_chunks(tmp_path / "no_existe.bin"))


def test_cli_text(capsys):
    assert main(["--text", "Hola", "--bytes", "2"]) == 0
    assert capsys.readouterr().out.splitlines() == ["486f", "6c61"]


def test_cli_file_with_offset(tmp_path, capsys):
    f = tmp_path / "a.bin"
    f.write_bytes(b"ABCD")
    assert main(["-f", str(f), "-b", "2", "--offset", "-s", " "]) == 0
    assert capsys.readouterr().out.splitlines() == ["00000000: 41 42", "00000002: 43 44"]


def test_cli_missing_file_returns_1(capsys):
    assert main(["--file", "/ruta/inexistente"]) == 1
    assert "no se encontro" in capsys.readouterr().err


def test_cli_invalid_bytes_returns_2(capsys):
    assert main(["--text", "x", "--bytes", "0"]) == 2