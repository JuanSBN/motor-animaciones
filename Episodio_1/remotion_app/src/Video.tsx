import React from "react";
import {
  Sequence,
  Audio,
  staticFile,
  useCurrentFrame,
  interpolate,
} from "remotion";
import { Scene } from "./Scene";
import data from "../../esquema_maestro.json";

export const MainVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const totalFrames = data.metadata.duracion_total_frames || 5904;
  const baseVolume = data.metadata.volumen_musica || 0.1;

  // Fade in suave de música al inicio (1s) y fade out al final (1.5s)
  const musicVolume = interpolate(
    frame,
    [0, 30, Math.max(0, totalFrames - 45), totalFrames],
    [0, baseVolume, baseVolume, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // Precalcular offsets de tiempo para cada escena
  let accumulated = 0;
  const scenesWithOffsets = data.escenas.map((escena) => {
    const from = accumulated;
    accumulated += escena.duracion_frames;
    return { escena, from };
  });

  return (
    <div style={{ flex: 1, backgroundColor: "#000" }}>
      {/* Música de fondo documental con fade in/out */}
      {data.metadata.musica_fondo && (
        <Audio
          src={staticFile(data.metadata.musica_fondo)}
          volume={musicVolume}
        />
      )}

      {/* Escenas secuenciales sincronizadas */}
      {scenesWithOffsets.map(({ escena, from }) => (
        <Sequence
          key={escena.id}
          from={from}
          durationInFrames={escena.duracion_frames}
        >
          <Scene scene={escena} />
        </Sequence>
      ))}
    </div>
  );
};

