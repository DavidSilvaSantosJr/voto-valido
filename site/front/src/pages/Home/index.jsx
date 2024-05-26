import Banner from "../../components/Banner";
import Footer from "../../components/footer";
import { ContentHome } from "./style";

import ButtonMap from "../../components/ButtonMap";
import votoSocial from "../../assets/voto-redesocial.png";
import votoCompleto from "../../assets/voto_completo.png"
import icon1 from "../../assets/icon1.webp"
import icon2 from "../../assets/icon2.webp"
import icon3 from "../../assets/icon3.webp"

export default function Home() {
  return (
    <ContentHome>
      <Banner/>
      <div className="register">
        <p>Cadastre-se gratuitamente para começar a usar o</p> 
        <span>VOTO VÁLIDO</span>
      </div>
      <section className="cards">
        <div className="card">
          <div className="img"><img src={icon1} alt="Transparência" /></div>
          <h1>TRANSPARÊNCIA</h1>
          <p>Tenha acesso direto às informações sobre o que está acontecendo na sua cidade.</p>
        </div>
        <div className="card">
          <div className="img"><img src={icon2} alt="Projeto Moderno" /></div>
          <h1>PROJETO MODERNO</h1>
          <p>Contribua para o debate público compartilhando suas próprias observações e experiências.</p>          
        </div>
        <div className="card">
          <div className="img"><img src={icon3} alt="Comunicação" /></div>
          <h1>COMUNICAÇÃO</h1>
          <p>Atualizações em tempo real sobre projetos governamentais na sua região</p>          
        </div>
      </section>
      <section className="events">
        <h1>VOTO VÁLIDO</h1>
        <article>
          <h1>Acontecimentos</h1>
          <ul>
            <li>Construção de Escolas ou Creches</li>
            <li>Manutenção de Ruas e Calçadas</li>
            <li>Instalação ou Reparo de Iluminação Pública</li>
            <li>Reformas em Praças e Parques</li>
            <li>Eventos Culturais e Esportivos na Comunidade</li>
            <li>Construção ou Ampliação de Ciclovias</li>
            <li>Projetos de Revitalização</li>
          </ul>
        </article>
        <ButtonMap/>
      </section>
      <section className="shortly">
        <div className="title">
          <h1>EM BREVE</h1>
          <h2>MUITO MAIS QUE UMA PLATAFORMA</h2>
        </div>
        <div className="content">
          <div className="img"><img src={votoSocial} alt="Logo Voto Válido"/></div>
          <div className="text">
            <p>Nosso objetivo é tornar o VOTO VÁLIDO uma rede social sobre acontecimentos nas cidades.</p>
            <p>Participe ativamente da discussão sobre os acontecimentos na sua cidade! Comente, compartilhe suas opiniões e interaja com outros membros da comunidade. Seu feedback é importante para construirmos juntos um ambiente urbano melhor.</p>
          </div>
        </div>
      </section>
      <section className="about">
        <div className="logo">
          <img src={votoCompleto} alt="Voto Válido"/>
        </div>
        <p>VOTO VÁLIDO é mais do que uma plataforma, é uma comunidade online que capacita os cidadãos a se envolverem ativamente na vida urbana. Uma rede social onde você pode não apenas compartilhar fotos dos acontecimentos na sua cidade, mas também discutir e influenciar os eventos que moldam ela.</p>
        <p>Nosso objetivo é promover a transparência, a participação cívica e a responsabilidade governamental, capacitando os moradores a se tornarem agentes de mudança positiva em suas comunidades.</p>
        <ButtonMap/>
      </section>
      <Footer/>
    </ContentHome>
  )
}