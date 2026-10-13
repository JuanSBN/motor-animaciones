import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface Palabra {
  w: string;
  s: number;
  e: number;
}

interface Grupo {
  palabras: Palabra[];
  s: number;
  e: number;
}

interface WordCaptionsProps {
  palabras?: Palabra[];
  textoFallback: string;
  fallbackStartFrame: number;
  fallbackTotalFrames: number;
  palabrasClave?: string[];
}

const MAX_PALABRAS = 4;
const MIN_PALABRAS_ANTES_DE_PUNTUACION = 2;
const SALTO_SILENCIO_SEG = 0.35;
const FONT_SIZE = 66;
const BOTTOM_SAFE = 150;

const normalizar = (t: string) =>
  t
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^\p{L}\p{N}]/gu, "");

export function agruparPalabras(palabras: Palabra[]): Grupo[] {
  const grupos: Grupo[] = [];
  let actual: Palabra[] = [];

  const cerrar = () => {
    if (actual.length === 0) return;
    grupos.push({ palabras: actual, s: actual[0].s, e: actual[actual.length - 1].e });
    actual = [];
  };

  palabras.forEach((p, i) => {
    const siguiente = palabras[i + 1];
    actual.push(p);
    const terminaFrase = /[.,;:!?…]$/.test(p.w.trim());
    const hayPausa = siguiente ? siguiente.s - p.e > SALTO_SILENCIO_SEG : true;
    if (
      actual.length >= MAX_PALABRAS ||
      hayPausa ||
      (terminaFrase && actual.length >= MIN_PALABRAS_ANTES_DE_PUNTUACION)
    ) {
      cerrar();
    }
  });
  cerrar();

  // Cada grupo permanece visible hasta que empieza el siguiente para evitar parpadeos.
  for (let i = 0; i < grupos.length - 1; i++) {
    grupos[i].e = Math.max(grupos[i].e, grupos[i + 1].s);
  }
  return grupos;
}

function palabrasDesdeTexto(texto: string, startSeg: number, durSeg: number): Palabra[] {
  const tokens = texto.split(/\s+/).filter(Boolean);
  const totalChars = tokens.reduce((acc, t) => acc + t.length, 0) || 1;
  let cursor = startSeg;
  return tokens.map((t) => {
    const d = (t.length / totalChars) * durSeg;
    const p = { w: t, s: cursor, e: cursor + d };
    cursor += d;
    return p;
  });
}

export const WordCaptions: React.FC<WordCaptionsProps> = ({
  palabras,
  textoFallback,
  fallbackStartFrame,
  fallbackTotalFrames,
  palabrasClave = [],
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  const fuente =
    palabras && palabras.length > 0
      ? palabras
      : palabrasDesdeTexto(textoFallback, fallbackStartFrame / fps, fallbackTotalFrames / fps);

  const grupos = agruparPalabras(fuente);
  const grupo = grupos.find((g) => t >= g.s && t < g.e);
  if (!grupo) return null;

  const clavesNorm = palabrasClave.flatMap((k) => k.split(/\s+/)).map(normalizar);
  const entradaFrame = frame - Math.round(grupo.s * fps);
  const pop = spring({ frame: entradaFrame, fps, config: { damping: 14, stiffness: 220 } });
  const escalaGrupo = interpolate(pop, [0, 1], [0.85, 1]);

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        bottom: BOTTOM_SAFE,
        display: "flex",
        justifyContent: "center",
        pointerEvents: "none",
        zIndex: 30,
      }}
    >
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: "0 18px",
          maxWidth: "80%",
          transform: `scale(${escalaGrupo})`,
          fontFamily: "'Montserrat', 'Arial Black', 'Segoe UI', sans-serif",
          fontWeight: 900,
          fontSize: FONT_SIZE,
          lineHeight: 1.15,
          textTransform: "uppercase",
          letterSpacing: 0.5,
        }}
      >
        {grupo.palabras.map((p, i) => {
          const activa = t >= p.s && t < p.e + 0.05;
          const esClave = clavesNorm.includes(normalizar(p.w));
          const color = activa ? "#FFE14D" : esClave ? "#FFB020" : "#FFFFFF";
          return (
            <span
              key={`${p.s}-${i}`}
              style={{
                color,
                WebkitTextStroke: "10px #0B0B12",
                paintOrder: "stroke fill",
                textShadow: "0 6px 0 rgba(0,0,0,0.55)",
                transform: `scale(${activa ? 1.08 : 1})`,
                display: "inline-block",
              }}
            >
              {p.w.trim()}
            </span>
          );
        })}
      </div>
    </div>
  );
};
