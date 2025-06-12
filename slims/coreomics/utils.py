import urllib.request, json
from django.conf import settings
from .models import Submission
from datetime import date, timedelta
from django.utils import timezone

def import_submissions(days=30):
    exclude_types = getattr(settings, 'EXCLUDE_SUBMISSION_TYPES', [])
    last_updated = date.today() - timedelta(days=days)
    # TODO: change this to filtering by updated, not submitted date in order to catch updates in submission.  Need to make this filter (updated__date__gte) available in Coreomics first....
    url = '{base_url}/server/api/submissions/?page=1&page_size=100&lab=dnatech&submitted__date__gte={last_updated}'.format(base_url=settings.COREOMICS_BASE_URL, last_updated=str(last_updated)) #updated__date__gte={last_updated}
    imported = []
    while url:
        print(url)
        req = urllib.request.Request(url)
        req.add_header('Authorization', 'Token {token}'.format(token=settings.COREOMICS_TOKEN))
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        # updated = []
        for submission in data['results']: #do something with submissions
            if submission['type']['id'] not in exclude_types and submission['type']['prefix'] not in exclude_types:
                instance = Submission.import_submission(submission)
                imported.append(instance)
        url = data['next']
    print('{} submissions imported or updated'.format(len(imported)))

def import_submission(id):
    url = '{base_url}/server/api/submissions/{id}/'.format(base_url=settings.COREOMICS_BASE_URL, id=id) #updated__date__gte={last_updated}
    print(url)
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'Token {token}'.format(token=settings.COREOMICS_TOKEN))
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    submission = Submission.import_submission(data)
    return submission

def link_share(submission, share):
    url = '{base_url}/server/api/plugins/bioshare/submissions/{submission_id}/submission_shares/import_share/'.format(base_url=settings.COREOMICS_BASE_URL,submission_id=submission.id)
    data = { "url": share.url }
    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data=params)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Token {token}'.format(token=settings.COREOMICS_TOKEN))
    try:
        response = urllib.request.urlopen(req)
    except urllib.request.HTTPError as e:
        error_message = e.read()
        raise Exception(error_message)
    return response

# def create_note(submission, text):
#     url = '{base_url}/server/api/notes/'.format(base_url=settings.COREOMICS_BASE_URL)
#     data = {"type":"NOTE","submission":submission.id,"send_email":True,"email_participants":False,"public":True,"edit":True,"parent":None,"text":text}
#     params = json.dumps(data).encode('utf8')
#     req = urllib.request.Request(url, data=params)
#     req.add_header('Content-Type', 'application/json')
#     req.add_header('Authorization', 'Token {token}'.format(token=settings.COREOMICS_TOKEN))
#     response = urllib.request.urlopen(req)
#     data = json.loads(response.read())
#     return data

def send_note(note_or_id):
    from .models import Note
    if isinstance(note_or_id, Note):
        note = note_or_id
    elif isinstance(note_or_id, int):
        try:
            note = Note.objects.get(id=note_or_id)
        except Note.DoesNotExist:
            print("Instance with given ID does not exist.")
            return
    print('Creating note: ' + note.text)
    url = '{base_url}/server/api/notes/'.format(base_url=settings.COREOMICS_BASE_URL)
    data = {"type":"NOTE","submission":note.submission.id,"send_email":True,"email_participants":settings.COREOMICS_EMAIL_PARTICIPANTS,"public":True,"edit":True,"parent":None,"text":note.text}
    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data=params)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Token {token}'.format(token=settings.COREOMICS_TOKEN))
    response = urllib.request.urlopen(req)
    note.data = json.loads(response.read())
    note.coreomics_id = note.data['id']
    note.sent = timezone.now()
    note.save()
    return note.data

def format_note(note, submission, data_directories=[]):
    share_url = submission.share.url if hasattr(submission, 'share') else ''
    data_url_template = share_url + '{repository_subpath}'
    data_urls = '\n'.join([data_url_template.format(repository_subpath=d.repository_subpath) for d in data_directories])
    return note.format(data_urls=data_urls, share_url=share_url)