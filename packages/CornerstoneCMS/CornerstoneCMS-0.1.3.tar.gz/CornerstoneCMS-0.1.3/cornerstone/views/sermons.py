from flask import Blueprint, current_app, request

from cornerstone.models import Sermon
from cornerstone.sphinxapi import SphinxClient
from cornerstone.theming import render

sermons = Blueprint('sermons', __name__)


class SermonsPage(object):
    title = 'Sermons'
    slug = 'sermons'


class SermonPage(object):
    title = 'Sermon'
    slug = 'sermon'


@sermons.route('/sermons', methods=['GET'])
def list():
    try:
        page_number = int(request.args.get('page', 1))
    except (ValueError, TypeError):
        page_number = 1
    query = Sermon.query
    if request.args.get('q', None):
        client = SphinxClient()
        client.SetServer(current_app.config.get('SPHINX_HOST', 'localhost'), current_app.config.get('SPHINX_PORT'))
        results = client.Query(request.args.get('q'))
        if results:
            query = query.filter(Sermon.id.in_([m['id'] for m in results['matches']]))
    pagination = query.order_by(Sermon.date.desc()).paginate(page=page_number, per_page=5)
    page = SermonsPage()
    return render('sermons.html', pagination=pagination, page=page)


@sermons.route('/sermons/<id>', methods=['GET'])
def get(id):
    sermon = Sermon.get(id)
    page = SermonPage()
    return render('sermon.html', sermon=sermon, page=page)
