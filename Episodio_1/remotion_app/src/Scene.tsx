import React from "react";
import {
  Img,
  Audio,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";
import { DnaPieChart } from "./components/DnaPieChart";
import { ThermostatGauge } from "./components/ThermostatGauge";
import { RaceStampCard } from "./components/RaceStampCard";
import { SkinToneTimeline } from "./components/SkinToneTimeline";
import { BalanceScale } from "./components/BalanceScale";
import { KineticOverlay } from "./components/KineticOverlay";
import { SleepVoidTimeline } from "./components/SleepVoidTimeline";
import { WordCaptions, Palabra } from "./components/WordCaptions";

interface Plano {
  id_plano: number;
  imagen?: string;
  tipo_visual?: "imagen_flux" | "componente_vectorial";
  componente?: string;
  punch_in?: boolean;
  duracion_frames: number;
  animacion?: string;
  locucion_plano?: string;
  palabras_clave_plano?: string[];
  sfx?: "whoosh" | "ding" | "pop" | "ninguno";
}

export interface SfxConfig {
  whoosh?: string;
  ding?: string;
  pop?: string;
  volumen?: number;
}

const COMPONENT_REGISTRY: Record<string, React.FC> = {
  BalanceScale,
  DnaPieChart,
  ThermostatGauge,
  SkinToneTimeline,
  RaceStampCard,
  SleepVoidTimeline,
};

// Ningún encuadre debe quedarse más de ~3.5 s: los planos largos se parten en "beats" de cámara.
const BEAT_FRAMES = 105;
const UMBRAL_REENCUADRE = 135;
const KINETIC_SCALE = 1.7;

interface Encuadre {
  s0: number;
  s1: number;
  ox: number;
  oy: number;
  dx: number;
}

const ENCUADRES: Encuadre[] = [
  { s0: 1.0, s1: 1.06, ox: 50, oy: 50, dx: -14 },
  { s0: 1.22, s1: 1.28, ox: 35, oy: 40, dx: 18 },
  { s0: 1.12, s1: 1.18, ox: 65, oy: 45, dx: -18 },
  { s0: 1.3, s1: 1.36, ox: 50, oy: 35, dx: 0 },
];

interface SceneProps {
  episodeId?: number;
  sfx?: SfxConfig;
  scene: {
    id: number;
    locucion: string;
    palabras_clave?: string[];
    palabras?: Palabra[];
    archivos_generados: { audio_tts: string; imagen_flux?: string };
    duracion_frames: number;
    planos?: Plano[];
  };
}

interface PlanoActivo {
  plano?: Plano;
  inicio: number;
  frameEnPlano: number;
  total: number;
}

function resolverPlano(scene: SceneProps["scene"], frame: number): PlanoActivo {
  const planos = scene.planos ?? [];
  if (planos.length === 0) {
    return { inicio: 0, frameEnPlano: frame, total: scene.duracion_frames };
  }
  let acumulado = 0;
  for (const plano of planos) {
    const dur = plano.duracion_frames || Math.floor(scene.duracion_frames / planos.length);
    if (frame < acumulado + dur) {
      return { plano, inicio: acumulado, frameEnPlano: frame - acumulado, total: dur };
    }
    acumulado += dur;
  }
  const ultimo = planos[planos.length - 1];
  const dur = ultimo.duracion_frames || 30;
  return { plano: ultimo, inicio: acumulado - dur, frameEnPlano: frame - (acumulado - dur), total: dur };
}

function calcularCamara(animacion: string, frameEnPlano: number, total: number, idPlano: number, fps: number) {
  // Si el último beat quedaría por debajo de 1.5 s se fusiona con el anterior para evitar cortes bruscos.
  const numBeats = total > UMBRAL_REENCUADRE ? Math.max(1, Math.round(total / BEAT_FRAMES)) : 1;
  const beatLen = total / numBeats;
  const beatReal = Math.min(numBeats - 1, Math.floor(frameEnPlano / beatLen));
  const inicioReal = Math.round(beatReal * beatLen);
  const finReal = Math.round((beatReal + 1) * beatLen);

  const enc = ENCUADRES[(idPlano + beatReal) % ENCUADRES.length];
  const f = frameEnPlano - inicioReal;
  const len = Math.max(1, finReal - inicioReal);

  let scale = interpolate(f, [0, len], [enc.s0, enc.s1], {
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.quad),
  });
  let tx = interpolate(f, [0, len], [0, enc.dx], { extrapolateRight: "clamp" });
  let ty = 0;
  let rot = 0;

  if (animacion === "paneo_suave") {
    scale = Math.max(scale, 1.08);
    tx = interpolate(f, [0, len], [enc.dx >= 0 ? -30 : 30, enc.dx >= 0 ? 30 : -30], {
      extrapolateRight: "clamp",
    });
  } else if (animacion === "flotar_suave") {
    ty = Math.sin((frameEnPlano / fps) * Math.PI) * 8;
  } else if (animacion === "sacudida") {
    const decay = interpolate(frameEnPlano, [0, 18], [1, 0], { extrapolateRight: "clamp" });
    tx += Math.sin(frameEnPlano * 2.3) * 22 * decay;
    ty += Math.cos(frameEnPlano * 2.9) * 14 * decay;
    rot = Math.sin(frameEnPlano * 1.7) * 1.4 * decay;
    scale = Math.max(scale, 1.06);
  }

  // Punch-in de entrada: los primeros frames del plano arrancan un 4 % más cerca y se asientan.
  const settle = interpolate(f, [0, 8], [0.04, 0], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  return {
    transform: `translate(${tx}px, ${ty}px) rotate(${rot}deg) scale(${scale + settle})`,
    transformOrigin: `${enc.ox}% ${enc.oy}%`,
  };
}

export const Scene: React.FC<SceneProps> = ({ scene, episodeId = 1, sfx }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { plano, inicio, frameEnPlano, total } = resolverPlano(scene, frame);

  const idPlano = plano?.id_plano ?? 1;
  const imagen = plano?.imagen || scene.archivos_generados.imagen_flux || "";
  const animacion = plano?.animacion || "zoom_in_suave";
  const camara = calcularCamara(animacion, frameEnPlano, total, idPlano, fps);

  const renderVisual = () => {
    if (plano?.componente && COMPONENT_REGISTRY[plano.componente]) {
      const Componente = COMPONENT_REGISTRY[plano.componente];
      return <Componente />;
    }
    if (!imagen) return null;
    return (
      <div style={{ position: "absolute", inset: 0, overflow: "hidden" }}>
        <Img
          src={staticFile(imagen)}
          style={{ width: "100%", height: "100%", objectFit: "cover", ...camara }}
        />
      </div>
    );
  };

  const volumenSfx = sfx?.volumen ?? 0.35;
  const sfxPorPlano = (p: Plano, i: number) => {
    const tipo = p.sfx ?? (i === 0 ? "ninguno" : p.animacion === "sacudida" ? "pop" : "whoosh");
    if (tipo === "ninguno") return null;
    return sfx?.[tipo] ?? null;
  };

  let cursor = 0;
  const cortes = (scene.planos ?? []).map((p, i) => {
    const desde = cursor;
    cursor += p.duracion_frames;
    const archivo = sfxPorPlano(p, i);
    if (!archivo) return null;
    // El whoosh arranca 4 frames antes del corte para que el pico caiga justo en el cambio de imagen.
    return (
      <Sequence key={`sfx-${p.id_plano}`} from={Math.max(0, desde - 4)} durationInFrames={30}>
        <Audio src={staticFile(archivo)} volume={volumenSfx} />
      </Sequence>
    );
  });

  return (
    <div style={{ width: "100%", height: "100%", backgroundColor: "#0A0A0A", overflow: "hidden", position: "relative" }}>
      <Audio src={staticFile(scene.archivos_generados.audio_tts)} />
      {cortes}

      {renderVisual()}

      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `scale(${KINETIC_SCALE})`,
          transformOrigin: "top left",
          pointerEvents: "none",
          zIndex: 20,
        }}
      >
        <KineticOverlay
          episodeId={episodeId}
          sceneId={scene.id}
          planoId={idPlano}
          shotFrame={frameEnPlano}
          shotTotalFrames={total}
        />
      </div>

      <WordCaptions
        palabras={scene.palabras}
        textoFallback={plano?.locucion_plano || scene.locucion}
        fallbackStartFrame={inicio}
        fallbackTotalFrames={total}
        palabrasClave={plano?.palabras_clave_plano || scene.palabras_clave || []}
      />
    </div>
  );
};
