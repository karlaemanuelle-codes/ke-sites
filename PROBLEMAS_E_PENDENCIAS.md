# PROBLEMAS E PENDÊNCIAS

Última auditoria: 21/08/2026. Verificado nesta rodada: os 3 builds (Salão, Vôlei, Plataforma) rodam sem erro, e os 42 testes automatizados do motor de pagamentos passam.

## 🔴 CRÍTICO

Nenhum problema crítico conhecido no momento. (Os dois problemas críticos encontrados em rodadas anteriores — um bug de layout que "estourava" a tela no celular em um painel de demonstração, e uma chave de tradução que aparecia como texto cru na tela — já foram corrigidos e reverificados.)

## 🟠 IMPORTANTE

- **Não existe controle de versão (git) configurado.** Isso significa que não há histórico automático de mudanças, nem uma forma fácil de "desfazer" uma alteração ruim além do backup manual. Recomendo fortemente configurar isso — é uma mudança de infraestrutura segura (não altera nada do site), mas estou registrando aqui em vez de fazer sozinha, porque envolve decisões suas (nome do repositório, se fica local ou em um serviço como GitHub, quem tem acesso).
- **Nenhuma hospedagem/domínio configurado.** O projeto todo ainda vive apenas neste ambiente de trabalho — nenhum site está publicamente acessível hoje.
- **O motor de pagamentos (`commerce/`) não está conectado a nenhuma conta real** de gateway (Ton/Stripe/Mercado Pago). O checkout do site é uma simulação visual completa e testada, mas nenhum pagamento real pode ser processado até que uma conta seja configurada. Detalhes em `commerce/README.md`.
- **Nenhum cliente real recebeu ainda um template personalizado.** Todo o conteúdo hoje é fictício/demonstrativo (marcado como DEMO ONLY onde aplicável).

## 🟡 MELHORIA

- **Duplicação de arquivos entre os 3 projetos**: `main.js` e `modal.js` são idênticos nos três (`platform`, `ct-de-volei`, `salao-de-beleza`); `base.css`/`components.css` são ~99% idênticos. Hoje cada projeto mantém sua própria cópia. Poderiam virar uma pasta única compartilhada — mas isso exige alterar os 3 `build.py` para apontar para essa pasta comum, o que é uma mudança de código, não só de organização. Não fiz essa alteração porque envolve refatorar código, o que você pediu para não fazer sem autorização.
- **A estrutura de pastas não segue ainda a nomenclatura numerada que você desenhou** (`01_TEMPLATES/ESPORTES/VOLEI/...`). Expliquei o motivo detalhado em `00_DOCUMENTACAO/MAPA_DO_PROJETO.md` — resumindo, essa estrutura pressupõe uma pasta de código por nível, e isso trocaria "um código, 3 níveis gerados" por "3 códigos duplicados", o que seria um passo atrás. Se quiser mesmo assim seguir esse caminho (ou uma variação dele, como só agrupar Vôlei/Futebol dentro de uma pasta `ESPORTES/`), me avise e eu faço com cuidado, atualizando os caminhos nos `build.py` para nada quebrar.
- **Template "Futebol" ainda não existe.** Registrado como "NÃO CRIADO" em `CONTROLE_DA_KE_SITES.md`, conforme pedido.

## 🟢 FUTURO

- Fases 2 a 5 do roadmap comercial (Afiliados com cadastro/dashboard real, CRM, Programa de Partners completo, Automação) — nenhuma foi iniciada ainda, por decisão deliberada de seguir por fases.
- Conectar o motor de pagamentos a uma conta real quando a KE Sites estiver pronta para vender de verdade.
- Testar a plataforma com usuários reais dos mercados internacionais (Espanha/EUA) — hoje en-US/es-ES existem e geram sem erro, mas nunca foram validados com um cliente real desses países.
- Pixels de rastreamento de anúncios (Google/Meta/TikTok/Pinterest) — vão exigir contas de anúncio reais quando chegar a hora.

## Segurança

Verifiquei o projeto inteiro em busca de senhas, chaves de API, tokens ou outras credenciais expostas: **nenhuma foi encontrada.** O projeto também não usa nenhum arquivo `.env` hoje. Não há sistema de versionamento configurado ainda, então a recomendação de ".gitignore para não vazar segredos" ficará registrada para quando o git for configurado (veja o item 🟠 acima).
