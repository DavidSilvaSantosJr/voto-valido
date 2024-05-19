import { ContentBanner } from "./style";

export default function Banner(){
  const videoId = 'bP8bI0RcrmM';
  const url = `https://www.youtube.com/embed/${videoId}`
  return(
    <ContentBanner className="">
      <header className="flex">
        <a className="img-logo" href="#">
          <img src="src\assets\voto1.png" alt="Voto válido"/>
        </a>
        <div className="btn">
          <button>Mapa interativo</button>
        </div>
      </header>
      <div className="informations flex">
        <h1 className="logo">
          <span>Voto </span>
          <span>Válido</span>
        </h1>
        <div className="youtube">
        <iframe
          width="500"
          height="250"
          src={url}
          title="YouTube video"
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        ></iframe>
        </div>
      </div>
      <div className="text">
        <span>
          Nossa plataforma inovadora conecta os cidadãos à realidade da sua cidade. Permitimos que você compartilhe e acesse informações sobre eventos, obras, e outras atividades importantes que impactam a sua vida diária.
        </span>
      </div>
    </ContentBanner>
  )
}