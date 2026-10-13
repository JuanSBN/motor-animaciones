import React from "react";
import { useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";

export const SleepVoidTimeline: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animación suave de entrada de la línea
  const progress = interpolate(frame, [0, 60], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Pulso del vacío central
  const pulseScale = interpolate(
    Math.sin((frame / 12) * Math.PI),
    [-1, 1],
    [0.96, 1.05]
  );

  // Flotación de signos de interrogación
  const qFloat1 = Math.sin((frame / 15) * Math.PI) * 8;
  const qFloat2 = Math.cos((frame / 18) * Math.PI) * 10;
  const qFloat3 = Math.sin((frame / 12) * Math.PI + 1) * 7;

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle at 50% 50%, #111827 0%, #030712 100%)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
        fontFamily: "'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif",
        overflow: "hidden",
      }}
    >
      {/* Fondo de partículas / estrellas sutiles */}
      <div style={{ position: "absolute", inset: 0, opacity: 0.2, pointerEvents: "none" }}>
        {[...Array(24)].map((_, i) => (
          <div
            key={i}
            style={{
              position: "absolute",
              left: `${(i * 37) % 100}%`,
              top: `${(i * 23) % 100}%`,
              width: (i % 3) + 2,
              height: (i % 3) + 2,
              borderRadius: "50%",
              backgroundColor: "#FFF",
              opacity: (i % 5) * 0.2 + 0.3,
            }}
          />
        ))}
      </div>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          maxWidth: 1200,
          width: "90%",
          zIndex: 2,
        }}
      >
        {/* Título de la infografía */}
        <div
          style={{
            fontSize: 32,
            fontWeight: 800,
            color: "#60A5FA",
            letterSpacing: "4px",
            textTransform: "uppercase",
            marginBottom: 60,
            textShadow: "0 0 20px rgba(96, 165, 250, 0.5)",
          }}
        >
          REGISTRO NOCTURNO DE LA CONCIENCIA
        </div>

        {/* Contenedor de la línea temporal */}
        <div
          style={{
            position: "relative",
            width: "100%",
            height: 180,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          {/* Línea base conectora */}
          <div
            style={{
              position: "absolute",
              top: "50%",
              left: 80,
              right: 80,
              height: 4,
              backgroundColor: "rgba(255, 255, 255, 0.15)",
              transform: "translateY(-50%)",
              borderRadius: 2,
            }}
          />

          {/* Línea animada de gradiente */}
          <div
            style={{
              position: "absolute",
              top: "50%",
              left: 80,
              width: `${(progress / 100) * 84}%`,
              height: 4,
              background: "linear-gradient(90deg, #3B82F6, #EC4899, #F59E0B)",
              transform: "translateY(-50%)",
              borderRadius: 2,
              boxShadow: "0 0 16px rgba(236, 72, 153, 0.7)",
            }}
          />

          {/* Nodo 1: 11:30 PM (Inicio del Sueño) */}
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              zIndex: 3,
            }}
          >
            <div
              style={{
                width: 70,
                height: 70,
                borderRadius: "50%",
                background: "linear-gradient(135deg, #1E3A8A, #3B82F6)",
                border: "3px solid #60A5FA",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 32,
                boxShadow: "0 0 25px rgba(59, 130, 246, 0.6)",
              }}
            >
              🌙
            </div>
            <div
              style={{
                marginTop: 14,
                fontSize: 24,
                fontWeight: 800,
                color: "#FFFFFF",
              }}
            >
              11:30 PM
            </div>
            <div
              style={{
                fontSize: 14,
                color: "#93C5FD",
                fontWeight: 600,
                textTransform: "uppercase",
              }}
            >
              Último Recuerdo
            </div>
          </div>

          {/* NODO CENTRAL: EL VACÍO ABSOLUTO (PORTAL NEGRO) */}
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              transform: `scale(${pulseScale})`,
              zIndex: 4,
            }}
          >
            <div
              style={{
                width: 140,
                height: 140,
                borderRadius: "50%",
                background: "radial-gradient(circle, #000000 60%, #1F1F38 90%, #A855F7 100%)",
                border: "3px dashed #C084FC",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                boxShadow: "0 0 40px rgba(168, 85, 247, 0.8), inset 0 0 30px #000000",
                position: "relative",
              }}
            >
              {/* Partículas de interrogación flotando */}
              <div
                style={{
                  position: "absolute",
                  top: -24 + qFloat1,
                  left: -12,
                  fontSize: 28,
                  fontWeight: 900,
                  color: "#FBBF24",
                  textShadow: "0 0 10px rgba(251, 191, 36, 0.8)",
                }}
              >
                ?
              </div>
              <div
                style={{
                  position: "absolute",
                  top: -30 + qFloat2,
                  right: -10,
                  fontSize: 32,
                  fontWeight: 900,
                  color: "#38BDF8",
                  textShadow: "0 0 10px rgba(56, 189, 248, 0.8)",
                }}
              >
                ?
              </div>
              <div
                style={{
                  position: "absolute",
                  bottom: -20 + qFloat3,
                  left: 55,
                  fontSize: 26,
                  fontWeight: 900,
                  color: "#EC4899",
                  textShadow: "0 0 10px rgba(236, 72, 153, 0.8)",
                }}
              >
                ?
              </div>

              <div
                style={{
                  fontSize: 16,
                  fontWeight: 900,
                  color: "#E9D5FF",
                  letterSpacing: "2px",
                  textAlign: "center",
                  lineHeight: 1.2,
                }}
              >
                VACÍO<br />ABSOLUTO
              </div>
            </div>

            <div
              style={{
                marginTop: 14,
                backgroundColor: "rgba(168, 85, 247, 0.2)",
                border: "1px solid #A855F7",
                borderRadius: 20,
                padding: "4px 14px",
                fontSize: 13,
                fontWeight: 700,
                color: "#F3E8FF",
                letterSpacing: "1px",
              }}
            >
              CERO GRABACIÓN
            </div>
          </div>

          {/* Nodo 2: 07:00 AM (El Despertar) */}
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              zIndex: 3,
            }}
          >
            <div
              style={{
                width: 70,
                height: 70,
                borderRadius: "50%",
                background: "linear-gradient(135deg, #D97706, #F59E0B)",
                border: "3px solid #FCD34D",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 32,
                boxShadow: "0 0 25px rgba(245, 158, 11, 0.6)",
              }}
            >
              ☀️
            </div>
            <div
              style={{
                marginTop: 14,
                fontSize: 24,
                fontWeight: 800,
                color: "#FFFFFF",
              }}
            >
              07:00 AM
            </div>
            <div
              style={{
                fontSize: 14,
                color: "#FDE68A",
                fontWeight: 600,
                textTransform: "uppercase",
              }}
            >
              Alarma / Despertar
            </div>
          </div>
        </div>

        {/* Resumen científico al pie */}
        <div
          style={{
            marginTop: 40,
            fontSize: 18,
            color: "#9CA3AF",
            backgroundColor: "rgba(255, 255, 255, 0.05)",
            padding: "10px 24px",
            borderRadius: 30,
            border: "1px solid rgba(255, 255, 255, 0.1)",
          }}
        >
          ⏱️ <span style={{ color: "#FBBF24", fontWeight: 700 }}>8 horas de noche</span> convertidas en <span style={{ color: "#F43F5E", fontWeight: 700 }}>0 segundos de recuerdo</span>
        </div>
      </div>
    </div>
  );
};
