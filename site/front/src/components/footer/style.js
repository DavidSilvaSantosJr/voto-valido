import styled from "styled-components";
import Theme from "../../styles/theme";

export const FooterContent = styled.footer`

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  background-color: ${Theme.colors.blueLogo};
  height: 200px;  

  h1 {
    display: flex;
    flex-direction: column;
    align-items: center;
    color: ${Theme.colors.yellow};   
    
    span {
      font-weight: 800;
      font-size: 3rem;
    }
  }

  > span {
    color: white;
  }
`