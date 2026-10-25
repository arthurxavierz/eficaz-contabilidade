# Escritório Eficaz · site

Site estático, sem dependências. Abra `index.html` no navegador ou publique a pasta inteira em qualquer hospedagem.

## Páginas
- `index.html` início: hero com vídeo, números, serviços empilhados, vídeos do Instagram, avaliações, agenda tributária, dicas
- `sobre.html` história, equipe (fotos tiradas dos reels), trajetória, visão, missão, responsáveis
- `servicos.html` cinco frentes de serviço com fotos, parcerias e passo a passo de abertura
- `depoimentos.html` avaliações públicas do Google (nota 5,0 em 32 avaliações)
- `correspondente-caixa.html`, `links-uteis.html`, `contato.html`, `privacidade.html`
- `empresa.html` redireciona para `sobre.html`; `noticias.html` redireciona para o início (notícias fixas foram removidas por não se atualizarem)

## Como editar
Cabeçalho, rodapé, dados de contato, vídeos (REELS), posts do Instagram (IG_POSTS) e avaliações (REVIEWS) ficam em `src/build.py`.
O conteúdo de cada página fica em `src/pages/`. Depois de editar, rode:

    python src/build.py

O script recusa textos com travessão. Ao mudar CSS ou JS, aumente `V` em `src/build.py` para limpar o cache.

## Mídia
- `assets/video/hero.mp4` (desktop) e `hero-m.mp4` (celular): montagem de clipes livres do Pexels (7821807, 7735903, 8425702, 7593891) com tratamento de cor.
- `assets/video/reel-N.mp4`: reels do @escritorioeficaz; `reel-N-prev.mp4` são as prévias curtas sem som.
- `assets/img/servicos/` e `assets/img/contabil/`: fotos livres do Pexels.
- Na página Sobre há espaços reservados (`ph-photo`) para fotos reais da equipe, recepção, sala de reuniões e fachada. Para preencher, troque o `<figure class="ph-photo ...">` por `<figure class="img-reveal ..."><img src="..."></figure>`.

## Pendências
- Avaliações: o Google mostra só 3 completas sem login. Para incluir mais, copie de https://www.google.com/maps (ficha do escritório) para REVIEWS.
- Formulário abre o e-mail do visitante (mailto) ou o WhatsApp com a mensagem pronta.
- Agenda tributária é calculada no navegador a partir da data do dia: atualiza sozinha todo mês, sem considerar feriados.
