import requests

# Configurar las credenciales de autenticación
username = 'myusername'
password = 'mypassword'

# Configurar los parámetros de la solicitud
host = 'myf5host'
virtual_server_name = 'myvirtualserver'

# Iniciar sesión y obtener la cookie de autenticación
auth_url = 'https://{}/mgmt/shared/authn/login'.format(host)
auth_payload = {'username': username, 'password': password}
response = requests.post(auth_url, json=auth_payload, verify=False)
auth_token = response.json()['token']['token']

# Configurar los encabezados de la solicitud con la cookie de autenticación
headers = {'X-F5-Auth-Token': auth_token}

# Obtener la configuración del virtual server
vs_url = 'https://{}/mgmt/tm/ltm/virtual/{}'.format(host, virtual_server_name)
response = requests.get(vs_url, headers=headers, verify=False)

# Extraer las direcciones IP disponibles del virtual server
if response.status_code == 200:
    vs_config = response.json()
    ip_list = vs_config.get('destination', {}).get('items', [])
    print('Direcciones IP disponibles para {}:'.format(virtual_server_name))
    for ip in ip_list:
        print(ip.get('fullPath'))
else:
    print('La solicitud para obtener la configuración de {} ha fallado con el código de estado {}.'.format(virtual_server_name, response.status_code))
