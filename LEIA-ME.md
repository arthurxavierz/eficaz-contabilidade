# Escritório Eficaz · site

Site estático, sem dependências. Abra `index.html` no navegador ou publique a pasta inteira em qualquer hospedagem.

## Páginas
- `index.html` início
- `empresa.html` empresa, visão, missão, responsáveis
- `servicos.html` cinco frentes de serviço, parcerias e passo a passo de abertura
- `correspondente-caixa.html` produtos Caixa Aqui
- `noticias.html` notícias
- `links-uteis.html` links com busca e filtro
- `contato.html` telefones, formulário e mapa
- `privacidade.html` privacidade e termos (LGPD)

## Como editar
O cabeçalho, o rodapé e os dados de contato (telefones, WhatsApp, redes, CNPJ, endereços dos mapas) ficam em `src/build.py`.
O conteúdo de cada página fica em `src/pages/`. Depois de editar, rode:

    python src/build.py

O script recusa textos com travessão, para manter o padrão de escrita.

## Pendências antes de publicar
- Confirmar o número de WhatsApp e o horário de atendimento em `src/build.py` (bloco EMPRESA). Hoje o WhatsApp usa o fixo de Patrocínio.
- Notícias: hoje estão fixas (edição de 25/09/2026) e apontam para as páginas atuais do site antigo. Para atualização diária, integrar o feed do fornecedor de notícias.
- Formulário: abre o e-mail do visitante com a mensagem pronta (mailto). Para envio direto, ligar a um serviço como Formspree ou a um endpoint próprio.
- Agenda tributária: calcula os prazos usuais a partir da data do dia, sem considerar feriados.
- Fotos: foram reaproveitadas do site antigo, com tratamento em duotone. Vale substituir por fotos reais da equipe e das unidades.
