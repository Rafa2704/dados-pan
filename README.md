**Documentação Completa: Criação do Banco de Dados até o Final do Processo:**

1. **Criação do Banco de Dados PostgreSQL na AWS e das Tabelas:**

   **Explicação:**
   Um banco de dados PostgreSQL foi criado na Amazon Web Services (AWS) para armazenar os dados do projeto. Além disso, foram criadas as tabelas necessárias para armazenar os dados processados.

   **Querys:**
   ```sql
   -- Query de criação do banco de dados (exemplo)
   CREATE DATABASE postgres;

   -- Criação da tabela base_geral
   CREATE TABLE base_geral (
       cpf VARCHAR(11),
       nome_completo VARCHAR(255),
       email VARCHAR(255),
       uf VARCHAR(2),
       dt_nascimento DATE 
   );

   -- Criação da tabela anonimizada_nome
   CREATE TABLE anonimizada_nome (
       cpf_anonimo VARCHAR(255),
       primeiro_nome VARCHAR(255),
       renda DECIMAL
   );

   -- Criação da tabela anonimizada_uf
   CREATE TABLE anonimizada_uf (
       cpf_anonimo VARCHAR(255),
       ultimo_nome VARCHAR(255),
       uf VARCHAR(2),
       orgsup_lotacao_instituidor_pensao VARCHAR(255)
   );

2. **Importação dos Arquivos CSV para as Tabelas: Explicação:**

    Três arquivos CSV foram importados para criar três tabelas no banco de dados.
    Transformações e Criação de Chaves Primárias na Base "anonimizada_nome":
    
    **Explicação:**
    
    Na tabela "anonimizada_nome", foram realizadas transformações nos dados e criada uma chave primária para relacionar com outras tabelas.

    **Querys:**
    ```sql
    -- Transformação da coluna "cpf_anonimo" para remover asteriscos e espaços em branco
    UPDATE anonimizada_nome
    SET "﻿cpf_anonimo" = REPLACE(REPLACE("﻿cpf_anonimo", '*', ''), ' ', '');
    
    -- Criação da chave primária "chave_geral_nome"
    ALTER TABLE anonimizada_nome
    ADD COLUMN chave_geral_nome VARCHAR(255);
    
    UPDATE anonimizada_nome
    SET chave_geral_nome = CONCAT("﻿cpf_anonimo", '-', LOWER(primeiro_nome));
    ```
    
3. **Transformações e Criação de Chaves Primárias na Base "anonimizada_uf":**

    **Explicação:**
    
    Assim como na tabela "anonimizada_nome", na tabela "anonimizada_uf" foram realizadas transformações nos dados e criada uma chave primária.

    **Querys:**
    ```sql
    ---- Transformação da coluna "cpf_anonimo" para remover asteriscos e espaços em branco
    UPDATE anonimizada_uf
    SET "﻿cpf_anonimo" = REPLACE(REPLACE("﻿cpf_anonimo", '*', ''), ' ', '');
    
    -- Criação da chave primária "chave_uf_anoni"
    ALTER TABLE anonimizada_uf
    ADD COLUMN chave_uf_anoni VARCHAR(255);
    
    UPDATE anonimizada_uf
    SET chave_uf_anoni = CONCAT("﻿cpf_anonimo", '-', LOWER(ultimo_nome));
    ```

4. **Atualização da Base "base_geral":**

    **Explicação:**
    
    Na tabela "base_geral", foram adicionadas novas colunas para armazenar informações adicionais relacionadas aos CPFs e e-mails.

    **Querys:**
    ```sql
    -- Adicionando uma nova coluna para o primeiro nome no email
    ALTER TABLE base_geral
    ADD COLUMN primeiro_nome_email VARCHAR(255);

    -- Atualizando a nova coluna com o primeiro nome do email
    UPDATE base_geral
    SET primeiro_nome_email = SPLIT_PART(email, '.', 1);

    -- Adição da coluna "sobrenome_email"
    ALTER TABLE base_geral
    ADD COLUMN sobrenome_email VARCHAR(255);

    -- Atualização da coluna "sobrenome_email" com o sobrenome extraído do endereço de e-mail
    UPDATE base_geral
    SET sobrenome_email = SUBSTRING(email, POSITION('.' IN email) + 1, POSITION('@' IN email) - POSITION('.' IN email) - 1);

    -- Adicionando uma nova coluna para os 6 números do meio do CPF
    ALTER TABLE base_geral
    ADD COLUMN numeros_meio_cpf VARCHAR(6);

    -- Atualizando a nova coluna com os 6 números do meio do CPF
    UPDATE base_geral
    SET numeros_meio_cpf = SUBSTRING("﻿cpf", 4, 6);

    -- Criação da chave primária "chave_geral_nome" para se relacionar com anonimizada_nome
    ALTER TABLE base_geral
    ADD COLUMN chave_geral_nome VARCHAR(255);

    UPDATE base_geral
    SET chave_geral_nome = CONCAT("﻿cpf_anonimo", '-', LOWER(primeiro_nome));
    ```
## 5. Relacionamentos Finais:

### Explicação:

A seguir está a consulta SQL que realiza os relacionamentos finais após as alterações feitas nas tabelas. Essa consulta une as tabelas `base_geral`, `anonimizada_nome` e `anonimizada_uf`, utilizando as chaves criadas para relacionamento.

### Query:

```sql
SELECT 
    CONCAT(bg.numeros_meio_cpf, '-', bg.primeiro_nome_email) AS chave_nome,
    CONCAT(bg.numeros_meio_cpf, '-', bg.sobrenome_email) AS chave_uf,
    bg."﻿cpf",
    bg.nome_completo,
    bg.uf,
    bg.dt_nascimento,
    an.renda,
    uf.orgsup_lotacao_instituidor_pensao
FROM 
    base_geral bg 
LEFT JOIN 
    anonimizada_nome an ON CONCAT(bg.numeros_meio_cpf, '-', bg.primeiro_nome_email) = an.chave_geral_nome
LEFT JOIN 
    anonimizada_uf uf ON CONCAT(bg.numeros_meio_cpf, '-', bg.sobrenome_email) = uf.chave_uf_anoni
WHERE 
    an.chave_geral_nome IS NOT NULL AND uf.orgsup_lotacao_instituidor_pensao IS NOT NULL;
```
## 6. Conexão Python com Banco de dados: 

### Script Python para Conexão com Banco de Dados e Criação de Indicadores:


      ```python
      import psycopg2
      import pandas as pd
      
      # Conectar ao banco de dados
      conn = psycopg2.connect(
          dbname="postgres",
          user="postgres",
          password="xxxxxx",
          host="xxxxxxxxxxxxx"
      )
      
      # Criar um cursor
      cur = conn.cursor()
      
      # Executar a consulta SQL
      cur.execute("""
          SELECT 
              concat(bg.numeros_meio_cpf, '-', bg.primeiro_nome_email) as chave_nome,
              concat(bg.numeros_meio_cpf, '-', bg.sobrenome_email) as chave_uf,
              bg."﻿cpf",
              bg.nome_completo,
              bg.uf,
              bg.dt_nascimento,
              an.renda,
              uf.orgsup_lotacao_instituidor_pensao
          FROM base_geral bg 
          LEFT JOIN anonimizada_nome an ON concat(bg.numeros_meio_cpf, '-', bg.primeiro_nome_email) = an.chave_geral_nome
          LEFT JOIN anonimizada_uf uf ON concat(bg.numeros_meio_cpf, '-', bg.sobrenome_email) = uf.chave_uf_anoni
          WHERE an.chave_geral_nome IS NOT NULL AND uf.orgsup_lotacao_instituidor_pensao IS NOT NULL
      """)
      
      # Obter os resultados
      rows = cur.fetchall()
      
      # Fechar o cursor e a conexão
      cur.close()
      conn.close()
      
      # Criar um DataFrame com os resultados
      df = pd.DataFrame(rows, columns=[
          'chave_nome',
          'chave_uf',
          'cpf',
          'nome_completo',
          'uf',
          'dt_nascimento',
          'renda',
          'orgsup_lotacao_instituidor_pensao'
      ])
      
      # Exibir o DataFrame
      display(df)
      
      # Exibir o DataFrame
      display(df)

## Anexos do Projeto
  As imagens das tabelas no Dbeaver e os indicadores gerados com Python estão anexados no projeto
