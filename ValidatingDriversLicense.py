import requests
import json

# Replace YOUR_API_KEY with your actual DVLA API key
API_KEY = 'YOUR_API_KEY'

# Replace DRIVER_LICENSE_NUMBER with the driver's license number you want to verify
DRIVER_LICENSE_NUMBER = 'DRIVER_LICENSE_NUMBER'

# Make a request to the DVLA API to retrieve information about the driver's license
response = requests.get(f'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles/{DRIVER_LICENSE_NUMBER}',
                        headers={'x-api-key': API_KEY})

# If the response is successful (status code 200), parse the JSON response and extract the driver's name and address
if response.status_code == 200:
    data = json.loads(response.text)
    driver_name = data['DriverName']
    driver_address = data['DriverAddress']
    print(f'Driver name: {driver_name}')
    print(f'Driver address: {driver_address}')
else:
    print(f'Error: {response.status_code} {response.reason}')
