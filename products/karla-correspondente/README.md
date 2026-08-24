# Karla Emanuelle - site e CRM MVP

Primeira versão funcional, mobile-first e estática para testes.

## Funcionalidades

- site público com serviços, comunicação neutra e CTAs de WhatsApp;
- formulário de lead com consentimento e abertura do WhatsApp;
- CRM local com funil, histórico de etapas, vendas e pós-venda;
- avaliações com consentimento, moderação e ocultação;
- configurações editáveis de empresa, produtos, instituições e certificações;
- nenhuma certificação, exclusividade ou credenciamento fictício;
- cabeçalhos básicos de segurança.

## Limitação intencional do MVP

O CRM usa `localStorage`: os dados ficam apenas no navegador usado. Isso permite teste funcional sem expor uma API administrativa pública, mas não oferece sincronização entre aparelhos, login, banco persistente, automações ou recuperação de senha. Não inserir dados sensíveis na versão pública de teste.

## Teste local

```bash
python -m http.server 8080 -d products/karla-correspondente
```

Acesse `/` para o site e `/admin.html` para o CRM.
