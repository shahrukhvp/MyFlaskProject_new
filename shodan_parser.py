import requests

def make_api_call(shod_api,ip):
    api_url = "https://api.shodan.io/shodan/host/"+ip+"?key="+shod_api
    #print(api_url)
    try:
        r = requests.get(api_url)
        if r.status_code == 200:
            return('success', r.status_code,r.json())
        else:
            return('failed', r.status_code, None)
    except Exception as e:
        print("Exception on making API request")
        #print(e.message, e.args)
        print(e)
    finally:
        ("make_api_call() finished")

#MAIN :
my_shod_api = "zz5EMMQEyRyW6MSDnDmKheyTqDEhtbvk"
my_ip = "156.250.25.187"
# Making API Call to Shodan
status, status_code, response_json = make_api_call(my_shod_api, my_ip)
print("make_api_call() {} with status code {}".format(status, status_code))

print("response_json is a {} with {} keys".format( type(response_json), len(response_json) ))
print("The keys are: {}".format(list(response_json.keys())))

# Lets PARSE the json now:
port_list = list(response_json['ports'])  # eg:- [80,443,667]
print("ports list: {}".format(port_list))
main_data = response_json['data']
print("main_data is a {} with {} items".format(type(main_data), len(main_data) ))
print( "Each item in main_data is a {} with : {} keys".format(type(main_data[0]), len(main_data[0]) ))
print("The keys are: {}".format(list(main_data[0].keys())))
print("Please note we have vulns inside this")
temp = list()
try:
    # get vulns into a list: return a blank list if vulns does not exist - means port is not vulnerable
    vulns_list = list()
    port_list = list()
    cves_list = list()
    result_dict = dict()

    print("we have {} items inside main_data - one for each port number".format(len(main_data)))
    for item in main_data:
        port_num = item['port']
        print("iteration for {}".format(port_num))
        try:
            #vulns.append(item['vulns'])
            temp = item['vulns']
            #print("temp : {}".format(temp))
            temp_cves = list()
            for cve in temp:
                #print(temp[cve]['cvss'])
                #print(item[cve])
                temp_cves.append([cve, temp[cve]['cvss']])
            result_dict[port_num] = [port_num, len(temp_cves), temp_cves]

        except:
            result_dict[port_num] = [port_num, 0, []]

    #PRint results:
    print("Port#, CVE_Count, CVE List with CVSS Score ")
    for item in result_dict:
        print(result_dict[item])




    '''
    for item in vulns:
        keys = item.keys()
        my_white_listed_set = ['cvss']
        result_set = list()
        for i in item:
            print(item[i].keys())
            result_set.append ([value for key, value in item[i].items() if key in my_white_listed_set])
        print("{}".format(result_set))
        break
    '''
except Exception as e:
    print(e)
'''

# Get vulnerable ports
vuln_ports = list()
for i, item in enumerate(port_list):
    if vulns[i] is not None:
        if len(vulns[i]) == 0:
            vuln_ports.append(item)
        print("Port {} has {} vulns -- {}".format(item, len(vulns[i]), list(vulns[i])))
    else:
        print("Something wrong - VULNS is None")
        


port_to_vulns = []
for i, item in enumerate(port_list):
    port_to_vulns.append([port_list[i], len(vulns[i]), vulns[i]])

for item in port_to_vulns:
    print("{} - {} - {}".format(item[0], item[1], item[2]))

#port_list = filter(None, port_list)
#info = filter(None, info)

print("Ports Open : {}".format(port_list))
print("Ports Vulnerable : {}".format(vuln_ports))

'''
'''

Vuln_Stats__ports = port
Vuln_Stats__vulns = vulns
Vuln_Stats__port_to_vulns = port_to_vulns
Vuln_Stats__info = info
Vuln_Stats__vuln_ports = vuln_ports
except:
print("Exception occurred")
try:
port_to_vulns = Vuln_Stats__port_to_vulns
# phantom.debug(port_to_vulns)

string = ""
count = 0

# phantom.debug("port_to_vulns has {}".format(len(port_to_vulns)))

cvss_list = []
for i, item in enumerate(port_to_vulns):
    # get CVE raw data for a PORT:
    temp = item[1]
    # get port number:
    my_port = item[0]
    if temp is None:
        port_to_vulns[i] = [my_port, '-', '-', '-']
        # phantom.debug(port_to_vulns[i])
        phantom.debug("Port # {} has no vulns".format(my_port))
        continue
    # phantom.debug(temp)
    phantom.debug("Port # {} has {} vulns".format(my_port, len(temp)))
    # for item in temp:
    count = 0
    cve_dict = dict()

    for n, cve in enumerate(temp):
        # phantom.debug(cve)
        # phantom.debug(temp[cve]['cvss'])
        cve_dict[cve] = [my_port, cve, temp[cve]['cvss'], temp[cve]['summary']]
        cvss_list.append(temp[cve]['cvss'])
        # phantom.debug("Port # - {}CVSE - {}CVSS - {}Summary - {}".format(my_port, cve, temp[cve]['cvss'], temp[cve]['summary']))
        string += "<p><b>------------------------------------------------------------------------------------------------</b></p> <p><b>CVE # -</b>  {}</p> <p><b>CVSS   -</b>    {}</p> <p><b>Port # -</b> {}</p> <p><b>Summary - </b>{}</p>".format(
            cve, temp[cve]['cvss'], my_port, temp[cve]['summary'])
        # string += "Port # - {}CVE - {}CVSS - {}".format(my_port, cve, temp[cve]['cvss'])
        # string += "{}".format( temp[cve]['summary'])
        count += 1

    port_to_vulns[i] = [my_port, cve_dict, count]

# remove None values from cvss_list:
cvss_list = filter(None, cvss_list)
cve_count = len(cvss_list)

'''

