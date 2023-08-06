from eppzy.rfc5733_contact import Contact
from eppzy.rfc5731_domain import Domain
from eppzy.rfc5732_host import Host
from eppzy.test_utils import overlayed
from eppzy.session import RequestWrapper

from util import mocked_session, data_file_contents


def test_overlayed():
    rw_check_count = 0

    def rw_checks(body):
        nonlocal rw_check_count
        rw_check_count += 1
        if rw_check_count == 1:
            assert b'info' in body
            return data_file_contents('rfc5730/obj_does_not_exist.xml')
        elif rw_check_count == 2:
            assert b'create' in body
            return data_file_contents('rfc5733/contact_create_example.xml')
        elif rw_check_count == 3:
            assert b'info' in body
            return data_file_contents('rfc5733/contact_info_example.xml')
        elif rw_check_count == 4:
            assert b'update' in body
            return data_file_contents('rfc5733/contact_update_example.xml')
        else:
            raise AssertionError('More requests made to rw than expected')

    def ro_checks(body):
        assert b'info' in body
        return data_file_contents('rfc5733/contact_info_example.xml')
    with mocked_session(rw_checks, [Contact]) as rws:
        with mocked_session(ro_checks, [Contact]) as ros:
            o = overlayed(rws, ros)
            r = o['contact'].info('cid', 'passable')
            assert r.data['city'] == 'Dulles'
            assert rw_check_count == 3
            o['contact'].update(r.data['id'], city='Interestes')


def _overlay_basic_checks(cls, info_path, create_path):
    rw_check_count = 0

    def rw_checks(body):
        nonlocal rw_check_count
        rw_check_count += 1
        if rw_check_count == 1:
            assert b'info' in body
            return data_file_contents('rfc5730/obj_does_not_exist.xml')
        elif rw_check_count == 2:
            assert b'create' in body
            return data_file_contents(create_path)
        if rw_check_count == 3:
            assert b'info' in body
            return data_file_contents(info_path)
        raise AssertionError('More rw requests than expected')

    def ro_checks(body):
        assert b'info' in body
        return data_file_contents(info_path)

    with mocked_session(rw_checks, [cls]) as rws:
        with mocked_session(ro_checks, [cls]) as ros:
            overlayed(rws, ros)[cls.name].info('example.com')
    assert rw_check_count == 3


def test_domain_overlay():
    _overlay_basic_checks(
        Domain, 'rfc5731/domain_info_full_example.xml',
        'rfc5731/create_example.xml')


def test_host_overlay():
    _overlay_basic_checks(Host, 'rfc5732/info.xml', 'rfc5732/create.xml')
