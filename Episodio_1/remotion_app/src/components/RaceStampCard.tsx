import React from "react";
import { useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";

export const RaceStampCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animación del sello de impacto rojo (aparece en frame 18)
  const stampSpring = spring({
    frame: frame - 16,
    fps,
    config: { damping: 10, stiffness: 180, mass: 0.8 },
  });

  const stampScale = interpolate(stampSpring, [0, 1], [2.8, 1]);
  const stampOpacity = interpolate(frame, [14, 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Efecto de sutil sacudida al golpear el sello (frame 17 a 25)
  const shake = interpolate(frame, [17, 19, 21, 23, 25], [0, -6, 6, -3, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle at 50% 50%, #1e1e24 0%, #0d0d11 100%)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
        fontFamily: "'Segoe UI', -apple-system, Roboto, sans-serif",
        transform: `translateY(${shake}px)`,
      }}
    >
      {/* Tarjeta central limpia de divulgación científica */}
      <div
        style={{
          position: "relative",
          background: "rgba(255, 255, 255, 0.05)",
          border: "1px solid rgba(255, 255, 255, 0.12)",
          borderRadius: 24,
          padding: "60px 80px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          boxShadow: "0 20px 50px rgba(0, 0, 0, 0.5)",
          maxWidth: 900,
        }}
      >
        <div
          style={{
            fontSize: 22,
            letterSpacing: "6px",
            color: "#94A3B8",
            fontWeight: 700,
            textTransform: "uppercase",
            marginBottom: 16,
          }}
        >
          Consenso Científico Internacional
        </div>

        <div
          style={{
            fontSize: 56,
            fontWeight: 900,
            color: "#F8FAFC",
            letterSpacing: "1px",
            textTransform: "uppercase",
            position: "relative",
          }}
        >
          Razas Biológicas
        </div>

        {/* Sello de impacto rojo "NO EXISTEN" */}
        <div
          style={{
            position: "absolute",
            top: "38%",
            transform: `scale(${stampScale}) rotate(-12deg)`,
            opacity: stampOpacity,
            border: "6px solid #EF4444",
            borderRadius: 16,
            padding: "12px 36px",
            backgroundColor: "rgba(239, 68, 68, 0.12)",
            boxShadow: "0 0 35px rgba(239, 68, 68, 0.5)",
          }}
        >
          <div
            style={{
              fontSize: 52,
              fontWeight: 950,
              color: "#EF4444",
              letterSpacing: "4px",
              textTransform: "uppercase",
              textShadow: "0 0 20px rgba(239, 68, 68, 0.8)",
            }}
          >
            ✕ NO EXISTEN
          </div>
        </div>

        <div
          style={{
            marginTop: 40,
            color: "#CBD5E1",
            fontSize: 22,
            textAlign: "center",
            maxWidth: 680,
            lineHeight: 1.5,
          }}
        >
          La genética demostró que la humanidad es un continuo adaptativo, no categorías biológicas separadas.
        </div>
      </div>
    </div>
  );
};
