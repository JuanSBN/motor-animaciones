import React from "react";
import {
  Sequence,
  Audio,
  staticFile,
  useCurrentFrame,
  interpolate,
} from "remotion";
import { Scene } from "./Scene";
import data from "../../../Episodio_2/esquema_maestro_ep2.json";

export const MainVideoEp2: React.FC = () => {
  const frame = useCurrentFrame();
  const escena1 = data.escenas[0];
  const escena2 = data.escenas[1];
  const totalFrames = (escena1.duracion_frames || 1415) + (escena2.duracion_frames || 724);
  const baseVolume = 0.08;

  // Música de fondo documental suave con fade in
  const musicVolume = interpolate(
    frame,
    [0, 30, Math.max(0, totalFrames - 45), totalFrames],
    [0, baseVolume, baseVolume, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  return (
    <div style={{ flex: 1, backgroundColor: "#000" }}>
      {/* Música de fondo lo-fi documental */}
      {data.metadata.musica_fondo && (
        <Audio
          src={staticFile(data.metadata.musica_fondo)}
          volume={musicVolume}
        />
      )}

      {/* Escena 1: El Gran Vaciado Nocturno (Parte 1 - Dormitorio y Misterio) [0.0s -> 47.16s] */}
      <Sequence from={0} durationInFrames={escena1.duracion_frames}>
        <Scene scene={escena1 as any} episodeId={2} />
      </Sequence>

      {/* Escena 2: El Gran Vaciado Nocturno (Parte 2 - El Contraste y el Puente Prohibido) [47.16s -> 71.30s] */}
      <Sequence from={escena1.duracion_frames} durationInFrames={escena2.duracion_frames}>
        <Scene scene={escena2 as any} episodeId={2} />
      </Sequence>
    </div>
  );
};
