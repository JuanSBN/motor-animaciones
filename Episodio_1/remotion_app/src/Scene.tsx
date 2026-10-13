import React from "react";
import {
  Img,
  Audio,
  staticFile,
  useCurrentFrame,
  interpolate,
} from "remotion";
import { DnaPieChart } from "./components/DnaPieChart";
import { ThermostatGauge } from "./components/ThermostatGauge";
import { RaceStampCard } from "./components/RaceStampCard";
import { SkinToneTimeline } from "./components/SkinToneTimeline";
import { BalanceScale } from "./components/BalanceScale";
import { KineticOverlay } from "./components/KineticOverlay";
import { SleepVoidTimeline } from "./components/SleepVoidTimeline";

interface Plano {
  id_plano: number;
  imagen?: string;
  tipo_visual?: "imagen_flux" | "componente_vectorial";
  componente?: string;
  punch_in?: boolean;
  duracion_frames: number;
  animacion?: string;
  prompt?: string;
  locucion_plano?: string;
  palabras_clave_plano?: string[];
}

// Registro dinámico de infografías científicas vectoriales
const COMPONENT_REGISTRY: Record<string, React.FC> = {
  BalanceScale,
  DnaPieChart,
  ThermostatGauge,
  SkinToneTimeline,
  RaceStampCard,
  SleepVoidTimeline,
};

interface SceneProps {
  episodeId?: number;
  scene: {
    id: number;
    acto?: number;
    locucion: string;
    palabras_clave?: string[];
    archivos_generados: {
      audio_tts: string;
      imagen_flux?: string;
    };
    duracion_frames: number;
    planos?: Plano[];
  };
}

export const Scene: React.FC<SceneProps> = ({ scene, episodeId = 1 }) => {
  const frame = useCurrentFrame();

  // Selección dinámica de plano actual
  let activeImage = scene.archivos_generados.imagen_flux || "";
  let activePlanoId = 1;
  let shotFrame = frame;
  let shotTotalFrames = scene.duracion_frames;
  let animationType = "zoom_in_suave";
  let activePlanoObj: Plano | undefined;

  if (scene.planos && scene.planos.length > 0) {
    let accumulated = 0;
    for (const plano of scene.planos) {
      const pDur = plano.duracion_frames || Math.floor(scene.duracion_frames / scene.planos.length);
      if (frame >= accumulated && frame < accumulated + pDur) {
        activeImage = plano.imagen || "";
        activePlanoId = plano.id_plano;
        activePlanoObj = plano;
        shotFrame = frame - accumulated;
        shotTotalFrames = pDur;
        animationType = plano.animacion || "zoom_in_suave";
        break;
      }
      accumulated += pDur;
    }
    if (!activePlanoObj && scene.planos.length > 0) {
      const last = scene.planos[scene.planos.length - 1];
      activeImage = last.imagen || "";
      activePlanoId = last.id_plano;
      activePlanoObj = last;
      shotFrame = Math.max(0, frame - (accumulated - (last.duracion_frames || 30)));
      shotTotalFrames = last.duracion_frames || 30;
      animationType = last.animacion || "zoom_in_suave";
    }
  }

  // --- MOVIMIENTO DE CÁMARA DINÁMICO Y EQUILIBRADO ---
  let scale = 1.0;
  let translateX = 0;

  const isLongShot = shotTotalFrames > 165; // Más de 5.5s
  const punchBoost = (activePlanoObj?.punch_in || isLongShot)
    ? interpolate(shotFrame, [Math.floor(shotTotalFrames * 0.45), Math.floor(shotTotalFrames * 0.45) + 10], [0, 0.07], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      })
    : 0;

  if (animationType === "paneo_suave") {
    scale = 1.06 + punchBoost;
    translateX = interpolate(shotFrame, [0, Math.max(1, shotTotalFrames)], [0, -28], {
      extrapolateRight: "clamp",
    });
  } else if (animationType === "flotar_suave") {
    scale = interpolate(Math.sin((shotFrame / 30) * Math.PI), [-1, 1], [1.02, 1.06]) + punchBoost;
  } else {
    // Zoom in continuo y cinematográfico con refuerzo dinámico para planos largos
    scale = interpolate(shotFrame, [0, Math.max(1, shotTotalFrames)], [1.0, 1.07], {
      extrapolateRight: "clamp",
    }) + punchBoost;
    translateX = interpolate(shotFrame, [0, Math.max(1, shotTotalFrames)], [0, -14], {
      extrapolateRight: "clamp",
    });
  }

  const audioSrc = staticFile(scene.archivos_generados.audio_tts);
  const imageSrc = activeImage ? staticFile(activeImage) : "";

  // Renderizado del contenido visual principal
  const renderVisualContent = () => {
    // 1. Registro declarativo dinámico (para nuevos episodios automáticos)
    if (activePlanoObj?.componente && COMPONENT_REGISTRY[activePlanoObj.componente]) {
      const DynamicComponent = COMPONENT_REGISTRY[activePlanoObj.componente];
      return <DynamicComponent />;
    }

    // 2. Fallback de compatibilidad retroactiva por IDs
    if (scene.id === 11 && activePlanoId === 1) {
      return <SkinToneTimeline />;
    }
    if (scene.id === 16 && activePlanoId === 2) {
      return <DnaPieChart />;
    }
    if (scene.id === 12 && activePlanoId === 1) {
      return <ThermostatGauge />;
    }
    if (scene.id === 14 && activePlanoId === 1) {
      return <BalanceScale />;
    }
    if (scene.id === 17 && activePlanoId === 1) {
      return <RaceStampCard />;
    }

    // Ilustración FLUX 2D limpia con cámara cinemática continua
    return (
      <div
        style={{
          width: "100%",
          height: "100%",
          position: "absolute",
          inset: 0,
        }}
      >
        <Img
          src={imageSrc}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: `scale(${scale}) translateX(${translateX}px)`,
          }}
        />
      </div>
    );
  };

  // Subtítulo dinámico sincronizado por plano
  const renderSubtitle = () => {
    const text = activePlanoObj?.locucion_plano || scene.locucion;
    const keywords = activePlanoObj?.palabras_clave_plano || scene.palabras_clave || [];
    if (!keywords || keywords.length === 0) return text;

    const sortedKeywords = [...keywords].sort((a, b) => b.length - a.length);
    const escaped = sortedKeywords.map((k) =>
      k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
    );
    const regex = new RegExp(`(${escaped.join("|")})`, "gi");

    const parts = text.split(regex);
    return parts.map((part, i) => {
      const isMatch = sortedKeywords.some(
        (k) => k.toLowerCase() === part.toLowerCase()
      );
      if (isMatch) {
        return (
          <span
            key={i}
            style={{
              color: "#FBBF24",
              fontWeight: 800,
              textShadow: "0 0 12px rgba(251, 191, 36, 0.4)",
            }}
          >
            {part}
          </span>
        );
      }
      return part;
    });
  };

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#0A0A0A",
        overflow: "hidden",
        position: "relative",
      }}
    >
      {/* Audio oficial unificado de Gemini TTS Puck */}
      <Audio src={audioSrc} />

      {/* Contenido visual principal (Motion Graphics nativos o Ilustración FLUX) */}
      {renderVisualContent()}

      {/* Insignia kinética explicativa superior */}
      <KineticOverlay
        episodeId={episodeId}
        sceneId={scene.id}
        planoId={activePlanoId}
        shotFrame={shotFrame}
        shotTotalFrames={shotTotalFrames}
      />

      {/* Subtítulo dinámico por plano, corto, nítido y perfectamente sincronizado */}
      <div
        style={{
          position: "absolute",
          bottom: 40,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          pointerEvents: "none",
          zIndex: 20,
        }}
      >
        <div
          style={{
            backgroundColor: "rgba(10, 10, 16, 0.85)",
            backdropFilter: "blur(10px)",
            padding: "12px 32px",
            borderRadius: 16,
            border: "1px solid rgba(255, 255, 255, 0.16)",
            color: "#F8FAFC",
            fontSize: 26,
            fontWeight: 700,
            fontFamily: "'Segoe UI', Roboto, sans-serif",
            textAlign: "center",
            maxWidth: "76%",
            lineHeight: 1.35,
            boxShadow: "0 8px 25px rgba(0, 0, 0, 0.6)",
          }}
        >
          {renderSubtitle()}
        </div>
      </div>
    </div>
  );
};
