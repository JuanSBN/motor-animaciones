import React from "react";
import { useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";

interface KineticOverlayProps {
  sceneId: number;
  planoId?: number;
  shotFrame: number;
  shotTotalFrames: number;
}

const BADGES: Record<string, { icon: string; title: string; subtitle: string; color: string }> = {
  "1_1": {
    icon: "☀️",
    title: "SABANA AFRICANA",
    subtitle: "Radiación solar extrema hace millones de años",
    color: "#F59E0B",
  },
  "2_1": {
    icon: "🏃",
    title: "TERMORREGULACIÓN",
    subtitle: "Pérdida de pelaje para sudar y no sobrecalentarse",
    color: "#38BDF8",
  },
  "3_1": {
    icon: "⚡",
    title: "RADIACIÓN ULTRAVIOLETA",
    subtitle: "Rayos UV dañinos penetrando la piel expuesta",
    color: "#A855F7",
  },
  "3_2": {
    icon: "🧬",
    title: "FOLATO (VITAMINA B9)",
    subtitle: "Molécula vital destruida por la luz solar intensa",
    color: "#EC4899",
  },
  "4_2": {
    icon: "🛡️",
    title: "MELANINA NATURAL",
    subtitle: "Escudo fotoprotector biológico definitivo",
    color: "#10B981",
  },
  "6_1": {
    icon: "🌍",
    title: "MIGRACIÓN HUMANA",
    subtitle: "Hace 60.000 años hacia nuevos continentes",
    color: "#3B82F6",
  },
  "7_2": {
    icon: "❄️",
    title: "CLIMA NÓRDICO",
    subtitle: "Menos horas de sol y menor índice UV",
    color: "#67E8F9",
  },
  "8_1": {
    icon: "🦴",
    title: "SÍNTESIS DE VITAMINA D",
    subtitle: "Imprescindible para fijar el calcio en los huesos",
    color: "#FBBF24",
  },
  "9_1": {
    icon: "⚠️",
    title: "DILEMA ADAPTATIVO",
    subtitle: "La piel muy oscura bloqueaba el escaso sol del norte",
    color: "#F97316",
  },
  "10_1": {
    icon: "🧬",
    title: "SELECCIÓN NATURAL",
    subtitle: "Individuos de piel clara producían más vitamina D",
    color: "#10B981",
  },
  "11_1": {
    icon: "⏳",
    title: "GRADIENTE EVOLUTIVO",
    subtitle: "Ajuste milenario según la latitud geográfica",
    color: "#F59E0B",
  },
  "13_1": {
    icon: "🧩",
    title: "CORRELACIÓN PERFECTA",
    subtitle: "Radiación UV y tono de piel coinciden exactamente",
    color: "#38BDF8",
  },
  "14_1": {
    icon: "⚖️",
    title: "BALANZA BIOLÓGICA",
    subtitle: "Equilibrio crítico: Proteger Folato vs. Sintetizar Vitamina D",
    color: "#FBBF24",
  },
  "15_2": {
    icon: "🐟",
    title: "EXCEPCIÓN INUIT",
    subtitle: "Dieta marina ártica colmada de Vitamina D natural",
    color: "#06B6D4",
  },
  "17_2": {
    icon: "🧬",
    title: "UNIDAD GENÉTICA",
    subtitle: "Mayor diversidad dentro de un grupo que entre poblaciones",
    color: "#A78BFA",
  },
  "18_1": {
    icon: "🏙️",
    title: "VIDA MODERNA",
    subtitle: "El 90% del tiempo transcurre bajo techos y luz artificial",
    color: "#64748B",
  },
  "18_2": {
    icon: "✈️",
    title: "VUELOS INTERCONTINENTALES",
    subtitle: "Viajamos en horas lo que tomó milenios adaptar",
    color: "#38BDF8",
  },
  "19_2": {
    icon: "✨",
    title: "UN MAPA VIVO",
    subtitle: "El legado solar de tus antepasados en tu piel",
    color: "#FBBF24",
  },
};

const EP2_BADGES: Record<string, { icon: string; title: string; subtitle: string; color: string }> = {
  "1_1": {
    icon: "🌙",
    title: "EL MISTERIO NOCTURNO",
    subtitle: "¿Por qué olvidamos el momento exacto de dormir?",
    color: "#60A5FA",
  },
  "1_4": {
    icon: "⏱️",
    title: "ATENCIÓN CONSCIENTE",
    subtitle: "El intento humano de cazar el sueño despierto",
    color: "#FBBF24",
  },
  "1_8": {
    icon: "⏰",
    title: "EL SALTO TEMPORAL",
    subtitle: "8 horas transcurridas en un solo parpadeo",
    color: "#F43F5E",
  },
  "1_10": {
    icon: "🕳️",
    title: "VACÍO DE MEMORIA",
    subtitle: "Desconexión biológica total del hipocampo",
    color: "#A855F7",
  },
  "1_13": {
    icon: "🔒",
    title: "BLOQUEO NEURONAL",
    subtitle: "Orden evolutiva de borrado consciente cada noche",
    color: "#EF4444",
  },
  "2_1": {
    icon: "🤕",
    title: "MEMORIA DE IMPACTO",
    subtitle: "El cerebro registra caídas y peligros al instante",
    color: "#F59E0B",
  },
  "2_3": {
    icon: "🗄️",
    title: "ARCHIVO DE SUPERVIVENCIA",
    subtitle: "El cerebro graba peligros y errores indeleblemente",
    color: "#F59E0B",
  },
  "2_4": {
    icon: "🌉",
    title: "EL PUENTE NEURONAL",
    subtitle: "La frontera biológica entre vigilia e inconsciencia",
    color: "#8B5CF6",
  },
  "2_5": {
    icon: "🚫",
    title: "ZONA RESTRINGIDA",
    subtitle: "Un recuerdo biológicamente prohibido por la evolución",
    color: "#EF4444",
  },
};

interface KineticOverlayProps {
  episodeId?: number;
  sceneId: number;
  planoId?: number;
  shotFrame: number;
  shotTotalFrames: number;
}

export const KineticOverlay: React.FC<KineticOverlayProps> = ({
  episodeId = 1,
  sceneId,
  planoId = 1,
  shotFrame,
  shotTotalFrames,
}) => {
  const { fps } = useVideoConfig();
  const key = `${sceneId}_${planoId}`;
  const badge = episodeId === 2 ? EP2_BADGES[key] : BADGES[key];

  if (!badge) return null;

  // Entrada en frame 12, permanece 70 frames, luego sale
  const enterStart = 12;
  const exitStart = Math.min(shotTotalFrames - 20, 85);

  const entrance = spring({
    frame: shotFrame - enterStart,
    fps,
    config: { damping: 14, stiffness: 120 },
  });

  const exitOpacity = interpolate(
    shotFrame,
    [exitStart, exitStart + 15],
    [1, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  const scale = interpolate(entrance, [0, 1], [0.85, 1]);
  const translateY = interpolate(entrance, [0, 1], [-25, 0]);
  const opacity = Math.min(
    interpolate(shotFrame, [enterStart, enterStart + 8], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }),
    exitOpacity
  );

  if (opacity <= 0) return null;

  return (
    <div
      style={{
        position: "absolute",
        top: 48,
        left: 56,
        display: "flex",
        alignItems: "center",
        gap: 16,
        backgroundColor: "rgba(10, 15, 29, 0.82)",
        backdropFilter: "blur(12px)",
        border: `1.5px solid ${badge.color}`,
        borderRadius: 20,
        padding: "12px 26px 12px 20px",
        boxShadow: `0 8px 32px rgba(0, 0, 0, 0.55), 0 0 15px ${badge.color}40`,
        transform: `translateY(${translateY}px) scale(${scale})`,
        opacity,
        zIndex: 10,
        fontFamily: "'Segoe UI', Roboto, sans-serif",
      }}
    >
      <div
        style={{
          fontSize: 32,
          lineHeight: 1,
          filter: `drop-shadow(0 0 8px ${badge.color})`,
        }}
      >
        {badge.icon}
      </div>
      <div style={{ display: "flex", flexDirection: "column" }}>
        <div
          style={{
            fontSize: 16,
            fontWeight: 900,
            color: badge.color,
            letterSpacing: "2px",
            textTransform: "uppercase",
          }}
        >
          {badge.title}
        </div>
        <div
          style={{
            fontSize: 14,
            fontWeight: 500,
            color: "#E2E8F0",
            marginTop: 2,
            maxWidth: 380,
          }}
        >
          {badge.subtitle}
        </div>
      </div>
    </div>
  );
};
