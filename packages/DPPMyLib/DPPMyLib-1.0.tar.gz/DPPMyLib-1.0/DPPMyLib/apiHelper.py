def print_hi(minPop):
    import requests

    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"

    querystring = {"minPopulation": minPop}

    headers = {
        'x-rapidapi-key': "c94b07d5fcmsh192324421c65896p1d93d1jsna064f463a452",
        'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)