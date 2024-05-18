import styled from "styled-components";
import Theme from "../../styles/theme";

export const ContentHome = styled.main`
  .register {
    background-color: #ccc;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 150px;

    font-weight: 800;
    font-size: 1.75rem;

    color: ${Theme.colors.blueLetters};

    p {
      font: inherit;
    }

    span {        
      font-weight: 800;
      font-size: 1.75rem;
      color: ${Theme.colors.blueLetters};
    }
  }
`