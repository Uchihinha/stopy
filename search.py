import json
import time

items = [{'category': 'SÉRIE', 'word': 'CQWE'}, {'category': 'CARRO', 'word': 'CQWE'}, {'category': 'CIDADE', 'word': 'CQWE'}, {'category': 'MARCA', 'word': 'CQWE'}, {'category': 'PCH', 'word':
'CQWE'}, {'category': 'ADJETIVO', 'word': 'CQWE'}, {'category': 'MÚSICA', 'word': 'CQWE'}, {'category': 'CANTOR', 'word': 'CQWE'}, {'category': 'NOME', 'word': 'CQWE'}, {'category': 'SOBREMESA', 'word': 'CQWE'}, {'category': 'INSETO', 'word': 'CQWE'}, {'category': 'ELETRO ELETRÔNICO', 'word': 'CQWE'}]

data = json.dumps(items, indent=4, ensure_ascii=False)

print(data)

fp = open(str(round(time.time() * 1000)) + '.json', 'w', encoding='utf8')
fp.write(str(data))
fp.close()
