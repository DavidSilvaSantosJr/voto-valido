import { Content } from "./style";

export default function Home(){
  return (
    <Content>
      <header className="search-box">
        <select>
          <option selected></option>
          <option value="SP">SP</option>
          <option value="PR">PR</option>
          <option value="MG">MG</option>
        </select>
        <div className="search">
          <input type="text" placeholder="Cidade" id="city"/>
          <span>
            <img />
          </span>
        </div>
      </header>
    </Content>
  )
}