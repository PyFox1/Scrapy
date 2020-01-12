
import re
import datetime

from cheetah_server.models.ScrapedRun import ScrapedRun
from cheetah_server.server import create_app, db

def modify_item(item):

    if '-' in item['date']:
        splitted_dates = item['date'].split()
        date2 = datetime.datetime.strptime(splitted_dates[2], '%d.%m.%y')
        day_date1 = int(splitted_dates[0].replace('.', ''))
        date1 = datetime.datetime(date2.year, date2.month, day_date1)
        item['date'] = [date1, date2]
    else:
        item['date'] = [datetime.datetime.strptime(item['date'],  '%d.%m.%y')]


    distance = []
    for element in item['event']:
        if element == 'Marathon':
            distance.append(42.195)
        elif element == 'Halbmarathon':
            distance.append(21.0975)
        elif element == '10 Km':
            distance.append(10)

    item['distance'] = distance

    test = item['country_list']

    for country in item['country_list']:
        if country.strip() in ["Deutschland", "Österreich", "Schweiz"]:
            item['country'] = country

    # modifiy zip and city
    location = item['location']
    if str(location).strip():
        plz_ger = re.compile(r'[0-9]+').findall(str(location))
        plz_ger1 = re.compile(r'[0]{1}[1-9]{1}[0-9]{3}').findall(str(location))
        plz_ger2 = re.compile(r'[1-9]{1}[0-9]{1}[0-9]{3}').findall(str(location))
        item['zip'] = int(plz_ger[0])

        location = str(location).replace(")", "").replace("(", "").replace(",", "").replace("'", "")
        item['city'] = re.compile(r'(([a-zäöüß]+\s?)+)$', re.IGNORECASE).search(location).group()

    item['event'] = ';'.join(item['event'])
    item['name'] = ';'.join(item['name'])

    run_scraped = ScrapedRun(**item)
    app = create_app()
    app.app_context().push()
    db.session.add(run_scraped)
    db.session.commit()

    return item