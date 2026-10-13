import React from "react";
import { Composition } from "remotion";
import { MainVideo } from "./Video";
import { VideoGenerico, duracionEsquema, Esquema } from "./VideoGenerico";
import data from "../../esquema_maestro.json";
import dataEp2 from "../../../Episodio_2/esquema_maestro_ep2_tight.json";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="VideoEpisodio"
        component={MainVideo}
        durationInFrames={data.metadata.duracion_total_frames || 473}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="Episodio2"
        component={VideoGenerico}
        defaultProps={{ esquema: dataEp2 as unknown as Esquema, episodeId: 2 }}
        durationInFrames={Math.max(1, duracionEsquema(dataEp2 as unknown as Esquema))}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
