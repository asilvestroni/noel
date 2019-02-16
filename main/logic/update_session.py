import main.models as models
import main.logic.common.const as const


def next_session_status(session: models.Session, step: str = '', progress: float = 0):
    sn_count = session.socialtoken_set.count()
    if session.stage == const.session_statuses['wait']:
        session.stage = const.session_statuses['gather']
        status = 'Acquisizione immagini da Social Network'
    elif session.stage == const.session_statuses['gather']:
        if step == 'final':
            session.stage = const.session_statuses['process']
            status = 'Processing immagini'
        else:
            session.progress += progress / (100 * sn_count) * 10
            status = 'Acquisizione immagini da {}'.format(step)
    elif session.stage == const.session_statuses['process']:
        if step == 'final':
            session.stage = const.session_statuses['cluster']
            status = 'Clustering immagini'
        else:
            session.progress += progress / (100 * (sn_count + 1)) * 70
            status = 'Processing immagini {}'.format(step)
    elif session.stage == const.session_statuses['cluster']:
        if step == 'final':
            session.stage = const.session_statuses['done']
            status = 'Completata'
        else:
            session.progress += progress / (100 * (sn_count + 1)) * 20
            status = 'Clustering immagini {}'.format(step)
    else:
        status = 'status non valido'

    session.status = status
    session.save()
    return status
