# Arquitetura - Correspondente bancário, compliance e avaliações

## Integração com a KE Sites existente

O repositório usa Python, Jinja e JSON para gerar produtos e a plataforma. Em vez de recriar a fábrica ou converter o projeto para outro framework, a funcionalidade foi adicionada como um domínio independente em `correspondent/`, seguindo o mesmo padrão configurável já usado no restante da solução.

## Limites dos módulos

| Módulo | Responsabilidade |
|---|---|
| `config.py` | Impedir publicação de afirmações profissionais não confirmadas |
| `models.py` | Estados e entidades de venda e avaliação |
| `repository.py` | Contrato de persistência e armazenamento JSON substituível |
| `service.py` | Fluxo de pós-venda, moderação, métricas e exportação pública |
| `site_config.json` | Conteúdo, campos e regras editáveis por cliente |
| `tests/` | Regressão das regras de privacidade e publicação |

## Separação de dados

A exportação pública nunca inclui `cliente_id`, `venda_id`, `proposta_id` ou `cliente_nome_interno`. O site recebe somente nota, depoimento, nome autorizado e data das avaliações elegíveis.

## Critérios para publicação

Uma avaliação só entra no site quando todos forem verdadeiros:

1. O cliente autorizou a publicação.
2. A avaliação foi aprovada manualmente.
3. A avaliação foi marcada explicitamente como publicada.

O mesmo princípio se aplica a certificações, credenciamentos, bancos e informações regulatórias: cada item precisa estar confirmado e marcado para publicação.

## Evolução futura

- Implementar adaptador SQL para produção sem alterar o serviço.
- Conectar envio de solicitações a um provedor de mensagens.
- Adicionar autenticação e autorização ao painel administrativo.
- Renderizar os dados públicos nos templates Jinja do produto específico.
- Registrar trilha de auditoria de edições e moderações.

Nenhuma integração de envio ou deploy foi executada nesta entrega.
