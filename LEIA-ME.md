# Escritório Eficaz · site

Site estático, sem dependências. Abra `index.html` no navegador ou publique a pasta inteira em qualquer hospedagem.

## Páginas
- `index.html` início: hero com vídeo, quem somos com fotos reais, seis cards de serviço (o último é "Muito mais"), vídeos, avaliações, além da contabilidade (BDMG, OAB, perícia), mapas. No celular, textos extras e a faixa de foto somem (classe `desk-only`)
- `sobre.html` história em três capítulos com fotos do acervo (assets/img/historia, vindas do protótipo do Márcio), números, foto da equipe, missão/visão/compromisso, responsáveis
- `servicos.html` cinco frentes de serviço com fotos, parcerias e passo a passo de abertura
- `depoimentos.html` avaliações públicas do Google (nota 5,0 em 32 avaliações)
- `links-uteis.html` (ferramentas da Ondatta primeiro, depois órgãos e portais), `contato.html`, `privacidade.html`
- `correspondente-caixa.html` redireciona para `servicos.html#parcerias` (o escritório não é mais Caixa Aqui)
- `empresa.html` redireciona para `sobre.html`; `noticias.html` redireciona para o início (notícias fixas foram removidas por não se atualizarem)

## Como editar
Cabeçalho, rodapé, dados de contato, vídeos (REELS) e avaliações (REVIEWS) ficam em `src/build.py`.
O conteúdo de cada página fica em `src/pages/`. Depois de editar, rode:

    python src/build.py

O script recusa textos com travessão. Ao mudar CSS ou JS, aumente `V` em `src/build.py` para limpar o cache.

## Mídia
- `assets/video/hero.mp4` (desktop) e `hero-m.mp4` (celular): montagem de clipes livres do Pexels (7821807, 7735903, 8425702, 7593891) com tratamento de cor.
- `assets/video/reel-N.mp4`: reels do @escritorioeficaz; `reel-N-prev.mp4` são as prévias curtas sem som.
- `assets/img/servicos/` e `assets/img/contabil/`: fotos livres do Pexels.
- `assets/img/historia/`: fotos reais do escritório (acervo e equipe atual) enviadas pelo cliente.

## Pendências
- Avaliações: o Google mostra só 3 completas sem login. Para incluir mais, copie de https://www.google.com/maps (ficha do escritório) para REVIEWS.
- Formulário abre o e-mail do visitante (mailto) ou o WhatsApp com a mensagem pronta.
- A agenda tributária saiu do site; o link atualizado fica em Links úteis (Ondatta).
- Botão "Acessar sistema" no topo: leva ao Portal do Cliente Onvio (Thomson Reuters), `EMPRESA["sistema"]` em `src/build.py`. Use `https://onvio.com.br/clientcenter/`, nunca o link da tela de login (tem token que expira).
