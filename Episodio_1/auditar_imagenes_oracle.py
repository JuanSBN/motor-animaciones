import os
import sys
import json
import base64
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(r"c:\Users\Lenovo\Documents\Proyecto\curioreels")
import oracle_remote

# Directorio temporal 100% aislado en Oracle (NO toca ningún archivo de otros proyectos)
REMOTE_TMP_DIR = "/tmp/animaciones_moondream_qa"

def preparar_entorno_remoto():
    # Crear directorio temporal en /tmp
    res = oracle_remote.run_ssh_command(f"mkdir -p {REMOTE_TMP_DIR}")
    if res.returncode != 0:
        raise RuntimeError(f"Error creando directorio temporal en Oracle: {res.stderr}")
    print(f"🔒 Entorno aislado creado en Oracle: {REMOTE_TMP_DIR} (Totalmente separado de otros proyectos)")

def limpiar_entorno_remoto():
    # Limpiar únicamente la carpeta temporal en /tmp
    oracle_remote.run_ssh_command(f"rm -rf {REMOTE_TMP_DIR}")
    print("🧹 Directorio temporal en Oracle eliminado y limpio.")

def auditar_imagen_con_moondream(local_img_path: str, prompt_escena: str) -> dict:
    remote_img_path = f"{REMOTE_TMP_DIR}/inspect.png"
    
    # 1. Subir imagen vía scp a /tmp
    scp_res = oracle_remote.scp_to_remote(local_img_path, remote_img_path)
    if scp_res.returncode != 0:
        return {"status": "ERROR", "error": f"SCP failed: {scp_res.stderr}"}
        
    prompt_qa = (
        "Analyze this cartoon animation frame for video production quality:\n"
        "1. Does it contain technical text, turnaround labels like 'HOJA DE PERSONAJE', model sheet rulers, or character reference charts?\n"
        "2. Does it visually represent: " + prompt_escena[:120] + "?\n"
        "Answer with this exact format:\n"
        "HAS_TECHNICAL_TEXT: [YES or NO]\n"
        "DESCRIPTION: [one concise sentence describing what is visible]\n"
        "VERDICT: [PASS or FAIL]"
    )

    remote_code = f"""
import urllib.request, json, base64

with open('{remote_img_path}', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

data = {{
    'model': 'moondream',
    'messages': [
        {{
            'role': 'user',
            'content': {json.dumps(prompt_qa)},
            'images': [b64]
        }}
    ],
    'stream': False
}}
req = urllib.request.Request(
    'http://localhost:11434/api/chat',
    data=json.dumps(data).encode('utf-8'),
    headers={{'Content-Type': 'application/json'}}
)
try:
    with urllib.request.urlopen(req, timeout=45) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print(res.get('message', {{}}).get('content', ''))
except Exception as e:
    print('ERROR:', e)
"""

    write_cmd = f"cat << 'EOF' > {REMOTE_TMP_DIR}/worker.py\n{remote_code}\nEOF\npython3 {REMOTE_TMP_DIR}/worker.py"
    res = oracle_remote.run_ssh_command(write_cmd)
    
    output = res.stdout.strip()
    has_text = "YES" in output.upper() if "HAS_TECHNICAL_TEXT:" in output.upper() else False
    if "hoja de personaje" in output.lower() or "turnaround" in output.lower():
        has_text = True
        
    verdict = "FAIL" if has_text or "FAIL" in output.upper() else "PASS"
    
    return {
        "output_raw": output,
        "has_technical_text": has_text,
        "verdict": verdict
    }

def main():
    preparar_entorno_remoto()
    
    with open("esquema_maestro.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    reporte = []
    fallidas = []
    
    total_planos = sum(len(e["planos"]) for e in data["escenas"])
    contador = 0
    
    print(f"\n🚀 Iniciando auditoría con Moondream en Oracle sobre las {total_planos} imágenes...\n")
    
    try:
        for escena in data["escenas"]:
            id_e = escena["id"]
            for plano in escena["planos"]:
                contador += 1
                id_p = plano["id_plano"]
                prompt = plano["prompt"]
                ruta_img = f"assets/img/ep1_escena_{id_e}_p{id_p}.png"
                
                if not os.path.exists(ruta_img):
                    print(f"[{contador}/{total_planos}] ⚠️ {ruta_img} no existe en disco!")
                    continue
                    
                t0 = time.time()
                resultado = auditar_imagen_con_moondream(ruta_img, prompt)
                t_elapsed = time.time() - t0
                
                veredicto = resultado.get("verdict", "UNKNOWN")
                has_text = resultado.get("has_technical_text", False)
                
                item_reporte = {
                    "escena": id_e,
                    "plano": id_p,
                    "ruta": ruta_img,
                    "prompt": prompt,
                    "veredicto": veredicto,
                    "has_technical_text": has_text,
                    "moondream_detalle": resultado.get("output_raw", ""),
                    "tiempo_seg": round(t_elapsed, 2)
                }
                reporte.append(item_reporte)
                
                if veredicto == "FAIL" or has_text:
                    fallidas.append(item_reporte)
                    print(f"[{contador}/{total_planos}] ❌ ESCENA {id_e} PLANO {id_p}: FAIL ({t_elapsed:.1f}s)")
                    print(f"   Moondream: {resultado.get('output_raw', '')[:100]}...")
                else:
                    print(f"[{contador}/{total_planos}] ✅ ESCENA {id_e} PLANO {id_p}: PASS ({t_elapsed:.1f}s)")
                    
    finally:
        limpiar_entorno_remoto()
        
    # Guardar reporte localmente
    with open("reporte_auditoria_imagenes.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)
        
    print(f"\n==========================================")
    print(f"📊 RESUMEN AUDITORÍA MOONDREAM:")
    print(f"   Total evaluadas: {contador}")
    print(f"   Aprobadas (PASS): {contador - len(fallidas)}")
    print(f"   Con errores (FAIL): {len(fallidas)}")
    print(f"==========================================")
    
    if fallidas:
        print("\nImágenes que requieren regeneración:")
        for f in fallidas:
            print(f"- Escena {f['escena']} Plano {f['plano']}: {f['ruta']}")
            
if __name__ == "__main__":
    main()
