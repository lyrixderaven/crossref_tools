from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel
from habanero import Crossref

SCIHUB_URL = "http://sci-hub.tw"

import logging

@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    references = []
    if 'DOI' in request.GET:
        doi = request.GET['DOI']
        cr = Crossref()
        logging.info(request.GET)
        # try:
        x = cr.works(doi)
        if 'message' in x and 'reference' in x['message']:
            if 'title' in x['message']:
                logging.info(u"Evaluating references for {}".format(x['message']['title']))
            for r in x['message']['reference']:
                if 'DOI' not in r:
                    continue

                title = ""
                year = ""

                try:
                    y = cr.works(u'{}'.format(r['DOI']))
                    logging.info(r['DOI'])

                    if 'message' in y and 'title' in y['message']:
                        title = u"{}".format(u''.join(y['message']['title']))
                    if 'message' in y and 'author' in y['message']:
                        title += u"\n" + u", ".join([a['family'] for a in y['message']['author']])
                    if 'message' in y and 'issued' in y['message']:
                        year = y['message']['issued']['date-parts'][0][0]
                except:
                    if 'unstructured' in r:
                        title = u"{}".format(r['unstructured'])

                logging.info(title)
                references.append([
                    u"{}/{}".format(SCIHUB_URL,r['DOI']),
                    title,
                    ##authors,
                    year])
        # except:
        #     pass
    logging.info(references)
    return {'refs': references}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_crossref_tools_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
