from models import storage
from models.user import User
 
karo = User(first_name="Karo", last_name="Efebe", email_address="Rozey@gmail.com", phone_number="0803464758", sex="Female", address="23 Federal balogun", password="rose")
storage.reload()
storage.new(karo)
storage.save()
ret = storage.all()
print(ret)
for item in ret.values():
   print(item)
