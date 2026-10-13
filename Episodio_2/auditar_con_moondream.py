import sys
import os
import glob

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(r"c:\Users\Lenovo\Documents\Animaciones\motor_animaciones")
from oracle_moondream_gate import OracleMoondreamGate

gate = OracleMoondreamGate()
images = sorted(glob.glob(r"c:\Users\Lenovo\Documents\Animaciones\Episodio_2\assets\img\*.png"))

print(f"🧐 Auditando {len(images)} imágenes con Moondream en Oracle VM...")

pregunta_qa = (
    "Analyze this image: "
    "1. Is there any garbled, misspelled, or hallucinated AI text/numbers? "
    "2. If a person is shown in bed or pajamas, do they incorrectly have outdoor shoes/sneakers or an outdoor vest on? "
    "3. Are there any distorted hands, clocks, or severe anatomical defects? "
    "Answer concisely: PASS or FAIL with a brief 1-sentence explanation."
)

for img in images:
    fname = os.path.basename(img)
    print(f"\n--- Auditando {fname} ---")
    resp = gate.consultar_moondream(img, pregunta_qa)
    print(f"Resultado Moondream: {resp}")

gate.limpiar_entorno()
