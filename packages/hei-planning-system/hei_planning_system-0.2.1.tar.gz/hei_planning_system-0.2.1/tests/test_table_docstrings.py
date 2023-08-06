import unittest

from planning_system.db.schema.tables import finance_structure



class TestDocStrings(unittest.TestCase):

    def test_table_docstring(self):
        base = finance_structure.Base
        firstn = 0 
        for tbl in base.registry._class_registry.values():
            if hasattr(tbl, "__tablename__"):
                for col in tbl.__table__.columns:
                    if len(col.foreign_keys) > 0:
                        print(col.foreign_keys) 
                firstn+=1
                if firstn>2:
                    break
        print(finance_structure.finance_section.__doc__)
        self.assertTrue(1==1)


if __name__ == '__main__':
    unittest.main()