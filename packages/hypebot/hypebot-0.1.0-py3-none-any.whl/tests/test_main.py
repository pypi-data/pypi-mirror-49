from unittest import TestCase
from unittest.mock import MagicMock, patch

from hypebot import main


class TestHypebot(TestCase):
    @patch("hypebot.main.create_twitter_api")
    def test_create_twitter_api(self, twitter):
        main.create_twitter_api()

    def test_update_tweet(self):
        livesplit_client = MagicMock()
        livesplit_client.post.side_effect = ["7", "−1:11"]
        twitter = MagicMock()
        main.update(livesplit_client, twitter, 6, "name", 7)
        self.assertTrue(twitter.PostUpdate.called)

    def test_update_no_tweet(self):
        livesplit_client = MagicMock()
        livesplit_client.post.side_effect = ["7", "13"]
        twitter = MagicMock()
        main.update(livesplit_client, twitter, 6, "name", 7)
        self.assertFalse(twitter.PostUpdate.called)
