from unittest import TestCase

from src.base import Flow


class TestFlow(TestCase):
    def test_flow(self):
        flow = Flow()
        flow.flow("主软dau")
