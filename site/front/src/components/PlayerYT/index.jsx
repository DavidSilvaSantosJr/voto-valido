import YouTube from 'react-youtube';

export default function PlayerYT() {
  const videoId = 'bP8bI0RcrmM';
  return (
    <YouTube videoId={videoId} />
  );
};