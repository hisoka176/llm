from unittest import TestCase

from src.service.hive_table import HiveTable


class Test(TestCase):
    def test_hive_table(self):
        hive_table = HiveTable()
        results = hive_table.get_hive_table_by_query("次留计算")
        print(results)

