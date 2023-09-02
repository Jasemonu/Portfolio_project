#!/usr/bin/python3
"""
Contains the TestUserDocs classes
"""

from datetime import datetime
import inspect
import models
from models import transaction
from models.base_model import BaseModel
import pep8
import unittest
Transaction = transaction.Transaction


class TestTransactionDocs(unittest.TestCase):
    """Tests to check the documentation and style of Transaction class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.trans_f = inspect.getmembers(Transaction, inspect.isfunction)

    def test_pep8_conformance_transaction(self):
        """Test that models/transaction.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/transaction.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_transaction(self):
        """Test that tests/test_models/test_transaction.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_transaction.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_transaction_module_docstring(self):
        """Test for the transaction.py module docstring"""
        self.assertIsNot(transaction.__doc__, None,
                         "transaction.py needs a docstring")
        self.assertTrue(len(transaction.__doc__) >= 1,
                        "transaction.py needs a docstring")

    def test_transaction_class_docstring(self):
        """Test for the Transaction class docstring"""
        self.assertIsNot(Transaction.__doc__, None,
                         "Transaction class needs a docstring")
        self.assertTrue(len(Transaction.__doc__) >= 1,
                        "Transaction class needs a docstring")

    def test_transaction_func_docstrings(self):
        """Test for the presence of docstrings in Transaction methods"""
        for func in self.trans_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestTransaction(unittest.TestCase):
    """Test the Transaction class"""
    @classmethod
    def setUpClass(self):
        """Set up transaction instance for testing"""
        pass

    def test_is_subclass(self):
        """Test that Transaction is a subclass of BaseModel"""
        trans = Transaction()
        self.assertIsInstance(trans, BaseModel)
        self.assertTrue(hasattr(trans, "id"))
        self.assertTrue(hasattr(trans, "created_at"))
        self.assertTrue(hasattr(trans, "updated_at"))

    def test_user_id_attr(self):
        """Test that Transaction has attr user_id"""
        trans = Transaction()
        self.assertTrue(hasattr(trans, "user_id"))

    def test_wallet_id_attr(self):
        """Test that Transaction has attr wallet_id"""
        trans = Transaction()
        self.assertTrue(hasattr(trans, "wallet_id"))

    def test_recipient_name_attr(self):
        """Test that Transaction has attr recipient_name"""
        trans = Transaction()
        self.assertTrue(hasattr(trans, "recipient_name"))

    def test_recipient_account_attr(self):
        """Test that Transaction has attr recipient_account"""
        trans = Transaction()
        self.assertTrue(hasattr(trans, "recipient_account"))

    def test_amount_attr(self):
        """Test that Transaction has attr amount"""
        trans = Transaction()
        self.assertTrue(hasattr(trans, "amount"))

    def test_transaction_type_attr(self):
        """Test that Transaction has attr transaction_type"""
        trans = Transaction()
        self.assertTrue(hasattr(trans, "transaction_type"))

    def test_timestamp_attr(self):
        """Test that Transaction has attr timestamp"""
        trans = Transaction()
        self.assertTrue(hasattr(trans, "timestamp"))

    def test_description_attr(self):
        """Test that Transaction has attr description"""
        trans = Transaction()
        self.assertTrue(hasattr(trans, "description"))

    def test_status_attr(self):
        """Test that Transaction has attr status"""
        trans = Transaction()
        self.assertTrue(hasattr(trans, "status"))

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        t = Transaction()
        new_t = t.to_dict()
        self.assertEqual(type(new_t), dict)
        self.assertFalse("_sa_instance_state" in new_t)
        for attr in t.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_t)
        self.assertTrue("__class__" in new_t)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        t = Transaction()
        new_t = t.to_dict()
        self.assertEqual(new_t["__class__"], "Transaction")
        self.assertEqual(type(new_t["created_at"]), str)
        self.assertEqual(type(new_t["updated_at"]), str)
        self.assertEqual(new_t["created_at"], t.created_at.strftime(t_format))
        self.assertEqual(new_t["updated_at"], t.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        trans = Transaction()
        string = "[Transaction] ({}) {}".format(trans.id, trans.__dict__)
        self.assertEqual(string, str(trans))
