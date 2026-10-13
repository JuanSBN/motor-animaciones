const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const outDir = path.join(__dirname, 'remotion_app', 'out', 'qa_frames');
if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

const videoPath = path.join(__dirname, 'remotion_app', 'out', 'episodio_1_completo_ink_v3.mp4');

const shots = [
  { t: '00:00:05', name: 'scene1' },
  { t: '00:01:47', name: 'scene11_tones' },
  { t: '00:01:58', name: 'scene12_thermostat' },
  { t: '00:02:13', name: 'scene13_p2_niko_map' },
  { t: '00:02:21', name: 'scene14_p1_scale' },
  { t: '00:02:31', name: 'scene15_p1_inuit' },
  { t: '00:02:47', name: 'scene16_p2_dna' },
  { t: '00:02:54', name: 'scene17_p1_stamp' },
  { t: '00:03:20', name: 'scene19_cierre' }
];

shots.forEach(s => {
  const outFile = path.join(outDir, s.name + '.png');
  const cmd = `ffmpeg -ss ${s.t} -i "${videoPath}" -vframes 1 -q:v 2 -y "${outFile}"`;
  execSync(cmd, { stdio: 'inherit' });
  console.log('Extracted ' + s.name);
});
