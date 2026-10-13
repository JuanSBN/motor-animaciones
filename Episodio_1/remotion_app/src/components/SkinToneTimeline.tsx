import React from "react";
import { useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";

export const SkinToneTimeline: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const tones = [
    {
      tone: "#2B1704",
      label: "Ecuador (0°)",
      sub: "Melanina Máxima",
      icon: "☀️☀️☀️",
    },
    {
      tone: "#5C381E",
      label: "Trópicos (20°)",
      sub: "Protección Alta",
      icon: "☀️☀️",
    },
    {
      tone: "#A5734C",
      label: "Lat. Media (40°)",
      sub: "Equilibrio",
      icon: "⛅",
    },
    {
      tone: "#D8A882",
      label: "Norte (55°)",
      sub: "Piel Clara",
      icon: "❄️",
    },
    {
      tone: "#F7D6B8",
      label: "Ártico (70°)",
      sub: "Máxima Absorción UV",
      icon: "❄️❄️",
    },
  ];

  const lineProgress = interpolate(frame, [5, 45], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle at 50% 50%, #1e2230 0%, #0d0f18 100%)",
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
          maxWidth: 1200,
          width: "90%",
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
            marginBottom: 50,
            textShadow: "0 0 20px rgba(251, 191, 36, 0.4)",
          }}
        >
          Gradiente Evolutivo de Pigmentación
        </div>

        {/* Contenedor del eje horizontal */}
        <div
          style={{
            position: "relative",
            width: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "0 40px",
          }}
        >
          {/* Línea horizontal conectora */}
          <div
            style={{
              position: "absolute",
              top: 55,
              left: 80,
              right: 80,
              height: 6,
              background: "rgba(255, 255, 255, 0.15)",
              borderRadius: 3,
              zIndex: 1,
            }}
          >
            <div
              style={{
                width: `${lineProgress}%`,
                height: "100%",
                background: "linear-gradient(90deg, #F59E0B 0%, #38BDF8 100%)",
                borderRadius: 3,
                boxShadow: "0 0 10px rgba(56, 189, 248, 0.6)",
              }}
            />
          </div>

          {/* Círculos de tonos y etiquetas */}
          {tones.map((t, idx) => {
            const circleSpring = spring({
              frame: frame - (10 + idx * 7),
              fps,
              config: { damping: 12, stiffness: 100 },
            });
            const scale = interpolate(circleSpring, [0, 1], [0.3, 1]);
            const opacity = interpolate(circleSpring, [0, 1], [0, 1]);

            return (
              <div
                key={idx}
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  zIndex: 2,
                  transform: `scale(${scale})`,
                  opacity,
                }}
              >
                {/* Etiqueta superior de latitud */}
                <div
                  style={{
                    fontSize: 16,
                    fontWeight: 700,
                    color: "#94A3B8",
                    marginBottom: 14,
                    letterSpacing: "1px",
                  }}
                >
                  {t.label}
                </div>

                {/* Círculo de color de piel */}
                <div
                  style={{
                    width: 100,
                    height: 100,
                    borderRadius: "50%",
                    backgroundColor: t.tone,
                    border: "4px solid #FFFFFF",
                    boxShadow: "0 8px 24px rgba(0, 0, 0, 0.5)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 24,
                  }}
                >
                  <span>{t.icon}</span>
                </div>

                {/* Subtítulo inferior explicativo */}
                <div
                  style={{
                    marginTop: 18,
                    fontSize: 15,
                    fontWeight: 700,
                    color: "#E2E8F0",
                    textAlign: "center",
                    maxWidth: 130,
                  }}
                >
                  {t.sub}
                </div>
              </div>
            );
          })}
        </div>

        {/* Nota explicativa inferior */}
        <div
          style={{
            marginTop: 60,
            background: "rgba(15, 23, 42, 0.7)",
            padding: "10px 28px",
            borderRadius: 20,
            border: "1px solid rgba(255, 255, 255, 0.1)",
            color: "#CBD5E1",
            fontSize: 18,
            fontWeight: 600,
          }}
        >
          A menor radiación UV, menor cantidad de melanina para permitir la absorción de luz
        </div>
      </div>
    </div>
  );
};
