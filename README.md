# Kryptologie-Lab
Krypto-Lab by Thorsten Kröhl

## Benutzung
Wurde geschrieben in Python 3.10.12 (Standard in Ubuntu-22.04).
Jedes Python-Script schreibt in die Console, falls man es nicht richtig benutzt, wie man es benutzen sollte.
Für jedes der Programme wurden Tests geschrieben:
etweder einzeln ausführbar durch `python3 -m unittest discover -s abgabe1`
oder alle auf einmal mit `./test_all.sh` (gehe hier jedes mal davon aus man ist im Unterordner
;jeder der Abgaben Ordner hat mindestens einen Test, kann aber natürlich auch mehr enthalten - sind am Ende weniger Unittests als eher: Einmal testen und schauen ob das rauskommt was man erwartet).
Anmerkung: Test von linearer Analyse/Attack ist ausgestellt weil der länger dauern kann.


### Additive Chiffre (/abgabe1)

Verschlüsselung:

`python3 encrypt_add_chiffre.py path-to-plaintext key path-to-output`

Entschlüsselung:

`python3 decrypt_add_chiffre.py path-to-crypttext key path-to-output`

Automatische Entschlüsselung deutscher Texte:

`python3 automatic_decrypt.py path-to-crypttext [path-to-output]`

### Viginere (/abgabe2)

Verschlüsselung:

`python3 encrypt_vigenere.py path-to-plaintext key path-to-output`

Automatische Entschlüsselung deutscher Texte:

`python3 decrypt_vigenere.py path-to-crypttext path-to-output`

### AES Modes (/abgabe3)

Modes

`python3 modes.py mode blocklength`

### AES 128 bit (/abgabe4)

Verschlüsseln / Entschlüsseln:

`python3 aes.py path-to-plaintext path-to-key path-to-output encrypt/decrypt`

### AES mit Modi(/abgabe5)

Verschlüsseln:

`python3 aes_encrypt.py mode input_file key_file output_file [initVec_file]`

Entschlüsseln:

`python3 aes_decrypt.py mode input_file key_file output_file [initVec_file]`

### Lineare Kryptoanalyse (/abgabe6)

SPN:

`python3 spn.py input_file key_file output_file`

Klartexte generieren für Teilschlüsselsuche:

`python3 genText.py plaintext_file number_of_texts`

Linearisierungsangriff:

`python3 linAttack.py plaintexts.txt ciphertexts.txt output_file`

### Güte von Approximationen bestimmen (/abgabe7)

`python3 checkQualityLinApprox.py sBox_file approximation_file`

### RSA (/abgabe8)

`python3 rsa.py input_file key_file output_file`

### RSA Schlüsselgenerierung (/abgabe9)

`python3 rsa_keygen.py length output_private_key output_public_key output_primes`

### Diffie-Hellman-Schlüsselaustausch (/abgabe10)

`python3 diffie.py keylength`

### Sha3-224 (/abgabe11)

`python sha3.py input_file output_file`
