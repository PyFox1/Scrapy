
import re
import datetime

from cheetah_server.models.ScrapedRun import ScrapedRun
from cheetah_server.server import create_app, db

def modify_item(item):

    #date
    if '-' in item['date']:
        splitted_dates = item['date'].split()
        date2 = datetime.datetime.strptime(splitted_dates[2], '%d.%m.%y')
        item['date'] = date2
    else:
        item['date'] = datetime.datetime.strptime(item['date'],  '%d.%m.%y')

    #distances
    distances = []
    for element in item['event']:
        if element == 'Marathon':
            distances.append(42.195)
        elif element == 'Halbmarathon':
            distances.append(21.0975)
        elif element == '10 Km':
            distances.append(10)
    item['distances'] = distances

    #zip_code, city, country
    location = item['location']
    if str(location).strip():
        #zip_code
        zip_code = re.compile(r'[0-9]+').findall(str(location))

        item['zip_code'] = int(zip_code[0]) if zip_code else ''

        #city
        location = str(location).replace(")", "")\
                                .replace("(", "")\
                                .replace(",", "")\
                                .replace("'", "")
        city_group = re.compile(r'(([a-zäöüß]+\s?)+)$', re.IGNORECASE).search(location)
        item['city'] = city_group.group() if city_group else ''


        #country
        for element in item['address_list']:
            if element.strip() in ["Deutschland", "Österreich", "Schweiz"]:
                item['country'] = element

        if 'country' not in item:
            country_group = re.compile(r'^((CH)|(A))(\s)', re.IGNORECASE | re.VERBOSE).search(str(location))
            if country_group:
                country = country_group.group(1)
                if country == "A":
                    item['country'] = "Österreich"
                elif country == "CH":
                    item['country'] = "Schweiz"
            else:
                item['country'] = ''

    # add source
    item['source'] = 'spider5'

    # only workaround, relational models neccessary
    item['event'] = ';'.join(item['event'])
    item['name'] = ';'.join(item['name'])
    item['distances'] = ';'.join([str(item) for item in item['distances']])

    item.pop('location')
    item.pop('address_list')
    item.pop('event')

    run_scraped = ScrapedRun(**item)
    app = create_app()
    app.app_context().push()
    db.session.add(run_scraped)
    db.session.commit()

    return item
