from eppzy.bases import ObjectDoesNotExist, AuthorizationError


def _contact_create_kwargs(contact_info):
    d = contact_info.data.copy()
    del d['roid']
    d['contact_id'] = d.pop('id')
    d['password'] = 'autocopy'
    return d


def _domain_create_kwargs(domain_info):
    d = domain_info.data.copy()
    for k in ('roid', 'host', 'crDate', 'exDate'):
        del d[k]
    return d


def _host_create_kwargs(host_info):
    d = host_info.data.copy()
    del d['roid']
    return d


info_create_map = {
    'contact': _contact_create_kwargs,
    'domain': _domain_create_kwargs,
    'host': _host_create_kwargs
}


class Overlay:
    def __init__(self, rw, ro, create_kwargs):
        self._rw = rw
        self._ro = ro
        self._create_kwargs = create_kwargs

    def info(self, *a, **k):
        try:
            return self._rw.info(*a, **k)
        except (ObjectDoesNotExist, AuthorizationError):
            ro_info = self._ro.info(*a, **k)
            self._rw.create(**self._create_kwargs(ro_info))
            return self._rw.info(*a, **k)

    def __getattr__(self, attr):
        return getattr(self._rw, attr)


def overlayed(rw_session, ro_session):
    r = {}
    for k in set(rw_session) & set(ro_session) & set(info_create_map):
        r[k] = Overlay(rw_session[k], ro_session[k], info_create_map[k])
    return r
