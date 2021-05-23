import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

import shodan
import sys
from retry import retry

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        #url = f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        url = f"https://api.shodan.io/shodan/host/{urllib.parse.quote_plus(symbol)}?key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"],
            "ip": quote["ip"],
            "country_code": quote["countryCode"]
        }
    except (KeyError, TypeError, ValueError):
        return None


# def usd(value):
#     """Format value as USD."""
#     return f"${value:,.2f}"


def apicall(ip):
    """Look up IP."""

    SHODAN_API_KEY = os.environ.get("API_KEY")
    api = shodan.Shodan(SHODAN_API_KEY)

    # retry decorator to handle timeouts searching vulns
    @retry()
    def exploit(query):
        return api.exploits.search(query)

    #query = sys.argv[0]
    try:
        # search Shodan
        #results = api.host({ip})
        results = f"https://api.shodan.io/shodan/host/{urllib.parse.quote_plus(ip)}?key={SHODAN_API_KEY}"

        # print host details
        # for k in results:
        #     if str(k) != 'data': # data is verbose
        #         print(str(k).rjust(15) + ' : ' + str(results[k]))
        response = requests.get(results)
        response.raise_for_status()

        # # get site titles from 'data' dictionary
        # for k in results['data']:
        #     if 'title' in k:
        #         print('\nPort %-5s Title: %s' % (k['port'], k['title']))
        # # vulnerabilities
        # if 'vulns' in results:
        #     for i in results['vulns']:
        #         # some return !CVE-* for explicilty not vulnerable
        #         if not i.startswith('!'):
        #             vulns = exploit(i)
        #             print('\033[1m' # bold
        #                 + '\n**********\tVULNERABILE to '
        #                 + i
        #                 + '\t**********\n'
        #                 + '\033[0m'# end bold
        #                 )
        #             # return Descriptions & Related CVE's
        #             for v in reversed(vulns['matches']):
        #                 if v['cve'][0] == i:
        #                     print('\033[1m%s\033[0m' % v['cve'][0])
        #                 else:
        #                     print('\033[1mRelated\033[0m - %s' % v['cve'][0])
        #                 print(str(v['description']).replace('. ', '.\n'))
        #                 print()
        #response = requests.get(results)
        #response.raise_for_status()
    except shodan.APIError as e:
        print('Error: %s' % e)

    #Parse response
    try:
        search = response.json()
        return {
            "ip_str": search["ip_str"],
            "region_code": search["region_code"],
            "postal_code": search["postal_code"],
            "country_code": search["country_code"],
            "city": search["city"],
            "dma_code": search["dma_code"],
            "last_update": search["last_update"],
            "org": search["org"],
            "country_name": search["country_name"],
            "tags": search["tags"],
            "area_code": search["area_code"],
            "latitude": search["latitude"],
            "longitude": search["longitude"],
            "hostnames": search["hostnames"],
            "org": search["org"],
            "asn": search["asn"],
            "isp": search["isp"],
            "domains": search["domains"],
            "os": search["os"],
            "ports": search["ports"],
            "isp": search["isp"],
        }
    except (KeyError, TypeError, ValueError):
        return None