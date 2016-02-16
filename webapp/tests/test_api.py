import falcon
from falcon import testing

class TestRouting(testing.TestBase):
    
    def test_get_list_of_journals(self):
        body = self.simulate_request('/v1/journals', decode='utf-8', method='GET')
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
    
    def test_add_journal(self):
        document = {
            'created': 1455492635225.0,
            'title': "Australian Journal of Education",
            'updated': None
        }
        body = self.simulate_request('/v1/journals', decode='utf-8', method='POST', body=json.dumps(document))
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
    
    def test_display_journal(self):
        body = self.simulate_request('/v1/journals', decode='utf-8', method='GET', query_string='id=56c282eb3b23eaf551c92029')
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
    
    def test_update_journal(self):
        document = {
            'created': 1455492635225.0,
            'title': "Australian Journal of Education",
            'updated': None
        }
        body = self.simulate_request('/v1/journals', decode='utf-8', method='PUT', body=json.dumps(document), query_string='id=56c282eb3b23eaf551c92029')
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

    def test_remove_journal(self):
        body = self.simulate_request('/v1/journals', decode='utf-8', method='DELETE', query_string='id=56c282eb3b23eaf551c92029')
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

    def test_suggest_journal(self):
        body = self.simulate_request('/v1/journals/suggest', decode='utf-8', method='GET', query_string='q=Austra')
        self.assertEqual(self.srmock.status, falcon.HTTP_200)



