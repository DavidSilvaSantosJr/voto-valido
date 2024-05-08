VOTO VÁLIDO

- uma ferramnenta poderosa para entender a gestão da cidade, sem viéses, sem manipuilação de mídia, sem medo de expor sua visão e realidade da cidade.
- envie o problema, local e descrição dele através do BOT no telegram. Após isso, consuilte a plataforma para ver como anda a cidade.

  entre em contato com o Vêve, bot oficial do voto válido e siga as instruções.
  
  o bot funciona recebendo mensagens e sendo tratadasd através dem decorradores, quando um decorador possui o "filtro" da mensagem, a função cabível é executada.
  as informações são enviadas para o banco de dados por um json,  que contém:
  - localização:
    - pode ser recebida via compartilhamento de localizaçao: captura a latitude e longitude, apos usa essas informações para capturar o estado e cidadem através da API do google maps
    - envio manual: caso o usuário esteja fora do local com problema, é possivel enviar o endereço da localização. O enderço é consultado na API do google maps,  se valiado como correto pelo usúario, é salvo da mesma forma que a anterior.
  - imagem: salva o caminho para API do telegram, e id do usúario, que passa por um filtro antes de ser salvo.
  - dscrição: breve texto contendo infomrações sobre o problema, que passa por um filtro antes de ser salvo.
