from models import storage
from models.user import User
from models.wallet import Wallet
from models.transaction import Transaction
 
#karo = User(first_name="Karo", last_name="Efebe", email_address="Rozey@gmail.com", phone_number="0803464758", sex="Female", address="23 Federal balogun", password="rose")
#storage.reload()
#storage.new(karo)

#wallet = Wallet(user_id=karo.id, phone_number=karo.phone_number, pin='1356', next_of_kin='Ogun Prince', next_of_kin_relationship='Brother', next_of_kin_number='0552323232', balance=6500.00)

#storage.new(wallet)
storage.reload()

#trans = Transaction(user_id="2292b676-cc41-4f5c-94e9-15282253ed76", wallet_id='62693ac2-bc5d-4181-b862-8dc957f60a99', recipient_account='0241845229', recipient_name='Affum Obasandjor', amount=100.00, transaction_type='transfer', description='rent', status='pending')
#storage.new(trans)
#trans = Transaction(user_id="2292b676-cc41-4f5c-94e9-15282253ed76", wallet_id='62693ac2-bc5d-4181-b862-8dc957f60a99', recipient_account='0241845229', recipient_name='Affum Obasandjor', amount=100.00, transaction_type='transfer', description='Bonus', status='pending')
#storage.new(trans)
#storage.save()
ret = storage.wallet(Wallet, 803464758)
print(ret.to_dict())
storage.close()
