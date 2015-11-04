# obsxingu: um protótipo de ferramenta de acesso a TUDO
O observatório Xingu é um aplicativo que pretende usar diferentes tecnologias para fornecer uma forma simples de monitorar o território da bacia do Xingu, utilizando as ferramentas Earth Engine da Google para calcular e mostrar em tempo real mosaicos processados de imagens de satélite.

O sistema se compõe de dois elementos fundamentais:

## Sistema agregador de informação espacial (webmapping mashup)
Programado _from scratch_ em [Leaflet](http://leafletjs.com/), uma libraria javascript de uso simples mas muito potente e popular. O Leaflet possui varios plugins de interesse, como o [ESRI Leaflet](http://esri.github.io/esri-leaflet/), que permite manipular camadas de geoserviços ESRI.

O mashup integra (ou pretende integrar) diversas fontes de informação:
[x] Camadas WMS: focos de calor FIRMS
[x] Camadas rest/WFS: informação de focos de calor, unidades de conservação, etc.
[ ] Features vindas de fusion tables: aldeias, localidades ribeirinhas, etc.
[x] Tiles vindos de Earth Engine (ver mais embaixo)

Adicionalmente, o uso do plugin [Draw](https://github.com/Leaflet/Leaflet.draw) permite ao usuário desenhar pontos, linhas e polígonos, para dar destaque a feições encontradas na sua navegação.

## Sistema de renderizado de imagens de satélite
Mediante uma complexa interação facilitada pelas librarias webapp2 (que permite controlar a resposta às requisições dos navegadores) e jinja2 (que permite o uso de _templates_ nos arquivos html), é possível rodar um script python no servidor Google Earth Engine (seria o script _server.py_) e ter acesso aos _tiles_ gerados programáticamente pelo script.
Existem duas peças chaves no sistema de geração de imagens:

### o algoritmo de geração de imagens: server.py
O algoritmo, contido no arquivo _server.py_ e outros auxiliares, permite calcular uma imagen _média_ Landsat para uma série de anos (especificada no começo do script), tirando nuvens e sombras de nuvens mediante a seleção dos pixels mais 'limpos' em cada pixel mostrado na tela. Esse algoritmo é executado de forma ultrarápida nos servidores Earth Engine da Google, sendo que o usuário não sente o onus do cálculo, só recebe _tiles_ que vão conformar um mosaico limpo.
Naturalmente, o algoritmo pode ser modificado para abranger mais ou menos datas e para realizar outro tipo de cálculos. Também podem ser modificados os limiares de limpeza de nuvens e sombras.

### A autenticação do aplicativo
Obsxingu usa um sistema de autenticação chamado _service account_, que permite que o navegador possa ter acesso sem autenticação ao Google Earth Engine, sem precisar uma autorização, que na verdade é dada, _a priori_, à própria aplicação. Para mais detalhes, ver https://github.com/google/earthengine-api/tree/master/demos/server-auth.

Para instruções de uso e instalação, contatar juan@socioambiental.org




