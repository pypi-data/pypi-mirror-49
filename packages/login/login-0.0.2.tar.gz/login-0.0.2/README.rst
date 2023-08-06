login
============================================================
| Module for common login service

.. code:: sh

  $ pip install login


.. code:: python

   from login.check import generate_password_hash, check_password_hash, set_salt  

   set_salt("__YOUR_SECRET_PLAINTEXT__")

   # signin
   email = 'ksg97031@gmail.com'
   password_hash = generate_password_hash(password) 
   user = User(email, password_hash)
   db.session.add(user)
   db.session.commit()

   # login
   user = User.query.filter(User.email == 'ksg97031@gmail.com').first();
   assert user is not None 
   check_password_hash(password, user.password)


