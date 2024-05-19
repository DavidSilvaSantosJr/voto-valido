import styled from "styled-components";
import Theme from '../../styles/theme';

import bloco1 from '../../assets/bloco1.webp';

export const ContentBanner = styled.div`
  background-image: url(${bloco1});

  padding: 0 10rem 2rem 10rem;  

  header {
    width: 100%;
    justify-content: space-between;
    align-items: center;

    a {
      text-decoration: none;

      img {
      width: 200px;
      }
    }

    .btn {
      button {
        background-color: ${Theme.colors.yellow};
        width: 10rem;
        height: 30px;
        color: white;
        border-radius: 20px;
      }
    }
  }

  .informations {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .logo {
      color: ${Theme.colors.yellow};
      font-size: 5rem;            

      display: flex;
      flex-direction: column;
      align-items: center;

      span {
        font-weight: 800;
      }
    }
  }

  .text {
    max-width: 50vw;
    margin-top: 1rem;
    span {
      color: white;
      font-size: 1.25rem;
      line-height: 2rem;
    }
  }
`