import React from "react";
import { useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";

export const BalanceScale: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animación de entrada suave
  const scaleEnter = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 90 },
  });

  // Movimiento oscilante sutil de la balanza para representar el equilibrio dinámico
  const tiltAngle = interpolate(
    Math.sin((frame / 22) * Math.PI),
    [-1, 1],
    [-2.5, 2.5]
  );

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle at 50% 50%, #1a1e2e 0%, #0a0c14 100%)",
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
          transform: `scale(${scaleEnter})`,
          zIndex: 2,
        }}
      >
        {/* Título de la infografía */}
        <div
          style={{
            fontSize: 34,
            fontWeight: 800,
            color: "#FBBF24",
            letterSpacing: "4px",
            textTransform: "uppercase",
            marginBottom: 35,
            textShadow: "0 0 20px rgba(251, 191, 36, 0.4)",
          }}
        >
          La Balanza Evolutiva Perfecta
        </div>

        {/* SVG de la Balanza */}
        <div style={{ position: "relative", width: 800, height: 460 }}>
          <svg width="800" height="460" viewBox="0 0 800 460">
            {/* Pilar central dorado */}
            <path
              d="M 390 100 L 410 100 L 418 390 L 382 390 Z"
              fill="#D97706"
              stroke="#F59E0B"
              strokeWidth="3"
            />
            {/* Base de la balanza */}
            <path
              d="M 330 390 C 330 375, 470 375, 470 390 L 510 420 L 290 420 Z"
              fill="#B45309"
              stroke="#F59E0B"
              strokeWidth="3"
            />
            {/* Remate superior */}
            <circle cx="400" cy="85" r="16" fill="#F59E0B" stroke="#FDE68A" strokeWidth="3" />

            {/* Barra oscilante transversal */}
            <g transform={`translate(400, 100) rotate(${tiltAngle})`}>
              <rect
                x="-320"
                y="-8"
                width="640"
                height="16"
                rx="8"
                fill="#F59E0B"
                stroke="#FDE68A"
                strokeWidth="2"
              />
              <circle cx="0" cy="0" r="12" fill="#D97706" />

              {/* Cadena izquierda */}
              <line x1="-280" y1="0" x2="-280" y2="120" stroke="#FBBF24" strokeWidth="3" />
              {/* Plato izquierdo */}
              <path
                d="M -360 120 C -360 170, -200 170, -200 120 Z"
                fill="rgba(217, 119, 6, 0.85)"
                stroke="#FBBF24"
                strokeWidth="3"
              />

              {/* Cadena derecha */}
              <line x1="280" y1="0" x2="280" y2="120" stroke="#FBBF24" strokeWidth="3" />
              {/* Plato derecho */}
              <path
                d="M 200 120 C 200 170, 360 170, 360 120 Z"
                fill="rgba(217, 119, 6, 0.85)"
                stroke="#FBBF24"
                strokeWidth="3"
              />
            </g>
          </svg>

          {/* Tarjeta / Escudo del Folato (Plato Izquierdo) */}
          <div
            style={{
              position: "absolute",
              top: 135,
              left: 45,
              width: 190,
              backgroundColor: "rgba(16, 185, 129, 0.95)",
              borderRadius: 16,
              padding: "16px 12px",
              boxShadow: "0 0 25px rgba(16, 185, 129, 0.5)",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              border: "2px solid #6EE7B7",
            }}
          >
            <div style={{ fontSize: 30 }}>🛡️</div>
            <div
              style={{
                fontSize: 20,
                fontWeight: 900,
                color: "#FFFFFF",
                letterSpacing: "1px",
                marginTop: 4,
              }}
            >
              FOLATO (B9)
            </div>
            <div
              style={{
                fontSize: 13,
                fontWeight: 700,
                color: "#D1FAE5",
                marginTop: 2,
                textAlign: "center",
              }}
            >
              Protegido por Melanina
            </div>
          </div>

          {/* Tarjeta / Cristal de la Vitamina D (Plato Derecho) */}
          <div
            style={{
              position: "absolute",
              top: 135,
              right: 45,
              width: 190,
              backgroundColor: "rgba(245, 158, 11, 0.95)",
              borderRadius: 16,
              padding: "16px 12px",
              boxShadow: "0 0 25px rgba(245, 158, 11, 0.5)",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              border: "2px solid #FDE68A",
            }}
          >
            <div style={{ fontSize: 30 }}>☀️</div>
            <div
              style={{
                fontSize: 20,
                fontWeight: 900,
                color: "#FFFFFF",
                letterSpacing: "1px",
                marginTop: 4,
              }}
            >
              VITAMINA D
            </div>
            <div
              style={{
                fontSize: 13,
                fontWeight: 700,
                color: "#FEF3C7",
                marginTop: 2,
                textAlign: "center",
              }}
            >
              Absorbida con Piel Clara
            </div>
          </div>
        </div>

        {/* Explicación inferior */}
        <div
          style={{
            marginTop: 10,
            background: "rgba(15, 23, 42, 0.8)",
            padding: "10px 28px",
            borderRadius: 20,
            border: "1px solid rgba(255, 255, 255, 0.12)",
            color: "#E2E8F0",
            fontSize: 18,
            fontWeight: 600,
          }}
        >
          Ecuador: Escudo contra UV ⇄ Polos: Ventana para sintetizar Vitamina D
        </div>
      </div>
    </div>
  );
};
