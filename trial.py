from models import storage
from models.user import User
 
# ret = User(first_name="Rosemary", last_name="Efebe", email_address="Rozey.com", phone_number="0803464758", sex="Female", address="23 Nicole balogun", password="rosemary")
storage.reload()
ret = storage.all()
print(ret)
for item in ret.values():
   print(item)
