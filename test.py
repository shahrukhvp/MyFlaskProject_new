
def make_api_call(district_id, date):
    import requests
    host = "cdn-api.co-vin.in"
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': 'https://www.cowin.gov.in',
            'Connection': 'close',
            'Referer': 'https://www.cowin.gov.in/'}

    api_url ="https://" + host + r"/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + district_id +"&date=" + date
    #print(api_url)
    #url_orig = r"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=305&date=22-05-2021"
    #print(url_orig)
    try:
        r = requests.get(api_url,headers=headers)
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


date = "23-05-2021"
district_id = {
            "1": ["297", "Kannur"],
            "2": ["305", "Kazhikode"],
            "3": ["295", "Kasaragode"]}
print( "1 : Kannur, 2: Kozhikode, 3: Kasaragode")
user_input = input()

# Making API Call to COWIN
status, http_resp_code, response_json = make_api_call(district_id[user_input][0], date)
print("make_api_call() {} with status code {}".format(status, http_resp_code))

#print("response_json is a {} with {} keys".format(type(response_json), len(response_json)))
if type(response_json) == type.__dict__:
    print("The keys are: {}".format(list(response_json.keys())))
#print(response_json)
if (len(response_json['centers']) == 0):
    print("no centers available in {}".format(district_id[user_input][1]))
if response_json['centers']:
    centers = response_json['centers']
    print (len(centers))
    print("Total Centers available in {}: {}".format(district_id[user_input][1], len(centers)))

    for a_center in centers:
        flag_18 = False
        flag_45 = False
        list_of_param = list(a_center.keys())
        '''
        for item in list_of_param:
            print("{} : {}".format(item, a_center[item]))
        '''
        #break
        print("{} | available dose: {} | {} | age: {}+ | Vaccine: {} - Center: {}".format(a_center['district_name'], a_center['sessions'][0]['available_capacity'], a_center['fee_type'], a_center['sessions'][0]['min_age_limit'], a_center['sessions'][0]['vaccine'], a_center['name']))
        if (a_center['sessions'][0]['min_age_limit'] == 18 and a_center['sessions'][0]['available_capacity'] >0):
            print("Vaccine available for 18+ category at {}".format(a_center['name']))
            flag_18 = True
        if (a_center['sessions'][0]['min_age_limit'] == 45 and a_center['sessions'][0]['available_capacity'] >0):
            print("Vaccine available for 45+ category at {}".format(a_center['name']))
            flag_45 = True

    print("\n--------------------------------------------------")
    if flag_18 == True:
        print("Vaccine slots available for 18+ category")
    else:
        print("Vaccine slots NOT available for 18+ category")
    if flag_45 == True:
        print("Vaccine slots available for 45+ category")
    else:
        print("Vaccine slots NOT available for 45+ category")
    print("--------------------------------------------------")

