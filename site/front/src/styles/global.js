import { createGlobalStyle } from 'styled-components';

export default createGlobalStyle`
  * {
  
    font-family: "Archivo", sans-serif;    
    font-weight: 300;
    font-style: normal;
    font-variation-settings: "wdth" 100;

    margin: 0;
    padding: 0px;
    outline: 0;
    box-sizing: border-box;
    border: none;
  }

  .flex {
    display: flex;
  }
`