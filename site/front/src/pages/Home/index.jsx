import Banner from "../../components/Banner";
import Footer from "../../components/footer";
import { ContentHome } from "./style";

export default function Home() {
  return (
    <ContentHome>
      <Banner/>
      <div className="register">
        <p>Cadastre-se gratuitamente para começar a usar o VOTO VÁLIDO</p>
      </div>
      <Footer/>
    </ContentHome>
  )
}