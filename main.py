from cpapi import APIClient, APIClientArgs

smart_console_host = ''
smart_console_login = ''
smart_console_password = ''
layer = ''

disabled_rules = []

def api_request_handler(smart_console_host, smart_console_login, smart_console_password, api_request, layer, disabled_rules):
    client_args = APIClientArgs()
    client_args = APIClientArgs(server = smart_console_host)
    with APIClient(client_args) as client:
        client = APIClient(client_args)
        if client.check_fingerprint() is False:
            print ('Fingerprint failed!')
            exit(1)
        else:
            login = client.login(smart_console_login, smart_console_password)
            if api_request == 'set-access-rule':
                for rule in disabled_rules:
                    uid = rule['uid']
                    client.api_call(api_request, {'layer':layer, 'uid':uid, 'new-position': {'below':'Disabled Rules'}})
                publish = client.api_call('publish')
                client.api_call('logout', {})
                return True
            elif api_request == 'show-access-rulebase':
                output_rulebase = client.api_call('show-access-rulebase', {'name':layer})
                publish = client.api_call('publish')
                client.api_call('logout', {})
                api_response_data = output_rulebase.data
                return False, api_response_data

break_point = False

while True:
    if break_point == False:
        output = api_request_handler(smart_console_host, smart_console_login, smart_console_password, 'show-access-rulebase', layer, disabled_rules)
        rules = output[1]['rulebase']
        for i in rules:
            if i.get('enabled') is False:
                disabled_rules.append({'uid': i['uid']})
        break_point = True

    elif break_point == True:
        output = api_request_handler(smart_console_host, smart_console_login, smart_console_password, 'set-access-rule', layer, disabled_rules)
        break
