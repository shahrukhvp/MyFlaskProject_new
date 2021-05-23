
def make_api_call(shod_api, ip):
    import requests
    api_url = "https://api.shodan.io/shodan/host/" + ip + "?key=" + shod_api
    # print(api_url)
    try:
        r = requests.get(api_url)
        if r.status_code == 200:
            return ('success', r.status_code, r.json())
        else:
            return ('failed', r.status_code, None)
    except Exception as e:
        print("Exception on making API request")
        # print(e.message, e.args)
        print(e)
    finally:
        ("make_api_call() finished")


# MAIN :
my_shod_api = "zz5EMMQEyRyW6MSDnDmKheyTqDEhtbvk"
my_ip = "156.250.25.187"
# Making API Call to Shodan
status, status_code, response_json = make_api_call(my_shod_api, my_ip)
print("make_api_call() {} with status code {}".format(status, status_code))

print("response_json is a {} with {} keys".format(type(response_json), len(response_json)))
print("The keys are: {}".format(list(response_json.keys())))

# Lets PARSE the json now:
port_list = list(response_json['ports'])  # eg:- [80,443,667]
print("ports list: {}".format(port_list))
main_data = response_json['data']
print("main_data is a {} with {} items".format(type(main_data), len(main_data)))
print("Each item in main_data is a {} with : {} keys".format(type(main_data[0]), len(main_data[0])))
print("The keys are: {}".format(list(main_data[0].keys())))
print("Please note we have vulns inside this")
temp = list()
try:
    result_dict = dict()

    print("we have {} items inside main_data - one for each port number".format(len(main_data)))
    for item in main_data:
        port_num = item['port']
        print("iteration for {}".format(port_num))
        try:
            # vulns.append(item['vulns'])
            temp = item['vulns']
            # print("temp : {}".format(temp))
            temp_cves = list()
            for cve in temp:
                # print(temp[cve]['cvss'])
                # print(item[cve])
                temp_cves.append([cve, temp[cve]['cvss']])
            result_dict[port_num] = [port_num, len(temp_cves), temp_cves, 'Vulnerable']

        except:
            result_dict[port_num] = [port_num, 0, [], 'Not Vulnerable']

    # Print results:
    print("Port#, CVE_Count, CVE List with CVSS Score, Verdict ")
    for item in result_dict:
        print(result_dict[item])

except Exception as e:
    print(e)