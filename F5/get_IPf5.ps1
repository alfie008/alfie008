# Configura las credenciales de autenticación
$username = 'myusername'
$password = 'mypassword'

# Configura los parámetros de la solicitud
$hostname = 'myf5host'

# Inicia sesión y obtiene la cookie de autenticación
$authUrl = "https://$hostname/mgmt/shared/authn/login"
$authPayload = @{username = $username; password = $password}
$response = Invoke-RestMethod -Uri $authUrl -Method POST -Body ($authPayload | ConvertTo-Json) -ContentType 'application/json'
$authToken = $response.token.token

# Configura los encabezados de la solicitud con la cookie de autenticación
$headers = @{ 'X-F5-Auth-Token' = $authToken }

# Obtiene la lista de virtual address list
$url = "https://$hostname/mgmt/tm/ltm/virtual-address-list"
$response = Invoke-RestMethod -Uri $url -Headers $headers -Method GET -ContentType 'application/json'

# Imprime el estado de cada virtual address list
if ($response) {
    foreach ($virtualAddressList in $response.items) {
        Write-Host "Virtual address list: $($virtualAddressList.name), status: $($virtualAddressList.status)"
    }
} else {
    Write-Host "La solicitud para obtener la lista de direcciones virtuales ha fallado."
}
