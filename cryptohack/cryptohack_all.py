#!/usr/bin/env python3
# cryptohack/cryptohack_all.py
# Soluciones: ejercicio 01 (intro) y ejercicio 02 (great_snakes.py).
# Ejecuta: python cryptohack_all.py       -> muestra todas las soluciones implementadas
#          python cryptohack_all.py 1     -> muestra sólo la solución 1
#          python cryptohack_all.py 2     -> muestra sólo la solución 2

import os
import sys
import subprocess
import re
from typing import Optional

FLAG_RE = re.compile(r"crypto\{[^}]+\}")

def solve_01_intro() -> str:
    """
    Ejercicio 01: devolver la flag exactamente como pide la plataforma.
    """
    return "crypto{y0ur_f1rst_fl4g}"

def extract_flag_from_text(text: str) -> Optional[str]:
    """
    Busca y devuelve la primera coincidencia con el patrón crypto{...}.
    """
    m = FLAG_RE.search(text)
    return m.group(0) if m else None

def run_script_capture_output(script_path: str) -> (int, str, str):
    """
    Ejecuta un script Python con el intérprete actual y devuelve (returncode, stdout, stderr).
    """
    try:
        # Usamos sys.executable para asegurarnos de usar el mismo intérprete Python
        proc = subprocess.run([sys.executable, script_path],
                              capture_output=True, text=True, timeout=30)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Execution timed out."
    except Exception as e:
        return -1, "", f"Error launching script: {e}"

def solve_02_great_snakes() -> str:
    """
    Ejecuta great_snakes.py (debe estar en la misma carpeta que este archivo)
    y devuelve la flag encontrada en la salida estándar o dentro del propio archivo.
    """
    base_dir = os.path.dirname(__file__) or "."
    script_name = "great_snakes.py"
    script_path = os.path.join(base_dir, script_name)

    # 1) Si el script existe, intentar ejecutarlo y capturar salida
    if os.path.isfile(script_path):
        rc, out, err = run_script_capture_output(script_path)
        if rc == 0:
            # Buscar la flag en stdout
            flag = extract_flag_from_text(out)
            if flag:
                return flag
            # Si no hay flag en stdout, devolver stdout (por si es auto-evidente)
            return f"No se encontró flag en la salida, pero el script se ejecutó correctamente.\nSalida:\n{out.strip() or '[vacía]'}"
        else:
            # Si hubo error al ejecutar, intentamos extraer la flag del archivo sin ejecutar
            preview = f"Ejecución fallida (rc={rc}). stderr:\n{err.strip()}\n\nIntentando búsqueda estática en el fichero..."
            try:
                with open(script_path, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read()
                flag = extract_flag_from_text(txt)
                if flag:
                    return f"{preview}\nFlag encontrada en el fichero: {flag}"
                else:
                    return f"{preview}\nNo se encontró ninguna cadena con formato crypto{{...}} en el fichero."
            except Exception as e:
                return f"{preview}\nAdemás, no se pudo leer el fichero para búsqueda estática: {e}"
    else:
        # 2) Si el script no existe, informar y (opcional) buscar en la carpeta actual por archivos parecidos
        candidates = []
        for fname in os.listdir(base_dir):
            if "snake" in fname.lower() or "great" in fname.lower():
                candidates.append(fname)
        msg = f"No se encontró '{script_name}' en {base_dir}."
        if candidates:
            msg += f" Archivos parecidos en la carpeta: {', '.join(candidates)}\nPuedes renombrar el script a {script_name} o colocarlo junto a este archivo."
            # Intentar búsqueda estática en los candidatos
            for c in candidates:
                try:
                    with open(os.path.join(base_dir, c), "r", encoding="utf-8", errors="ignore") as f:
                        txt = f.read()
                    flag = extract_flag_from_text(txt)
                    if flag:
                        return f"{msg}\nFlag encontrada estáticamente en '{c}': {flag}"
                except Exception:
                    continue
        return msg

def main(selected: Optional[int] = None) -> None:
    solvers = {
        1: ("Intro - flag", solve_01_intro),
        2: ("Great Snakes (ejecutar great_snakes.py)", solve_02_great_snakes),
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
        print("\nPara ejecutar solo uno: python cryptohack_all.py 2  (ejemplo: muestra solo el ejercicio 2)")
    else:
        if selected in solvers:
            name, fn = solvers[selected]
            print(f"Ejercicio {selected}: {name}\n{fn()}")
        else:
            print(f"No hay solución para el ejercicio {selected} (aún).")

if __name__ == "__main__":
    # Permite pasar un número de ejercicio por argumento opcional
    if len(sys.argv) > 1:
        try:
            idx = int(sys.argv[1])
        except ValueError:
            idx = None
        main(idx)
    else:
        main()
