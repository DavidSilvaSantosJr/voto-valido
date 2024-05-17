import { ContentBanner } from "./style";

export default function Banner(){
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
        <div className="logo">
          Voto <span>Válido</span>
        </div>
        <div className="youtube">
          youtube
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