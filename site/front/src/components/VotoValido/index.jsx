import styled from "styled-components"

import Theme from "../../styles/theme";

const Voto = styled.h1`
  h1 {
    display: flex;
    flex-direction: column;
    align-items: center;
    color: ${Theme.colors.yellow};
  }
`

export default function VotoValido(){
  return(
    <Voto>
      <span>Voto</span> 
      <span>Válido</span>
    </Voto>
  )
}