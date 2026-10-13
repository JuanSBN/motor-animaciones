import React from "react";
import { Audio, Series, staticFile, useCurrentFrame, interpolate } from "remotion";
import { Scene, SfxConfig } from "./Scene";

export interface Esquema {
  metadata: {
    musica_fondo?: string;
    volumen_musica?: number;
    sfx?: SfxConfig;
  };
  escenas: React.ComponentProps<typeof Scene>["scene"][];
}

const escenasListas = (esquema: Esquema) =>
  esquema.escenas.filter((e) => e.archivos_generados?.audio_tts && e.duracion_frames > 0);

export const duracionEsquema = (esquema: Esquema) =>
  escenasListas(esquema).reduce((acc, e) => acc + e.duracion_frames, 0);

export const VideoGenerico: React.FC<{ esquema: Esquema; episodeId: number }> = ({ esquema, episodeId }) => {
  const frame = useCurrentFrame();
  const total = duracionEsquema(esquema);
  const base = esquema.metadata.volumen_musica ?? 0.08;
  const volumenMusica = interpolate(frame, [0, 30, Math.max(31, total - 45), total], [0, base, base, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div style={{ flex: 1, backgroundColor: "#000" }}>
      {esquema.metadata.musica_fondo && (
        <Audio src={staticFile(esquema.metadata.musica_fondo)} volume={volumenMusica} loop />
      )}
      <Series>
        {escenasListas(esquema).map((escena) => (
          <Series.Sequence key={escena.id} durationInFrames={escena.duracion_frames}>
            <Scene scene={escena} episodeId={episodeId} sfx={esquema.metadata.sfx} />
          </Series.Sequence>
        ))}
      </Series>
    </div>
  );
};
