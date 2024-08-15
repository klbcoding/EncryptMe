from flask import Flask, render_template, request, redirect
from cs50 import SQL
from cryptography.fernet import Fernet

# Configure application
app = Flask(__name__)

db = SQL("sqlite:///encryptme.db")

@app.route("/")
def index():
    reference_list = db.execute("SELECT id, name, key FROM reference")
    return render_template("index.html", reference_list=reference_list)


#function to transform a character into cipher
def fernet_encryption(string_bytes, key):
    encrypted = Fernet(key).encrypt(string_bytes)
    return encrypted


#function to transform a cipher back into a character
def fernet_decryption(string_bytes, key):
    decrypted = Fernet(key).decrypt(string_bytes)
    return decrypted


@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    if request.method == "POST":
        plaintext = request.form.get("plaintext")
        plaintext_bytes = plaintext.encode("utf-8")
        key = Fernet.generate_key()

        #convert the plaintext into ciphertext
        ciphertext = fernet_encryption(plaintext_bytes, key)
        return render_template("encrypt.html", key=key.decode("utf-8"), ciphertext=ciphertext.decode("utf-8"))
    else:
        return render_template("encrypt.html")


@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    if request.method == "POST":
        ciphertext = request.form.get("ciphertext")
        ciphertext_bytes = ciphertext.encode("utf-8")
        key = request.form.get("key")
        key_bytes = key.encode("utf-8")

        #convert ciphertext back into plaintext
        decrypted_text = fernet_decryption(ciphertext_bytes, key_bytes)
        return render_template("decrypt.html", decrypted_text=decrypted_text.decode("utf-8"))
    else:
        return render_template("decrypt.html")


@app.route("/manager", methods=["GET", "POST"])
def manager():
    if request.method == "POST":
        name = request.form.get("name")
        key = request.form.get("key")

        #insert values into the database
        db.execute("INSERT INTO reference (name, key) VALUES (?, ?)", name, key)
        return redirect("/")
    else:
        return render_template("manager.html")


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        delete_id = request.form.get("delete_id")
        db.execute("DELETE FROM reference WHERE id = ?", delete_id)
        return redirect("/")
    else:
        return render_template("delete.html")

