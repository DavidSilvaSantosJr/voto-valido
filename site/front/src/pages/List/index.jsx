import { Content } from "./style";

export default function List(){
  return (
    <Content>
      <header className="search-box">
        <select>          
          <option selected value="SP">SP</option>
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
      <table class="table table-hover table-bordered">
        <thead>
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Cidade</th>
            <th scope="col">Like</th>
            <th scope="col">Deslike</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">1</th>
            <td>Mark</td>
            <td>Otto</td>
            <td>@mdo</td>
          </tr>
          <tr>
            <th scope="row">2</th>
            <td>Jacob</td>
            <td>Thornton</td>
            <td>@fat</td>
          </tr>
          <tr>
            <th scope="row">2</th>
            <td>Jacob</td>
            <td>Thornton</td>
            <td>@fat</td>
          </tr>
        </tbody>
      </table>
    </Content>
  )
}