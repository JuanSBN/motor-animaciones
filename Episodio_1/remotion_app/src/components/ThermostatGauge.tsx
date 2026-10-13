import React from "react";
import { useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";

export const ThermostatGauge: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrada suave del dial
  const enterScale = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 85 },
  });

  // Movimiento de la aguja: oscila y se calibra según la narración
  // Ángulo de -60 grados (Ecuador / alta radiación) a +60 grados (Polos / baja radiación)
  const needleAngle = interpolate(
    frame,
    [10, 45, 90, 140],
    [-55, 45, -20, 15],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle at 50% 50%, #1e1b2e 0%, #0c0a14 100%)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
        fontFamily: "'Segoe UI', -apple-system, Roboto, sans-serif",
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          transform: `scale(${enterScale})`,
          zIndex: 2,
        }}
      >
        {/* Título superior */}
        <div
          style={{
            fontSize: 34,
            fontWeight: 800,
            color: "#FBBF24",
            letterSpacing: "4px",
            textTransform: "uppercase",
            marginBottom: 24,
            textShadow: "0 0 20px rgba(251, 191, 36, 0.4)",
          }}
        >
          Termostato de Radiación Solar
        </div>

        {/* Indicador de cuadrante */}
        <div
          style={{
            position: "relative",
            width: 520,
            height: 320,
            background: "rgba(30, 27, 46, 0.8)",
            border: "2px solid rgba(251, 191, 36, 0.25)",
            borderRadius: "260px 260px 20px 20px",
            boxShadow: "0 15px 35px rgba(0, 0, 0, 0.6)",
            display: "flex",
            justifyContent: "center",
            paddingTop: 30,
            overflow: "hidden",
          }}
        >
          {/* Arco del cuadrante */}
          <svg width="440" height="240" viewBox="0 0 440 240">
            <defs>
              <linearGradient id="arcGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#D97706" />
                <stop offset="50%" stopColor="#F59E0B" />
                <stop offset="100%" stopColor="#38BDF8" />
              </linearGradient>
            </defs>

            {/* Arco de fondo */}
            <path
              d="M 60 210 A 160 160 0 0 1 380 210"
              fill="none"
              stroke="#332d4a"
              strokeWidth="24"
              strokeLinecap="round"
            />
            {/* Arco degradado coloreado */}
            <path
              d="M 60 210 A 160 160 0 0 1 380 210"
              fill="none"
              stroke="url(#arcGrad)"
              strokeWidth="16"
              strokeLinecap="round"
              strokeDasharray="4 8"
            />

            {/* Aguja dinámica */}
            <g transform={`translate(220, 210) rotate(${needleAngle})`}>
              <line
                x1="0"
                y1="0"
                x2="0"
                y2="-150"
                stroke="#EF4444"
                strokeWidth="6"
                strokeLinecap="round"
                filter="drop-shadow(0 0 8px rgba(239, 68, 68, 0.8))"
              />
              <circle cx="0" cy="0" r="16" fill="#EF4444" />
              <circle cx="0" cy="0" r="8" fill="#FFFFFF" />
            </g>
          </svg>

          {/* Etiquetas en los extremos */}
          <div
            style={{
              position: "absolute",
              bottom: 25,
              left: 45,
              color: "#F59E0B",
              fontSize: 18,
              fontWeight: 800,
              display: "flex",
              flexDirection: "column",
              alignItems: "flex-start",
            }}
          >
            <span>☀️ ECUADOR</span>
            <span style={{ fontSize: 13, color: "#9CA3AF", fontWeight: 600 }}>Melanina Alta</span>
          </div>

          <div
            style={{
              position: "absolute",
              bottom: 25,
              right: 45,
              color: "#38BDF8",
              fontSize: 18,
              fontWeight: 800,
              display: "flex",
              flexDirection: "column",
              alignItems: "flex-end",
            }}
          >
            <span>❄️ POLOS</span>
            <span style={{ fontSize: 13, color: "#9CA3AF", fontWeight: 600 }}>Melanina Baja</span>
          </div>
        </div>

        {/* Subtítulo aclaratorio */}
        <div
          style={{
            marginTop: 22,
            color: "#E2E8F0",
            fontSize: 20,
            fontWeight: 600,
            backgroundColor: "rgba(15, 23, 42, 0.7)",
            padding: "8px 22px",
            borderRadius: 20,
            border: "1px solid rgba(255, 255, 255, 0.1)",
          }}
        >
          Calibrado por la luz solar y la geografía
        </div>
      </div>
    </div>
  );
};
