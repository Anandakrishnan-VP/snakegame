"""
Unit test for Postgres adapter wrapper.
Verifies placeholder conversion, DictCursor delegation, and transaction methods.
"""

import unittest
from unittest.mock import MagicMock
from backend.db.database import PostgresCursorWrapper, PostgresConnectionWrapper

class TestPostgresAdapter(unittest.TestCase):
    def test_placeholder_conversion(self):
        mock_raw_cur = MagicMock()
        mock_raw_cur.fetchall.return_value = [{"is_code": "IS 17803:2022", "title": "Flask"}]
        
        wrapper = PostgresCursorWrapper(mock_raw_cur)
        wrapper.execute("SELECT is_code, title FROM standards WHERE is_code = ? AND division = ?", ("IS 17803:2022", "Metallurgical"))
        
        # Verify ? was converted to %s
        mock_raw_cur.execute.assert_called_once_with(
            "SELECT is_code, title FROM standards WHERE is_code = %s AND division = %s",
            ("IS 17803:2022", "Metallurgical")
        )
        
        rows = wrapper.fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["is_code"], "IS 17803:2022")

    def test_connection_methods(self):
        mock_raw_conn = MagicMock()
        conn_wrapper = PostgresConnectionWrapper(mock_raw_conn)
        
        conn_wrapper.commit()
        mock_raw_conn.commit.assert_called_once()
        
        conn_wrapper.rollback()
        mock_raw_conn.rollback.assert_called_once()
        
        conn_wrapper.close()
        mock_raw_conn.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
