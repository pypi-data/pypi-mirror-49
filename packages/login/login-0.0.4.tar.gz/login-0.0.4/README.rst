login
============================================================
| Module for common login service

.. code:: sh

  $ pip install login


.. code:: python

   from login import generate_password_hash, check_password_hash, set_salt  

   set_salt("__YOUR__SECRET__KEY__")

   # signin
   username = 'ksg97031'
   password_hash = generate_password_hash(password) 
   user = User(username, password_hash)
   db.session.add(user)
   db.session.commit()

   # login
   login_username = 'ksg97031'
   user = User.query.filter(User.name == login_username).first();
   assert user is not None 
   if not check_password_hash(password, user.password):
       return 'Login Fail'




