from django.test import TestCase

from src.python.db.current import Current


class CurrentTests(TestCase):




    def test_current_init(self):
        current = Current(10, 'abracadabra', 'USD', 1545254453, 1554443238, 14850, 1)
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)
