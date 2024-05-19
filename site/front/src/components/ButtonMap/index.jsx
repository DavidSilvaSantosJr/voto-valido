import styled from "styled-components"
import Theme from "../../styles/theme"

const Button = styled.button`
  background-color: ${Theme.colors.yellow};
  border-radius: 10px;
  padding: .5rem 2.5rem;
  color: ${Theme.colors.blueLetters};
  font-weight: 600;
  font-size: 1.2rem;
  transition: linear all .2s;

  &:hover {
    background-color: ${Theme.colors.blueLogo};
    color: ${Theme.colors.yellow}
  }
`

export default function ButtonMap() {
  return (
    <Button>MAPA INTERATIVO</Button>
  )
}