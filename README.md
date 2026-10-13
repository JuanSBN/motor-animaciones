# 🎬 Motor de Animaciones Divulgativas (Ink Explainer)

Pipeline integral automatizado para la creación de videos de divulgación científica en formato 2D (*Ink Explainer / Kurzgesagt / Curiosamente*), combinando inteligencia artificial generativa, síntesis de voz, sincronización fonética por Whisper y renderizado programático con Remotion (React + SVG).

---

## 🚀 Características Principales

- **Locución Oficial Unificada:** Gemini TTS 3.1 Flash (`Puck`) con filtrado acústico a 48 kHz y eliminación de ruidos parásitos.
- **Forced Alignment con Whisper:** Sincronización milimétrica palabra por palabra y corte de plano a nivel de fotograma.
- **Enrutador Visual Híbrido:**
  - **Componentes Vectoriales React / SVG:** Líneas temporales, indicadores, gráficos de ADN y balanzas biológicas sin artefactos de IA.
  - **Ilustraciones 2D (FLUX.2 Klein 4B en Modal):** Escenarios ricos, fondos y personajes coherentes generados en la nube sobre GPUs A100.
- **Control de Calidad (Moondream VLM + OpenCV):** Auditoría visual automática para detectar distorsiones y post-procesamiento quirúrgico.
- **Renderizado Programático:** Remotion Studio Full HD (1920×1080) a 30 fps con subtítulos dinámicos e insignias kinéticas.

---

## 📂 Estructura del Repositorio

```text
├── motor_animaciones/               # Módulos centrales reutilizables
│   ├── pipeline_maestro.py          # Orquestador principal
│   ├── pacing_semantic_splitter.py  # Algoritmo de ritmo (2.5s - 5.0s por plano)
│   ├── visual_classifier.py         # Enrutador inteligente (SVG vs FLUX)
│   └── oracle_moondream_gate.py     # Auditor de calidad visual
│
├── Episodio_1/                      # Episodio: "¿Por qué tenemos diferentes colores de piel?"
│   └── remotion_app/                # Entorno React/Remotion compartido
│       ├── src/                     # Código fuente de animación y componentes
│       └── public/assets/           # Assets visuales y acústicos montados
│
├── Episodio_2/                      # Episodio: "¿Por qué no recuerdas cuándo te quedas dormido?"
│   ├── esquema_maestro_ep2.json     # Estructura declarativa completa del episodio
│   ├── assets/                      # Audios e ilustraciones finales
│   └── scripts/                     # Scripts de generación y alineamiento
│
├── DOCUMENTACION_SISTEMA_ANIMACIONES.md # Documentación técnica completa
└── .gitignore                       # Filtros de exclusión de binarios pesados
```

---

## 🛠️ Requisitos e Instalación

### Requisitos Previos
- **Node.js** v18+ y npm
- **Python** 3.10+
- **FFmpeg** instalado en el PATH
- Cuenta de **Modal** configurada (`modal setup`) para aceleración de inferencia GPU

### Instalación de Dependencias de Renderizado
```bash
cd Episodio_1/remotion_app
npm install
```

### Previsualización y Renderizado
```bash
# Abrir Remotion Studio para previsualización interactiva
npm run start

# Renderizar un episodio o preview
npx remotion render Episodio2Preview out/ep2_preview.mp4 --concurrency=4
```

---

## 📖 Documentación Completa
Para una guía técnica detallada sobre la arquitectura de 5 capas, reglas de pacing y estándares de producción, consulta [DOCUMENTACION_SISTEMA_ANIMACIONES.md](./DOCUMENTACION_SISTEMA_ANIMACIONES.md).
