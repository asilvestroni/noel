from celery import shared_task

import main.logic.common.const as const
from main.models import Session


@shared_task
def next_session_status(session_id: str, step: str = '', progress: float = 0):
    session = Session.objects.get(id=session_id)
    sn_count = session.socialtoken_set.count()
    if session.stage == const.session_statuses['wait']:
        session.stage = const.session_statuses['gather']
        status = 'Acquisizione immagini da Social Network'
    elif session.stage == const.session_statuses['gather']:
        if step == 'final':
            session.stage = const.session_statuses['process']
            status = 'Processing immagini'
        else:
            session.progress += (progress / sn_count * 20)
            status = 'Acquisizione immagini da {}'.format(step)
    elif session.stage == const.session_statuses['process']:
        if step == 'final':
            session.stage = const.session_statuses['cluster']
            status = 'Clustering immagini'
        else:
            session.progress += (progress / (sn_count + 1) * 70)
            status = 'Processing immagini {}'.format(step)
    elif session.stage == const.session_statuses['cluster']:
        if step == 'final':
            session.stage = const.session_statuses['done']
            session.progress = 100
            status = 'Completata'
        else:
            session.progress += (progress / sn_count * 10)
            status = 'Clustering immagini {}'.format(step)
    else:
        status = 'status non valido'

    session.status = status
    session.save()
    return status
