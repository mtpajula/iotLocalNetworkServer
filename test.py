import unittest
from IotServerDevice import *


class Test(unittest.TestCase):

    def setUp(self):
        '''
        Sets up the initial state for all the test cases.
        '''
        self.d = IotServerDevice()

    def test_db_get_id(self):
        dbos = self.d.db.con.get('command',1)
        self.assertEqual("otsikko" , dbos[0].device, "db get(id) failed")

    def test_db_put(self):
        newp = "test put"
        dbo  = self.d.db.con.getDbo()
        dbo.id      = 1
        dbo.device  = "otsikko"
        dbo.payload = newp
        self.d.db.con.put('command', dbo)

        dbos = self.d.db.con.get('command',1)

        self.assertEqual(newp , dbos[0].payload, "db put failed")

    def test_delete(self):
        dbos = self.d.db.con.get('command')
        len1 = len(dbos)

        self.d.db.con.delete('command', dbos[len1-1])

        dbos2 = self.d.db.con.get('command')
        len2 = len(dbos2)

        self.assertEqual(len1 , len2+1, "db delete failed")

    def test_post(self):

        str1 = "TEST"
        str2 = "UNITTEST"

        dbo  = self.d.db.con.getDbo()
        dbo.device  = str1
        dbo.payload = str2
        self.d.db.con.post('command', dbo)

        dbos = self.d.db.con.get('command')
        len1 = len(dbos)

        self.assertEqual(str1 , dbos[len1-1].device, "post device failed")
        self.assertEqual(str2 , dbos[len1-1].payload, "post payload failed")

    def test_clear(self):
        dbo  = self.d.db.con.getDbo()
        dbo.address = "http://"
        dbo.name    = "name1"
        dbo.task    = "task1"
        self.d.db.con.post('device', dbo)

        self.d.db.con.clear('device')

        dbos = self.d.db.con.get('device')
        len1 = len(dbos)

        self.assertEqual(len1 , 0, "db clear failed")

if __name__ == "__main__":
    unittest.main()
