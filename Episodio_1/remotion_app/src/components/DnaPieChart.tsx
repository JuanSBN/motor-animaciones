import React from "react";
import { useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";

export const DnaPieChart: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animación del porcentaje (de 0.0% a 99.9%)
  const percentageProgress = interpolate(frame, [10, 45], [0, 99.9], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Animación del arco circular SVG
  const circleRadius = 180;
  const circumference = 2 * Math.PI * circleRadius;
  const strokeOffset = interpolate(
    frame,
    [10, 45],
    [circumference, circumference * (1 - 0.999)],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // Entrada con spring suave
  const cardScale = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 90 },
  });

  // Pop-in del detalle 0.1% a partir del frame 48
  const detailOpacity = interpolate(frame, [45, 60], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const detailTranslate = interpolate(frame, [45, 60], [30, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Sutil flotación y brillo de fondo
  const pulse = interpolate(Math.sin((frame / 20) * Math.PI), [-1, 1], [0.98, 1.02]);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle at 50% 45%, #131d33 0%, #070a12 100%)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Segoe UI', -apple-system, Roboto, sans-serif",
      }}
    >
      {/* Luces y partículas ambientales */}
      <div
        style={{
          position: "absolute",
          width: 600,
          height: 600,
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(14, 165, 233, 0.15) 0%, transparent 70%)",
          filter: "blur(40px)",
          transform: `scale(${pulse})`,
        }}
      />

      {/* Contenedor principal con spring */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 70,
          transform: `scale(${cardScale})`,
          zIndex: 2,
        }}
      >
        {/* Gráfico circular de Donut */}
        <div style={{ position: "relative", width: 440, height: 440 }}>
          <svg width="440" height="440" style={{ transform: "rotate(-90deg)" }}>
            {/* Círculo de fondo (el 0.1% restante / base) */}
            <circle
              cx="220"
              cy="220"
              r={circleRadius}
              stroke="#F59E0B"
              strokeWidth="28"
              fill="transparent"
              opacity="0.8"
            />
            {/* Círculo animado del 99.9% */}
            <circle
              cx="220"
              cy="220"
              r={circleRadius}
              stroke="#06B6D4"
              strokeWidth="28"
              fill="transparent"
              strokeDasharray={circumference}
              strokeDashoffset={strokeOffset}
              strokeLinecap="round"
              style={{
                filter: "drop-shadow(0 0 16px rgba(6, 182, 212, 0.6))",
              }}
            />
          </svg>

          {/* Contador y texto central */}
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <div
              style={{
                fontSize: 68,
                fontWeight: 900,
                color: "#38BDF8",
                letterSpacing: "-2px",
                lineHeight: 1,
                textShadow: "0 0 24px rgba(56, 189, 248, 0.5)",
              }}
            >
              {percentageProgress.toFixed(1)}%
            </div>
            <div
              style={{
                fontSize: 18,
                fontWeight: 700,
                color: "#E2E8F0",
                letterSpacing: "3px",
                marginTop: 8,
                textTransform: "uppercase",
              }}
            >
              ADN Idéntico
            </div>
          </div>
        </div>

        {/* Panel lateral de datos explicativos */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 22,
            maxWidth: 520,
          }}
        >
          {/* Tarjeta 1: 99.9% */}
          <div
            style={{
              background: "rgba(15, 23, 42, 0.8)",
              border: "1px solid rgba(56, 189, 248, 0.35)",
              borderRadius: 16,
              padding: "18px 24px",
              boxShadow: "0 10px 25px rgba(0,0,0,0.4)",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <div
                style={{
                  width: 14,
                  height: 14,
                  borderRadius: "50%",
                  backgroundColor: "#06B6D4",
                  boxShadow: "0 0 10px #06B6D4",
                }}
              />
              <span style={{ color: "#38BDF8", fontWeight: 800, fontSize: 20 }}>
                99.9% Genoma Humano Compartido
              </span>
            </div>
            <p style={{ color: "#94A3B8", fontSize: 16, margin: "8px 0 0 26px", lineHeight: 1.4 }}>
              Todo ser humano en el planeta comparte la casi totalidad de su código genético fundamental.
            </p>
          </div>

          {/* Tarjeta 2: 0.1% */}
          <div
            style={{
              background: "rgba(15, 23, 42, 0.8)",
              border: "1px solid rgba(245, 158, 11, 0.35)",
              borderRadius: 16,
              padding: "18px 24px",
              boxShadow: "0 10px 25px rgba(0,0,0,0.4)",
              opacity: detailOpacity,
              transform: `translateY(${detailTranslate}px)`,
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <div
                style={{
                  width: 14,
                  height: 14,
                  borderRadius: "50%",
                  backgroundColor: "#F59E0B",
                  boxShadow: "0 0 10px #F59E0B",
                }}
              />
              <span style={{ color: "#FBBF24", fontWeight: 800, fontSize: 20 }}>
                0.1% Variación Superficial
              </span>
            </div>
            <p style={{ color: "#CBD5E1", fontSize: 16, margin: "8px 0 0 26px", lineHeight: 1.4 }}>
              Apenas un puñado de genes regula el tono de piel y rasgos externos: simples adaptaciones climáticas.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
