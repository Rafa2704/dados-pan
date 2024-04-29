#!/usr/bin/env python
# coding: utf-8

# In[3]:


import psycopg2
import pandas as pd

# Conectar ao banco de dados
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Cisper270484",
    host="database-1.cvmo64yu8eu7.us-east-2.rds.amazonaws.com"
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


# In[5]:


contagem_uf = df['uf'].value_counts()
print("Contagem de registros por UF:\n", contagem_uf)


# In[6]:


import matplotlib.pyplot as plt

contagem_uf.plot(kind='bar')
plt.title('Contagem de Registros por UF')
plt.xlabel('UF')
plt.ylabel('Contagem')
plt.show()


# In[7]:


total_registros = len(df)
print("Total de registros:", total_registros)


# In[8]:


plt.hist(df['renda'], bins=20, color='skyblue', edgecolor='black')
plt.title('Histograma da Renda')
plt.xlabel('Renda')
plt.ylabel('Frequência')
plt.show()


# In[9]:


from datetime import datetime

agora = datetime.now()
df['idade'] = (agora - df['dt_nascimento']).astype('<m8[Y]')
media_idade = df['idade'].mean()
print("Idade média:", media_idade)


# In[10]:


plt.boxplot(df['idade'])
plt.title('Boxplot da Idade')
plt.ylabel('Idade')
plt.show()


# In[11]:


plt.pie(contagem_uf, labels=contagem_uf.index, autopct='%1.1f%%')
plt.title('Distribuição dos Registros por UF')
plt.axis('equal')
plt.show()


# In[ ]:




