# commerce — motor comercial da KE Sites

Pacote Python com a arquitetura de pagamentos, parcelamento, comissão de
afiliado, promoções e assinaturas descrita no adendo de pagamentos.

## O que é real aqui

- `models.py`, `config.py`, `pricing.py`, `providers.py`, `commissions.py`,
  `promotions.py`, `webhooks.py` — código funcional, testado (`tests/`,
  42 testes, `python3 -m pytest commerce/tests/`).
- A calculadora de parcelamento (`pricing.py`) roda de verdade e alimenta o
  checkout da plataforma (`platform/templates/pages/checkout.html`), que
  usa esses números pré-calculados no build — nenhum valor é inventado no
  navegador.
- Nenhuma taxa é hardcoded como definitiva — tudo em `config.py` está
  marcado `ilustrativo=True` e deve ser confirmado com a documentação
  oficial do provedor escolhido antes de qualquer cobrança real.

## O que NÃO é real aqui (e por quê)

Este projeto é um site estático (gerado por Jinja2, sem backend, sem banco
de dados, sem servidor rodando em produção). Por isso:

- `providers.py`: `TonProvider`, `StripeProvider` e `MercadoPagoProvider`
  levantam `NotConnectedError` em qualquer operação real — não existem
  credenciais nem conta configurada. `ManualProvider` é o único adapter que
  "funciona", porque modela o fluxo manual (conferência humana de
  Pix/transferência), que não depende de uma API externa.
- `webhooks.py`: modela idempotência, mas não há servidor HTTP exposto
  para receber um webhook de verdade.
- Não existe painel administrativo com dados reais, nem persistência em
  banco de dados — `Order`, `Subscription`, `Commission` etc. são apenas
  o contrato de dados (dataclasses), sem tabela por trás.

## Para conectar isso a um pagamento real, futuramente

1. Hospedar um backend real (com banco de dados) que importe este pacote.
2. Criar uma conta real no provedor escolhido (Ton, Stripe ou Mercado
   Pago) e obter credenciais.
3. Implementar `create_charge`/`verify_webhook`/`refund` no adapter
   correspondente usando o SDK oficial do provedor — o `NotConnectedError`
   atual é exatamente o ponto onde esse código real entra.
4. Confirmar as taxas vigentes na documentação oficial do provedor e
   substituir os valores ilustrativos em `config.py`.
5. Expor um endpoint HTTP real para receber os webhooks do provedor.
