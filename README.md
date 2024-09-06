# EncryptMe
A web-based application used to encrypt text using Python's `cryptography` library.
### Video description
Here is a video showcasing the project [Video here](https://youtu.be/DaZHyPA5qUE).
### Synopsis
Ever wanted to encrypt important information and store it on your device? With EncryptMe, you can do just that.

In the age of rapid technology growth, cybersecurity has become increasingly important. Cryptography is a way of providing security and privacy for individuals and companies alike. Encryption is used everywhere, from file storage devices, to applications, and VPNs. The process of converting unencrypted plain text into encrypted ciphertext ensures that adversaries are unable to decipher messages and important documents, unless they possess a secret key. The most widely used encryption algorithm today is the Advanced Encryption Standard (AES).

### Project dependencies
`from cryptography.fernet import Fernet`

EncryptMe uses Python's `Fernet` encryption, which allows you to generate keys and encrypt text. The full documentation is [here](https://pypi.org/project/cryptography/).

Flask is a micro-web framework useful for making web applications. The Flask documentation is [here](https://flask.palletsprojects.com/en/3.0.x/).

The project also uses Jinja for placeholders, together with HTML and CSS to create the webpage interface. More information and documentation of these programming
languages can be found below:

[Jinja](https://jinja.palletsprojects.com/en/3.1.x/).

[Introduction to HTML](https://www.w3schools.com/html/html_intro.asp).

### app.py
This file contains all the Python magic. Below are the libraries used:

```
from flask import Flask, render_template, request, redirect
from cs50 import SQL
from cryptography.fernet import Fernet
```

`Flask` allows Python to get an input by using `request.form.get()`.

`SQL` is used to initialise the database: `db = SQL("sqlite:///encryptme.db")`

### layout.html
This file provides the entire layout of the webpage, which consists of the project title and the navigation bar. The navigation bar style is mostly recycled from CS50x Problem Set 9 "Finance".

Jinja is used to create a placeholder for the different HTML templates. By adding `{% block main %}{% endblock %}`
into layout.html, I can display any template by calling the same command in a HTML file and implementing code in between. `{% extends "layout.html" %}` tells Jinja that this HTML template can be used within layout.html. For example:

```
{% extends "layout.html" %}

{% block main %}
    *your code here*
{% endblock %}
```


### index.html
This is the main page of EncryptMe. It provides a summary of the names of the keys and the keys themselves, akin to a wallet. Simply copy the key and go to "Decrypt" in the navigation bar and paste it into the "key" input box.

### manager.html
This file is one of the HTML templates that allow you to save your keys into a database while giving a name for the key
for easy indentification. The keys are stored into the encryptme.db database.

This file receives user input using the `<input>` function in HTML. I decided to recycle the input box style used by CS50X Problem Set 9 "Finance".

```
<div class="mb-3">
        <p><label for="Name">Name:</label></p>
        <input autocomplete="off" autofocus class="form-control mx-auto w-auto" name="name" placeholder="e.g May's birthday gift" type="text">
        <p><label for="key">Key:</label></p>
        <input autocomplete="off" autofocus class="form-control mx-auto w-auto" name="key" placeholder="key" type="text">
    </div>
```

Upon pressing "Enter", you will be redirected to the main page where you can see a summary of keys stored, which is displayed by index.html

### encryptme.db
This database file is accessible via Structured Query Language (SQL), specifically the `sqlite3` library. The schema is as follows:

```
CREATE TABLE reference (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    key TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
In index.html, the id, name and keys are shown. The way to display values in a database is as follows:

Call the columns in the dictionary that you want to display. In this case, I used `db.execute()` and saved the return value in a variable as a `list` object.

`reference_list = db.execute("SELECT name, key FROM reference")`

Afterwards, you can iterate over the list of dictionaries using Jinja in index.html, by typing the code as follows:
```
<tr>
    {% for row in reference_list %}
    <td text-align=center>{{ row.id }}</td>
    <td text-align=center>{{ row.name }}</td>
    <td text-align=center>{{ row.key }}</td>
</tr>
{% endfor %}
```

Be sure to end your for loop outside of `<tr>`, else Jinja will print every element in the same row.

### encrypt.html
This file provides an interface for the user to enter a piece of text they want to encrypt. To create a larger text box that could accomodate longer plaintext, `<textarea rows="10" cols="100">` was used to create a text box that is 100 characters in width and 10 characters in height.

The Python code `Fernet.generate_key()` is used to generate a new key every time the user encrypts text. It returns a `byte` object.

In order to use `Fernet` to encrypt text, the text needs to be converted into a `byte` object using the
`encode("utf-8")` method. Afterwards, the ciphertext and key are converted from a `byte` object into a `string` using the `decode("utf-8")` method.

This is the function that I have created. The return value is a `byte` object:

```
def fernet_encryption(string_bytes, key):
    encrypted = Fernet(key).encrypt(string_bytes)
    return encrypted
```

Subsequently, the encrypted text is generated below the key, allowing users to copy and paste the ciphertext back into their documents.

### decrypt.html
Of course, users need a way to decrypt text whenever they require access to certain information. This file contains another textbox for users to paste their encrypted text. They will also be required to paste the secret key used into the `key` input box. The decrypted text will be displayed at the bottom of the webpage.

Here is the decryption function in action. The return value is a `byte` object:

```
def fernet_decryption(string_bytes, key):
    decrypted = Fernet(key).decrypt(string_bytes)
    return decrypted
```

### delete.html
This file allows you to delete keys that are no longer in use. By getting the id of the key to be deleted, an SQL query can be executed to delete the corresponding key.

```
db.execute("DELETE FROM references WHERE id = ?", delete_id)
```
### Additional materials
Here are some additional resources that can introduce you to cryptography.

AES: How to design secure encryption by Spanning Tree: https://www.youtube.com/watch?v=C4ATDMIz5wc

Introduction to cryptography by SciShow: https://www.youtube.com/watch?v=-yFZGF8FHSg&t=83s

Copyright © 2024 Beh Kai Le Rinchen  
All rights reserved. No part of this software may be copied, redistributed or modified without written permission from the copyright owner.



