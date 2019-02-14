# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
#  Tests data consistency for Session data endpoint
# ----------------------------
from io import BytesIO

from django.test import Client, TestCase

from main.models import Session


class SessionTestCase(TestCase):
    session: Session
    client: Client

    def setUp(self):
        self.session = Session.objects.create(id='a_new_session_id')
        self.client = Client()

    def test_session_has_all_fields(self):
        response = self.client.get('/sessions/{}/data'.format(self.session.id))
        data = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual('a_new_session_id', data['id'])
        self.assertEqual(0, data['progress'])
