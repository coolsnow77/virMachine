#!/bin/bash

url='http://127.0.0.1:5000/v2.0/tokens'
#curl -i 'http://127.0.0.1:5000/v2.0/tokens' -X POST -H "Content-Type: application/json" -H "Accept: application/json"  -d '{"auth": {"tenantName": "service", "passwordCredentials": {"username": "ceilometer", "password": "incito"}}}' | python -mjson.tool


curl  -s    -H "Content-Type: application/json" -H "Accept: application/json"  -d '{"auth": {"tenantName": "service", "passwordCredentials": {"username": "ceilometer", "password": "incito"}}}' $url | python -mjson.tool


echo  "############################################################"
#curl  -s    -H "Content-Type: application/json" -H "Accept: application/json"  -d '{"auth": {"tenantName": "", "passwordCredentials": {"username": "ceilometer", "password": "incito"}}}' $url | python -mjson.tool 


# echo  tenants  list 


token='MIIIRwYJKoZIhvcNAQcCoIIIODCCCDQCAQExDTALBglghkgBZQMEAgEwggaVBgkqhkiG9w0BBwGgggaGBIIGgnsiYWNjZXNzIjogeyJ0b2tlbiI6IHsiaXNzdWVkX2F0IjogIjIwMTQtMDktMDlUMDc6MDk6NDMuNzExNDc5IiwgImV4cGlyZXMiOiAiMjAxNC0wOS0wOVQwODowOTo0M1oiLCAiaWQiOiAicGxhY2Vob2xkZXIiLCAidGVuYW50IjogeyJkZXNjcmlwdGlvbiI6ICJTZXJ2aWNlIFRlbmFudCIsICJlbmFibGVkIjogdHJ1ZSwgImlkIjogImVlM2Y0NzRkODliNjQ2MzdiMjA2YmFhNmQ0MjlkMGMzIiwgIm5hbWUiOiAic2VydmljZSJ9fSwgInNlcnZpY2VDYXRhbG9nIjogW3siZW5kcG9pbnRzIjogW3siYWRtaW5VUkwiOiAiaHR0cDovL2NvbnRyb2xsZXI6OTI5MiIsICJyZWdpb24iOiAicmVnaW9uT25lIiwgImludGVybmFsVVJMIjogImh0dHA6Ly9jb250cm9sbGVyOjkyOTIiLCAiaWQiOiAiMTMxNGMxMWU2ZWI4NDVlNTkxNjU5ZDMxNzM4MGY3M2QiLCAicHVibGljVVJMIjogImh0dHA6Ly9jb250cm9sbGVyOjkyOTIifV0sICJlbmRwb2ludHNfbGlua3MiOiBbXSwgInR5cGUiOiAiaW1hZ2UiLCAibmFtZSI6ICJnbGFuY2UifSwgeyJlbmRwb2ludHMiOiBbeyJhZG1pblVSTCI6ICJodHRwOi8vY29udHJvbGxlcjo4Nzc0L3YyL2VlM2Y0NzRkODliNjQ2MzdiMjA2YmFhNmQ0MjlkMGMzIiwgInJlZ2lvbiI6ICJyZWdpb25PbmUiLCAiaW50ZXJuYWxVUkwiOiAiaHR0cDovL2NvbnRyb2xsZXI6ODc3NC92Mi9lZTNmNDc0ZDg5YjY0NjM3YjIwNmJhYTZkNDI5ZDBjMyIsICJpZCI6ICI0MjM1ODdlNmQ2MWM0NTcxYjVlZDMzNDgwMDkxMzM4NCIsICJwdWJsaWNVUkwiOiAiaHR0cDovL2NvbnRyb2xsZXI6ODc3NC92Mi9lZTNmNDc0ZDg5YjY0NjM3YjIwNmJhYTZkNDI5ZDBjMyJ9XSwgImVuZHBvaW50c19saW5rcyI6IFtdLCAidHlwZSI6ICJjb21wdXRlIiwgIm5hbWUiOiAibm92YSJ9LCB7ImVuZHBvaW50cyI6IFt7ImFkbWluVVJMIjogImh0dHA6Ly9jb250cm9sbGVyOjg3NzciLCAicmVnaW9uIjogInJlZ2lvbk9uZSIsICJpbnRlcm5hbFVSTCI6ICJodHRwOi8vY29udHJvbGxlcjo4Nzc3IiwgImlkIjogIjhjNjgwOGVjMTEyNzRiY2NhYmFjYWQxNjI1MmEyN2M3IiwgInB1YmxpY1VSTCI6ICJodHRwOi8vY29udHJvbGxlcjo4Nzc3In1dLCAiZW5kcG9pbnRzX2xpbmtzIjogW10sICJ0eXBlIjogIm1ldGVyaW5nIiwgIm5hbWUiOiAiY2VpbG9tZXRlciJ9LCB7ImVuZHBvaW50cyI6IFt7ImFkbWluVVJMIjogImh0dHA6Ly9jb250cm9sbGVyOjM1MzU3L3YyLjAiLCAicmVnaW9uIjogInJlZ2lvbk9uZSIsICJpbnRlcm5hbFVSTCI6ICJodHRwOi8vY29udHJvbGxlcjo1MDAwL3YyLjAiLCAiaWQiOiAiNDQyYjExNmRjMTNlNDIyMDk3NjE2OWViODIzNDIzMmQiLCAicHVibGljVVJMIjogImh0dHA6Ly9jb250cm9sbGVyOjUwMDAvdjIuMCJ9XSwgImVuZHBvaW50c19saW5rcyI6IFtdLCAidHlwZSI6ICJpZGVudGl0eSIsICJuYW1lIjogImtleXN0b25lIn1dLCAidXNlciI6IHsidXNlcm5hbWUiOiAiY2VpbG9tZXRlciIsICJyb2xlc19saW5rcyI6IFtdLCAiaWQiOiAiOGUwMDlkNzQ4ZTIyNDc5NjgzYTExNDIwZGI2YzEwYTQiLCAicm9sZXMiOiBbeyJuYW1lIjogImFkbWluIn1dLCAibmFtZSI6ICJjZWlsb21ldGVyIn0sICJtZXRhZGF0YSI6IHsiaXNfYWRtaW4iOiAwLCAicm9sZXMiOiBbImQwZjVkNWE5ODkyYjQ4YTBiNTRiMGNlZjYxMTNjMGJhIl19fX0xggGFMIIBgQIBATBcMFcxCzAJBgNVBAYTAlVTMQ4wDAYDVQQIDAVVbnNldDEOMAwGA1UEBwwFVW5zZXQxDjAMBgNVBAoMBVVuc2V0MRgwFgYDVQQDDA93d3cuZXhhbXBsZS5jb20CAQEwCwYJYIZIAWUDBAIBMA0GCSqGSIb3DQEBAQUABIIBAArPDkG655DH4iv1yNwvEDnMvUs-1zZRBNqh22OsVBDV5MPgMbLDOrBDmvrczRD34Pt6tfAlRFZzGk-YSJV1z03Lx48EffRK2PwW3FTybrH54tfAmHkeQjZt+NUnpgDq2g0-uQLwafjJqMPpXps7--VO3ZLHjeDV6HHCtUZHCnzRC049jtgV50+gXUHXdPCcTJyZKmM6OsqU7r5tn8zonoszX6ZfH5snNZKT7ozXmLNCY4itUbUaXvgMhfPm1saXHsIiqpZc1067YULi5eSroR19n0hd25a5PrTEXgO9YWmluBm-cC4kQZufuLWS4TGQyGY0QyV-10FJ6EJ8JBF9ysw='

echo  "tenants  list  #######################################################"

# curl -i -X GET http://10.66.32.18:35357/v2.0/tenants -H "User-Agent: python-keystoneclient" -H "X-Auth-Token: $token"
# curl -i -X GET http://10.66.32.18:35357/v2.0/endpoints -H "User-Agent: python-keystoneclient" -H "X-Auth-Token: $token"

curl -i -X GET -H 'User-Agent: python-ceilometerclient' -H "Content-Type:application/json"  -H "Accept:application/json" -H "X-Auth-Token:$token"   http://10.66.32.18:8777/v2/meters 
