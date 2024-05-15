import styled from 'styled-components'

export const Content = styled.main`
  width: 60vw;
  
  .search-box {
    display: flex;
    justify-content: center;
    width: 100%;

    select {
      height: 3rem;
      width: 3rem;
    }

    .search {
      input {
        height: 3rem;
        width: 300px;
        border: 1px solid #ccc;
        border-radius: 25px;
        padding: 1rem;
        transition: ease-in all .2s;
        
        &:focus{
        border: 3px solid blue;
      }
      }

      
    }
  }
`