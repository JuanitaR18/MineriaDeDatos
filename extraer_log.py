import re
import json
import matplotlib.pyplot as plt
from collections import Counter

log_file = 'logs.txt'

ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'
datetime_pattern = r'\d{2}/\w{3}/\d{4}(:\d{2}){3}'
http_method_pattern = r'(GET|POST|PUT|DELETE)'
status_code_pattern = r'\d{3}'  # Captura los códigos de estado HTTP
url_pattern = r'"(GET|POST|PUT|DELETE) (.*?) HTTP/1.1"'  # Captura las URLs

extracted_data = []

with open(log_file, 'r') as file:
    for line in file:
        ip_match = re.search(ip_pattern, line)
        method_match = re.search(http_method_pattern, line)
        status_code_match = re.search(status_code_pattern, line)
        url_match = re.search(url_pattern, line)

        # Si se encuentran todas las coincidencias
        if ip_match and method_match and status_code_match and url_match:
            data = {
                'ip': ip_match.group(0),
                'method': method_match.group(0),
                'status_code': status_code_match.group(0),
                'url': url_match.group(2)
            }
            extracted_data.append(data)

with open('datos_extraidos.json', 'w') as json_file:
    json.dump(extracted_data, json_file, indent=4)

methods = [data['method'] for data in extracted_data]
method_counts = Counter(methods)

plt.figure(figsize=(8, 6))
plt.bar(method_counts.keys(), method_counts.values(), color='skyblue')
plt.title('Distribución de Métodos HTTP')
plt.xlabel('Método HTTP')
plt.ylabel('Frecuencia')
plt.show()

status_codes = [data['status_code'] for data in extracted_data if data['status_code'].startswith('4') or data['status_code'].startswith('5')]
status_code_counts = Counter(status_codes)

plt.figure(figsize=(8, 6))
plt.bar(status_code_counts.keys(), status_code_counts.values(), color='salmon')
plt.title('Frecuencia de Errores HTTP (Códigos 4xx y 5xx)')
plt.xlabel('Código de Estado HTTP')
plt.ylabel('Frecuencia')
plt.show()

urls = [data['url'] for data in extracted_data]
url_counts = Counter(urls)

plt.figure(figsize=(8, 6))
plt.bar(url_counts.keys(), url_counts.values(), color='lightgreen')
plt.title('Accesos a Recursos Específicos')
plt.xlabel('Recurso')
plt.ylabel('Frecuencia')
plt.xticks(rotation=90)  # Rota las etiquetas del eje X para evitar superposición
plt.show()
