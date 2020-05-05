from urllib.request import urlopen, Request
import xml.etree.ElementTree as ET

server_name = "Your_Server"
version = "3.4"
site_url_id = "Your_Site"
personal_access_token_name = "Your_Token_Name"
personal_access_token_secret = "Your_Token_Secret"

signin_url = "https://{server}/api/{version}/auth/signin".format(server=server_name, version=version)

request_xml = ET.Element('tsRequest')
credentials = ET.SubElement(request_xml, 'credentials',
personalAccessTokenName=personal_access_token_name,
personalAccessTokenSecret=personal_access_token_secret)
site_element = ET.SubElement(credentials, 'site', contentUrl="site_url_id")
request_data = ET.tostring(request_xml)

# Send the request to the server
req = Request(signin_url, data=request_data, method="POST")
req = urlopen(req)

# Get the response
server_response = req.read()
response_xml = ET.fromstring(server_response)

# Get the authentication token from the <credentials> element
token = response_xml.find('.//t:credentials',
			namespaces={'t': "http://tableau.com/api"}).attrib['token']

# Get the site ID from the <site> element
site_id = response_xml.find('.//t:site',
			namespaces={'t': "http://tableau.com/api"}).attrib['id']

print('Sign in successful!')
print('\tToken: {token}'.format(token=token))
print('\tSite ID: {site_id}'.format(site_id=site_id))
