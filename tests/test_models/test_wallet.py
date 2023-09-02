#!/usr/bin/python3
"""
Contains the TestWalletDocs classes
"""

from datetime import datetime
import inspect
import models
from models import wallet
from models.base_model import BaseModel
import pep8
import unittest

Wallet = wallet.Wallet


class TestWalletDocs(unittest.TestCase):
    """Tests to check the documentation and style of User class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.wallet_f = inspect.getmembers(Wallet, inspect.isfunction)

    def test_pep8_conformance_wallet(self):
        """Test that models/wallet.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/wallet.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_wallet(self):
        """Test that tests/test_models/test_wallet.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_wallet.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_wallet_module_docstring(self):
        """Test for the wallet.py module docstring"""
        self.assertIsNot(wallet.__doc__, None,
                         "wallet.py needs a docstring")
        self.assertTrue(len(wallet.__doc__) >= 1,
                        "wallet.py needs a docstring")

    def test_wallet_class_docstring(self):
        """Test for the Wallet class docstring"""
        self.assertIsNot(Wallet.__doc__, None,
                         "Wallet class needs a docstring")
        self.assertTrue(len(Wallet.__doc__) >= 1,
                        "Wallet class needs a docstring")

    def test_wallet_func_docstrings(self):
        """Test for the presence of docstrings in Wallet methods"""
        for func in self.wallet_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestWallet(unittest.TestCase):
    """Test the Wallet class"""
    @classmethod
    def setUpClass(self):
        """Set up wallet instance for testing"""
        pass

    def test_is_subclass(self):
        """Test that Wallet is a subclass of BaseModel"""
        wallet = Wallet()
        self.assertIsInstance(wallet, BaseModel)
        self.assertTrue(hasattr(wallet, "id"))
        self.assertTrue(hasattr(wallet, "created_at"))
        self.assertTrue(hasattr(wallet, "updated_at"))

    def test_user_id_attr(self):
        """Test that Wallet has attr user_id"""
        wallet = Wallet()
        self.assertTrue(hasattr(wallet, "user_id"))

    def test_phone_number_attr(self):
        """Test that Wallet has attr phone_number"""
        wallet = Wallet()
        self.assertTrue(hasattr(wallet, "phone_number"))

    def test_pin_attr(self):
        """Test that Wallet has attr pin"""
        wallet = Wallet()
        self.assertTrue(hasattr(wallet, "pin"))

    def test_next_of_kin_attr(self):
        """Test that Wallet has attr next_of_kin"""
        wallet = Wallet()
        self.assertTrue(hasattr(wallet, "next_of_kin"))

    def test_next_of_kin_relationship_attr(self):
        """Test that Wallet has attr next_of_kin_relationship"""
        wallet = Wallet()
        self.assertTrue(hasattr(wallet, "next_of_kin_relationship"))

    def test_next_kin_number_attr(self):
        """Test that Wallet has attr next_of_kin_number"""
        wallet = Wallet()
        self.assertTrue(hasattr(wallet, "next_of_kin_number"))

    def test_balance_attr(self):
        """Test that Wallet has attr balance"""
        wallet = Wallet()
        self.assertTrue(hasattr(wallet, "balance"))

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        wallet = Wallet()
        new_wallet = wallet.to_dict()
        self.assertEqual(type(new_wallet), dict)
        self.assertFalse("_sa_instance_state" in new_wallet)
        for attr in wallet.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_wallet)
        self.assertTrue("__class__" in new_wallet)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        w = Wallet()
        new_w = w.to_dict()
        self.assertEqual(new_w["__class__"], "Wallet")
        self.assertEqual(type(new_w["created_at"]), str)
        self.assertEqual(type(new_w["updated_at"]), str)
        self.assertEqual(new_w["created_at"], w.created_at.strftime(t_format))
        self.assertEqual(new_w["updated_at"], w.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        wallet = Wallet()
        string = "[Wallet] ({}) {}".format(wallet.id, wallet.__dict__)
        self.assertEqual(string, str(wallet))
