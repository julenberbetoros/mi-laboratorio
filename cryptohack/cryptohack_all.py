#!/usr/bin/env python3
# cryptohack_all_improved.py
# Versión mejorada de cryptohack_all.py con heurísticas para el ejercicio 10

import os
import sys
import subprocess
import re
import base64
from typing import Optional, List, Tuple
import itertools

FLAG_RE = re.compile(r"crypto\{[A-Za-z0-9_]+\}")

# ===============================
# === FUNCIONES AUXILIARES ======
# ===============================
def long_to_bytes(n: int) -> bytes:
    if n == 0:
        return b"\x00"
    length = (n.bit_length() + 7) // 8
    return n.to_bytes(length, "big")


def xor_bytes(a: bytes, b: bytes) -> bytes:
    if len(a) != len(b):
        raise ValueError(f"Longitudes diferentes: {len(a)} vs {len(b)}")
    return bytes(x ^ y for x, y in zip(a, b))


def extract_flag_from_text(text: str) -> Optional[str]:
    m = FLAG_RE.search(text)
    return m.group(0) if m else None


def run_script_capture_output(script_path: str) -> (int, str, str):
    try:
        proc = subprocess.run([sys.executable, script_path],
                              capture_output=True, text=True, timeout=30)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Execution timed out."
    except Exception as e:
        return -1, "", f"Error launching script: {e}"

# ===============================
# === EJERCICIOS 01-10 ==========
# ===============================
def solve_01_intro() -> str:
    return "crypto{y0ur_f1rst_fl4g}"


def solve_02_great_snakes() -> str:
    base_dir = os.path.dirname(__file__) or "."
    script_name = "great_snakes.py"
    script_path = os.path.join(base_dir, script_name)
    if os.path.isfile(script_path):
        rc, out, err = run_script_capture_output(script_path)
        if rc == 0:
            flag = extract_flag_from_text(out)
            if flag:
                return flag
            return f"No se encontró flag en la salida.\nSalida:\n{out.strip() or '[vacía]'}"
        else:
            preview = f"Ejecución fallida (rc={rc}). stderr:\n{err.strip()}\n"
            try:
                with open(script_path, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read()
                flag = extract_flag_from_text(txt)
                if flag:
                    return f"{preview}\nFlag encontrada en el fichero: {flag}"
                else:
                    return f"{preview}\nNo se encontró ninguna cadena crypto{{...}} en el fichero."
            except Exception as e:
                return f"{preview}\nError al leer el fichero: {e}"
    else:
        candidates = [f for f in os.listdir(base_dir) if "snake" in f.lower() or "great" in f.lower()]
        msg = f"No se encontró '{script_name}' en {base_dir}."
        if candidates:
            msg += f" Archivos similares: {', '.join(candidates)}"
        return msg


def solve_03_ascii_array() -> str:
    nums = [99,114,121,112,116,111,123,65,83,67,73,73,95,112,114,49,110,116,52,98,108,51,125]
    return "".join(chr(n) for n in nums)


def solve_04_hex_to_ascii() -> str:
    hex_string = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"
    return bytes.fromhex(hex_string).decode("utf-8")


def solve_05_hex_to_base64() -> str:
    hex_str = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
    raw = bytes.fromhex(hex_str)
    return base64.b64encode(raw).decode()


def solve_06_bigint_to_bytes() -> str:
    n = 11515195063862318899931685488813747395775516287289682636499965282714637259206269
    message_bytes = long_to_bytes(n)
    return message_bytes.decode("utf-8")


def solve_07_xor_label() -> str:
    s = "label"
    transformed = "".join(chr(ord(c) ^ 13) for c in s)
    return f"crypto{{{transformed}}}"


def solve_08_xor_chain() -> str:
    KEY1_h = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
    K2_xor_K1_h = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
    K2_xor_K3_h = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
    enc_h = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

    key1 = bytes.fromhex(KEY1_h)
    k2_xor_k1 = bytes.fromhex(K2_xor_K1_h)
    k2_xor_k3 = bytes.fromhex(K2_xor_K3_h)
    enc = bytes.fromhex(enc_h)

    key2 = xor_bytes(k2_xor_k1, key1)
    key3 = xor_bytes(k2_xor_k3, key2)
    tmp = xor_bytes(key1, key2)
    tmp2 = xor_bytes(tmp, key3)
    flag_bytes = xor_bytes(enc, tmp2)
    return flag_bytes.decode("utf-8")


def solve_09_single_byte_xor() -> str:
    hex_str = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
    data = bytes.fromhex(hex_str)
    for key in range(256):
        x = bytes(b ^ key for b in data)
        try:
            txt = x.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if "crypto{" in txt:
            return txt
    # fallback: best printable candidate
    best = None
    best_ratio = -1.0
    for key in range(256):
        x = bytes(b ^ key for b in data)
        try:
            txt = x.decode("utf-8")
        except UnicodeDecodeError:
            continue
        printable = sum(1 for ch in txt if 32 <= ord(ch) <= 126)
        ratio = printable / len(txt)
        if ratio > best_ratio:
            best_ratio = ratio
            best = (key, txt)
    if best:
        return f"[key=0x{best[0]:02x}] {best[1]}"
    return "[No se pudo descifrar]"


def derive_partial_key_from_crib(cipher: bytes, crib: bytes, offset: int, keylen: int) -> List[Optional[int]]:
    """
    Devuelve una lista de longitud keylen con bytes conocidos (o None) del key,
    basados en que `crib` aparece en `cipher` en `offset`.
    """
    key = [None] * keylen
    for i in range(len(crib)):
        cpos = offset + i
        kpos = cpos % keylen
        key_byte = cipher[cpos] ^ crib[i]
        if key[kpos] is None:
            key[kpos] = key_byte
        elif key[kpos] != key_byte:
            # conflicto -> no válido
            return []
    return key


def is_mostly_printable(s: bytes, threshold: float = 0.95) -> bool:
    if not s:
        return False
    printable = sum(1 for ch in s if 32 <= ch <= 126)
    return (printable / len(s)) >= threshold


def key_bytes_are_printable_ascii(k: bytes) -> bool:
    # prefer claves formadas por caracteres legibles (letras/dígitos/_)
    return all(32 <= b <= 126 for b in k)


def fill_and_test_key_improved(cipher: bytes, key_partial: List[Optional[int]], max_unknowns_bruteforce: int = 3) -> Optional[Tuple[str, bytes]]:
    """
    Si el número de posiciones None en key_partial <= max_unknowns_bruteforce,
    fuerza bruta esas posiciones y prueba cada key completa. Devuelve la flag y la clave (bytes) si la encuentra.
    Aplica filtros heurísticos para reducir falsos positivos.
    """
    keylen = len(key_partial)
    unknown_positions = [i for i, b in enumerate(key_partial) if b is None]
    unk = len(unknown_positions)
    if unk > max_unknowns_bruteforce:
        return None
    # valores a probar para cada unknown
    # iteramos combinaciones
    for combo in itertools.product(range(256), repeat=unk):
        key = list(key_partial)
        for pos, val in zip(unknown_positions, combo):
            key[pos] = val
        key_bytes = bytes(key)
        plain = bytes(cipher[i] ^ key_bytes[i % keylen] for i in range(len(cipher)))
        # filtro 1: el texto debe ser mayoritariamente imprimible
        if not is_mostly_printable(plain, threshold=0.95):
            continue
        try:
            txt = plain.decode('utf-8')
        except UnicodeDecodeError:
            # si no es utf-8, descartamos (flag debe ser ascii)
            continue
        # filtro 2: debe contener la flag en formato esperado
        flag = extract_flag_from_text(txt)
        if not flag:
            continue
        # filtro 3 (heurístico): preferir si la clave es ascii imprimible (mejor para documentar)
        if key_bytes_are_printable_ascii(key_bytes):
            return flag, key_bytes
        # si no es ascii printable, aún podemos devolverlo pero lo hacemos al final
        return flag, key_bytes
    return None


def solve_10_secret_key_xor() -> str:
    hex_str = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
    cipher = bytes.fromhex(hex_str)
    n = len(cipher)
    crib = b"crypto{"
    # intentar keylen plausibles; probamos 1..40
    for keylen in range(1, 41):
        for offset in range(0, n - len(crib) + 1):
            key_partial = derive_partial_key_from_crib(cipher, crib, offset, keylen)
            if key_partial == []:
                # conflicto detectado, saltar
                continue
            # si no hay conflictos, probar fuerza bruta para pocas posiciones faltantes
            res = fill_and_test_key_improved(cipher, key_partial, max_unknowns_bruteforce=3)
            if res:
                flag, key_bytes = res
                try:
                    key_ascii = key_bytes.decode('utf-8')
                except Exception:
                    key_ascii = None
                return f"FLAG: {flag}\nkey (hex): {key_bytes.hex()}\nkey (ascii, if printable): {key_ascii}"
    # si no encontró nada, devolvemos candidatas de depuración (keylen=8 como fallback)
    debug_lines = []
    keylen = 8
    for offset in range(0, n - len(crib) + 1):
        kp = derive_partial_key_from_crib(cipher, crib, offset, keylen)
        if kp == []:
            continue
        filled = bytes([b if b is not None else 0 for b in kp])
        plain = bytes(cipher[i] ^ filled[i % keylen] for i in range(n))
        try:
            txt = plain.decode("utf-8", errors="ignore")
        except Exception:
            txt = plain.decode("latin-1", errors="ignore")
        score = sum(1 for ch in txt if 32 <= ord(ch) <= 126)
        debug_lines.append(f"[offset={offset} partial_key={kp} filled=0x{filled.hex()} score={score}] {txt[:80]}")
    if debug_lines:
        return "No encontrada automáticamente. Candidatas (keylen=8):\n" + "\n".join(debug_lines[:8])
    return "[No se pudo descifrar el mensaje automáticamente]"

# =======================================
# === EJECUCIÓN GENERAL =================
# =======================================

def main(selected: Optional[int] = None) -> None:
    solvers = {
        1: ("Intro - flag", solve_01_intro),
        2: ("Great Snakes (ejecutar script)", solve_02_great_snakes),
        3: ("ASCII array -> flag", solve_03_ascii_array),
        4: ("Hexadecimal -> ASCII", solve_04_hex_to_ascii),
        5: ("Hex -> Base64", solve_05_hex_to_base64),
        6: ("Bytes and Big Integers", solve_06_bigint_to_bytes),
        7: ("XOR 'label' with 13 -> flag", solve_07_xor_label),
        8: ("XOR chain -> flag", solve_08_xor_chain),
        9: ("Single-byte XOR cipher", solve_09_single_byte_xor),
        10: ("Secret XOR - crib + brute (auto)", solve_10_secret_key_xor),
    }

    if selected is None:
        print("=== Cryptohack: soluciones disponibles ===")
        for k, (name, fn) in sorted(solvers.items()):
            print(f"\n-- Ejercicio {k}: {name} --")
            try:
                result = fn()
            except Exception as e:
                result = f"ERROR al ejecutar: {e}"
            print(result)
        print("\nPara ejecutar solo uno: python cryptohack_all_improved.py 10")
    else:
        if selected in solvers:
            name, fn = solvers[selected]
            print(f"Ejercicio {selected}: {name}\n{fn()}")
        else:
            print(f"No hay solución para el ejercicio {selected}.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            idx = int(sys.argv[1])
        except ValueError:
            idx = None
        main(idx)
    else:
        main()
