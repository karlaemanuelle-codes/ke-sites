"""
commerce — motor comercial da KE Sites (preços, parcelamento, promoções,
comissões, assinaturas e provedores de pagamento).

IMPORTANTE — leia antes de conectar qualquer coisa a dinheiro real:

Este pacote é ARQUITETURA PREPARADA, não uma integração ativa. Nada aqui se
conecta a uma conta real de Ton, Stripe, Mercado Pago ou qualquer gateway.
Não existem credenciais, não existe servidor rodando estes módulos em
produção, e nenhuma taxa aqui é a taxa real vigente de nenhum provedor —
todas as taxas são valores ilustrativos, marcados com `ilustrativo=True`,
e devem ser confirmados com a documentação oficial do provedor antes de
qualquer cobrança real (ver `providers.py`, seção "REGRA TON").

O que este pacote resolve:
  - Modelagem de Order/Subscription/Promotion/Bonus/Commission (models.py)
  - Cálculo de parcelamento configurável, sem taxa hardcoded (pricing.py)
  - Abstração de provedor de pagamento + adapters preparados (providers.py)
  - Motor de comissão de afiliado com ciclo de vida completo (commissions.py)
  - Motor de promoções + proteção de margem mínima (promotions.py)
  - Validação de webhook + idempotência (webhooks.py)
  - Configuração administrável central, nada hardcoded (config.py)

O que este pacote NÃO faz (requer infraestrutura real que não existe neste
projeto — um site estático, sem backend/servidor/banco de dados):
  - Processar um pagamento de verdade
  - Gerar um QR Code Pix real
  - Tokenizar um cartão de verdade
  - Receber um webhook de verdade (não há servidor exposto para recebê-lo)
  - Persistir Order/Subscription em um banco de dados real
"""
