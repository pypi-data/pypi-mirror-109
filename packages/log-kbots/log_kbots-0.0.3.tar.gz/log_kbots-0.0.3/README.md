# log_kbots

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=flat-square)](https://www.python.org/)



A biblioteca fornece uma função que aceita dados de robôs como entrada, os valida e cria um arquivo json pronto para upload.



#### Argumentos de entrada esperados:
    
- PATH_LOG (str): Caminho para a diretório com logs json a processar
- robot_name (str): Código do robô (ex: DGA-100)
- schedule_value (str): Agendamento do robô em formato padrão cron
- start_date (datetime): Datahora do início do processamento do dado
- status (str): Status final do processamento do dado
- error_value (str, optional): Mensagem de erro quando existente. Padrao é None.
- detail_value (str, optional): Informações adicionais ao dado quando necessário. Padrao é None.



#### Feito:
- Cria arquivo json no formato correto
- Confere se o status do processamento está entre os esperados 


#### A fazer:
- Conferir acesso a pasta de logs
- Validar formato do nome do robô
