import React from "react";
import { Composition } from "remotion";
import { MainVideo } from "./Video";
import { MainVideoEp2 } from "./VideoEp2";
import data from "../../esquema_maestro.json";
import dataEp2 from "../../../Episodio_2/esquema_maestro_ep2.json";

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
        id="Episodio2Preview"
        component={MainVideoEp2}
        durationInFrames={
          (dataEp2.escenas[0].duracion_frames || 1415) +
          (dataEp2.escenas[1]?.duracion_frames || 724)
        }
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
