# LLM OCR - Análise Inteligente de Currículos

Sistema de análise inteligente de currículos que combina OCR (Reconhecimento Óptico de Caracteres) com LLM (Modelos de Linguagem Local via Ollama) para extrair e analisar informações de currículos.

## 📋 Funcionalidades

- **Extração de texto** de arquivos PDF e imagens usando OCR avançado (PaddleOCR)
- **Análise de currículos** com base em requisitos específicos de vagas
- **Resumo automático** destacando pontos principais dos currículos
- **Histórico de análises** com armazenamento em banco de dados
- **API RESTful** com documentação interativa

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e de alto desempenho
- **PaddleOCR**: Engine OCR de alta precisão
- **Ollama**: Para execução local de modelos de linguagem
- **PyMuPDF (fitz)**: Para processamento avançado de PDFs
- **Docker**: Para containerização da aplicação

## 🛠️ Problemas Conhecidos e Soluções

### Problemas Identificados



1. **Tempo de processamento elevado**  
  - **Descrição**: O tempo médio de leitura por arquivo é de aproximadamente 1 minuto, dependendo do tamanho do arquivo. Arquivos resumidos levam cerca de 50 segundos.  
  - **Solução**: Otimizar o pipeline de OCR e análise, ajustando parâmetros ou utilizando técnicas de paralelismo para processar múltiplos arquivos simultaneamente.


2. **Desempenho com requisições sem query**  
  - **Descrição**: Quando uma requisição é enviada sem uma query, o tempo de resposta da API é mais lento.  
  - **Solução**: Implementar um cache para respostas padrão ou otimizar o modelo LLM para cenários sem query.

3. **Impacto da temperatura no modelo LLM**  
  - **Descrição**: A temperatura configurada em 0.1 pode influenciar negativamente na decisão do recrutador, descartando currículos que poderiam ser relevantes.  
  - **Solução**: Ajustar a temperatura para um valor mais equilibrado (ex.: 0.3) para permitir maior diversidade nas respostas, sem comprometer a precisão.

4. **Tipo de modelo LLM influencia na resposta**  
    - **Descrição**: O modelo LLM utilizado pode gerar respostas diferentes dependendo de sua arquitetura e treinamento.  
    - **Solução**: Testar diferentes modelos disponíveis no Ollama para identificar aquele que melhor atende às necessidades do sistema. Além disso, permitir que o usuário selecione o modelo desejado via configuração na API ou interface.


### Referências para Resolução dos Problemas 

  1. **Otimização do Pipeline de OCR e Análise**  
    - Vídeo: [Como otimizar pipelines de OCR com PaddleOCR](https://www.youtube.com/watch?v=sq5TOVWUikU&t)  
    - Repositório: [asimov-academy/cv-analyzer - Implementação de análise com AI](https://github.com/asimov-academy/cv-analyzer/blob/main/analyze/ai.py)



    Essas referências fornecem insights práticos e exemplos de código que podem ser adaptados para resolver os problemas identificados no sistema.


### Histórico de Melhorias de Desempenho

  1. **Primeira Implementação com Hugging Face**  
    - **Descrição**: Inicialmente, o sistema utilizava modelos da Hugging Face para análise de currículos. O tempo médio de processamento era de aproximadamente 7 minutos por arquivo PDF.  
    - **Problema**: O tempo elevado tornava o sistema inviável para uso em larga escala.  
    - **Solução**: Após pesquisa e testes, foi realizada a migração para o Ollama, utilizando modelos LLM otimizados para execução local.  

  2. **Resultados Após a Otimização**  
    - **Descrição**: Com a adoção do Ollama e ajustes no pipeline de OCR e análise, o tempo médio de processamento foi reduzido para cerca de 1 minuto por arquivo PDF.  
    - **Referência Utilizada**:  
      - Vídeo: [Domine o Reconhecimento Óptico de Caracteres com PaddleOCR: Tutorial Completo em Python](https://www.youtube.com/watch?v=kkgN3hzkSs4)  
      - Repositório: [asimov-academy/cv-analyzer - Implementação de análise com AI](https://github.com/asimov-academy/cv-analyzer/blob/main/analyze/ai.py)




## 🚀 Instalação e Execução

### Pré-requisitos
- Docker e Docker Compose

### Utilizando Docker Compose

1. Clone o repositório:
   ```bash
   git clone git@github.com:HeitorLouzeiro/analisador-curriculos-llm.git
   cd analisador-curriculos-llm
   ```

2. Inicie os containers:
   ```bash
   docker-compose up -d
   ```

3. Após iniciar o container Ollama, em outro terminal execute:
   ```bash
   docker exec fabio_ollama ollama pull llama3.2
   ```

3. A API estará disponível em:
   ```
   http://localhost:8000
   ```

## 📖 Como Usar a API

### Analisar Currículos

**Endpoint**: `/api/analisar`

#### Parâmetros:
- `arquivos`: Lista de arquivos de currículo (PDF ou imagens)
- `query` (opcional): Requisitos da vaga para análise comparativa, se omitido gera resumo
- `user_id`: ID do usuário realizando a análise
- `request_id` (opcional): ID para rastreamento da solicitação

#### Exemplo de requisição:

```bash
curl -X POST "http://localhost:8000/api/analisar" \
  -H "accept: application/json" \
  -F "arquivos=@curriculo.pdf" \
  -F "user_id=user123" \
  -F "query=Desenvolvedor Python com experiência em FastAPI e Docker"
```

#### Exemplo de resposta:

```json
{
  "id": "6462a8e94f6d7b2e30a1c2d3",
  "request_id": "e1f2a3b4-c5d6-7e8f-9a0b-1c2d3e4f5a6b",
  "user_id": "user123",
  "timestamp": "2025-05-01T14:30:45.123Z",
  "query": "Desenvolvedor Python com experiência em FastAPI e Docker",
  "resultado": [
    {
      "arquivo": "curriculo.pdf",
      "resposta": "O currículo atende aos requisitos da vaga. O candidato possui 3 anos de experiência em desenvolvimento Python, com projetos utilizando FastAPI e containerização com Docker..."
    }
  ]
}
```

## 🔢 Status Codes

A API retorna os seguintes códigos de status HTTP:

- **200 OK**: Requisição bem-sucedida e resposta retornada com sucesso.
- **400 Bad Request**: Requisição inválida, como parâmetros ausentes ou incorretos.
- **415 Unsupported Media Type**: Formato de arquivo não suportado.
- **422 Unprocessable Entity**: Erro de validação - parâmetros inválidos ou faltando (como não fornecer arquivos).
- **500 Internal Server Error**: Erro interno no servidor durante o processamento da requisição.
- **503 Service Unavailable**: Serviço LLM indisponível (por exemplo, modelo não encontrado no Ollama).

Para mais detalhes, consulte a [Documentação Swagger](http://localhost:8000/docs).

## 📚 Documentação da API

A documentação interativa da API está disponível em:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Guia da API**: http://localhost:8000/

## 🧩 Estrutura do Projeto

```
├── app/                  # Código-fonte principal
│   ├── config/           # Configurações (banco de dados, etc.)
│   ├── docs/             # Documentação da API
│   ├── models/           # Modelos de dados
│   ├── repositories/     # Repositórios de dados
│   ├── routers/          # Definições de rotas da API
│   ├── services/         # Lógica de negócios
│   │   ├── analise_service.py  # Processamento de análises
│   │   ├── llm_service.py      # Comunicação com Ollama
│   │   └── ocr_service.py      # Extração de texto com OCR
│   ├── templates/        # Templates HTML
│   └── utils/            # Utilitários
├── app.py                # Ponto de entrada para desenvolvimento local
├── docker-compose.yml    # Configuração dos serviços
├── Dockerfile            # Definição do container
└── requirements.txt      # Dependências Python
```
<p align="right">(<a href="#top">voltar ao topo</a>)</p>

## ⚙️ Configuração do Modelo LLM

A aplicação utiliza o modelo LLM disponível via Ollama. Por padrão, o sistema está configurado para usar o modelo "llama3.2", mas isso pode ser ajustado.

### Personalização do Modelo LLM

Para personalizar o modelo LLM utilizado pela aplicação, siga os passos abaixo:

1. **Verifique a instalação do modelo no Ollama**  
  Certifique-se de que o modelo desejado está instalado no servidor Ollama. Você pode explorar e baixar modelos disponíveis no site: [Ollama Search](https://ollama.com/search).

2. **Baixe o modelo desejado**  
  Execute o comando abaixo para baixar o modelo no container Docker do Ollama:
  ```bash
  docker exec fabio_ollama ollama pull <nome_do_modelo>
  ```
  Exemplo:  
  Para baixar o modelo `llama4`, execute:
  ```bash
  docker exec fabio_ollama ollama pull llama4
  ```

3. **Atualize a configuração do modelo no código**  
  No arquivo `app/services/llm_service.py`, altere a linha que define o modelo padrão para o nome do modelo que você baixou:
  ```python
  self.default_model = "<nome_do_modelo>"
  ```
  Exemplo:  
  Para usar o modelo `llama4`, atualize para:
  ```python
  self.default_model = "llama4"
  ```

4. **Reinicie o serviço**  
  Após realizar as alterações, reinicie os containers para aplicar as mudanças:
  ```bash
  docker-compose restart
  ```

Com isso, o sistema estará configurado para utilizar o modelo LLM personalizado.

<p align="right">(<a href="#top">voltar ao topo</a>)</p>


## 📝 Desenvolvimento e Contribuição
### 🤝 Contribuindo

Contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será muito apreciada.

Se você tiver uma sugestão para melhorar este projeto, faça um fork do repositório e crie uma pull request. Você também pode abrir uma issue com a tag "melhoria". Não se esqueça de dar uma estrela ao projeto! Obrigado novamente!

#### Passos para Contribuir:

1. Faça um fork do projeto.
2. Crie sua branch de funcionalidade:
  ```bash
  git checkout -b feature/Melhorias
  ```
3. Faça o commit das suas alterações:
  ```bash
  git commit -m 'Adicionei minhas melhorias'
  ```
4. Envie para a branch:
  ```bash
  git push origin feature/Melhorias
  ```
5. Abra uma Pull Request.

Agradecemos sua contribuição para tornar este projeto ainda melhor! 😊

<p align="right">(<a href="#top">voltar ao topo</a>)</p>

### Padrões de Código
O projeto segue as convenções PEP 8 para código Python.

## 📄 Licença

Distribuído sob a Licença MIT. Consulte [LICENSE](LICENSE) para mais informações.

<p align="right">(<a href="#top">voltar ao topo</a>)</p>

## 👥 Contato

<div align='center'>  
  <a href="https://www.instagram.com/heitorlouzeiro/" target="_blank">
    <img src="https://img.shields.io/badge/-Instagram-%23E4405F?style=for-the-badge&logo=instagram&logoColor=white" target="_blank">
  </a> 
  <a href = "mailto:heitorlouzeiro2019@gmail.com">
    <img src="https://img.shields.io/badge/-Gmail-%23333?style=for-the-badge&logo=gmail&logoColor=white" target="_blank">    
  </a>
  <a href="https://www.linkedin.com/in/heitor-louzeiro/" target="_blank">
    <img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank">
  </a> 
</div>

Project Link: [https://github.com/HeitorLouzeiro/analisador-curriculos-llm](https://github.com/HeitorLouzeiro/analisador-curriculos-llm)

<p align="right">(<a href="#top">voltar ao topo</a>)</p>