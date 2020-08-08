# Stopy

Robô que aprende e joga **[Stop]** desenvolvido em Python com conceitos básicos de IA com fins de aprendizado.

[stop]: https://stopots.com/pt/

## Instalando GeckoDriver (Mozilla Firefox Driver)

Para rodarmos o projeto e simularmos o navegador, precisamos do <b>GeckoDriver</b>, o driver do navegador Firefox que o Selenium utilizará.

1. Primeiro entre no repositório do **[GeckoDriver]**.
2. Baixe a versão compatível com o seu sistema operacional.
3. Adicione o arquivo `.exe` na diretório onde está instalado o seu Python.
4. Pronto, basta seguir com o processo!

[geckodriver]: https://github.com/mozilla/geckodriver/releases

## Dependências

```
pip install selenium
pip install requests
pip install times
pip install mysql-connector
```

## Migration

O modelo do banco de dados esperado pelo robô está no arquivo `migrations.sql` na raíz do projeto, basta executar isso em seu banco de dados mysql.

## Execução

Para rodar o robô, basta entrar no diretório do projeto e executar o comando `python3 main.py`.
