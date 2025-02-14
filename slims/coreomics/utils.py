import urllib.request, json
from django.conf import settings
from .models import Submission
from datetime import date, timedelta

def import_submissions(days=30):
    last_updated = date.today() - timedelta(days=days)
    url = '{base_url}/server/api/submissions/?page=1&page_size=100&lab=dnatech&updated__date__gte={last_updated}'.format(base_url=settings.COREOMICS_BASE_URL, last_updated=str(last_updated))
    imported = []
    while url:
        print(url)
        req = urllib.request.Request(url)
        req.add_header('Authorization', 'Token {token}'.format(token=settings.COREOMICS_TOKEN))
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        # updated = []
        for submission in data['results']: #do something with submissions
            instance = Submission.import_submission(submission)
            imported.append(instance)
        url = data['next']
    print('{} submissions imported or updated'.format(len(imported)))