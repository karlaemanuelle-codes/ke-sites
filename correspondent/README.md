# Correspondente Bancário - Módulos reutilizáveis

Este pacote integra ao patrimônio atual da KE Sites duas capacidades sem alterar os produtos existentes:

1. **Compliance profissional configurável**, sem credenciais, registros ou vínculos presumidos.
2. **Pós-venda e avaliações moderadas**, com separação entre dados internos e dados públicos autorizados.

## Segurança institucional

- Nenhuma certificação, instituição parceira ou informação regulatória é publicada por padrão.
- Itens só podem ir ao site quando estiverem confirmados e marcados como públicos.
- Expressões de exclusividade, representação oficial e vínculo empregatício não fazem parte do conteúdo padrão.
- A associação de uma avaliação à venda e ao cliente fica apenas no CRM.

## Fluxo de avaliações

`LEAD -> ATENDIMENTO -> SIMULACAO -> PROPOSTA -> VENDA_CONCLUIDA -> POS_VENDA -> AVALIACAO_SOLICITADA -> PENDENTE_APROVACAO -> APROVADA | REJEITADA`

Uma avaliação aprovada ainda precisa de autorização de publicação e de `publicada=true` para entrar na exportação pública.

## Uso

```python
from correspondent import CorrespondentService
from correspondent.config import load_config
from correspondent.repository import JsonRepository

service = CorrespondentService(
    repository=JsonRepository("data/correspondent-crm.json"),
    config=load_config("correspondent/config/site_config.json"),
)
```

O `JsonRepository` é uma implementação local/testável. A interface `ReviewRepository` permite substituir o armazenamento por banco de dados sem reescrever as regras.

## Testes

```bash
python -m unittest discover -s correspondent/tests -v
```

Não há rotina de deploy neste pacote.
