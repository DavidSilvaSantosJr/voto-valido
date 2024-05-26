import styled from "styled-components";
import Theme from "../../styles/theme";

import bloco2 from "../../assets/bloco2.jpg"
import bloco3 from "../../assets/bloco3.webp"

export const ContentHome = styled.main`
  .register {
    background-color: #fafafa;
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

  .cards {
    display: flex;

    .card {      
      
      display: flex;
      flex-direction: column;
      justify-content: space-evenly;
      align-items: center;
      gap: 1rem;

      padding: 5rem 0 3rem 0;

      border: none;

      cursor: pointer;
      
      transition: linear all .2s;

      &:hover {
        transform: scale(1.1);
      }

      .img {
        img {
          width: 7.5rem;
        }
      }

      h1 {
        font-size: 1.2rem;
        font-weight: 600;
        color: ${Theme.colors.blueLetters};
      }

      p {
        text-align: center;
        font-size: .8rem;
        line-height: 1.5rem;

        max-width: 80%;
      }
    }
  }

  .events {
    background-image: url(${bloco2});
    background-position: center;
    background-size: cover;

    padding: 5rem 0;

    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
    gap: 2rem;

    > h1 {
      color: ${Theme.colors.yellow};
      font-weight: 800;  
      font-size: 3rem;
    }

    article {
      display: flex;
      flex-direction: column;
      align-items: center;  
      cursor: pointer;    

      h1 {
        color: ${Theme.colors.blueLogo};  
        font-weight: 600;
        font-size: 1.5rem;
      }

      ul {
        list-style: none;
        margin: 0;
        padding: 0;

        li {
          text-align: center; 
          font-size: .8rem;          
          transition: linear all .2s;
          color: ${Theme.colors.blueLetters};
          
          &:hover {
            transform: scale(1.1);
          }          
        }
      }
    }
  }

  .shortly {
    margin-top: 50px;
    padding: 0 100px;

    .title {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-transform: uppercase;
      color: ${Theme.colors.blueLogo};      

      h1 {
        font-weight: 700;  
        font-size: 2rem;
      }

      h2 {
        font-weight: 500;  
        font-size: 1.5rem;
      }
    }

    .content {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 2rem;

      .img {
        img {
          width: 200px;
        }
      }

      .text {
        color: ${Theme.colors.blueLetters};
        max-width: 700px;

        p {
          font-size: .9rem;
          line-height: 1.75rem;
          text-align: justify;
        }
      }
    }

    
  }

  .about {
    padding-bottom: 50px;
    display: flex;
    flex-direction: column;
    align-items: center;

    background-image: url(${bloco3});
    background-position: center;
    background-size: cover;

    .logo {      
      img {
        width: 300px;
      }
    }

    p {
      text-align: center;
      max-width: 700px;
      font-size: .9rem;
      color: ${Theme.colors.blueLetters};
      line-height: 1.75rem;
    }
  }
`