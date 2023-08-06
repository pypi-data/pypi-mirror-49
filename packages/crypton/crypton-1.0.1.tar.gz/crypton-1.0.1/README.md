CryptOn
----------

CryptOn is an open-source tool that allows :

   - Secure passwords generation based on [OWASP criteria].
   - Passwords strength & security checks based on [OWASP Guidelines for enforcing secure passwords].
   - Symmetric cryptography*
   - Asymmetric cryptography*
   - Hash Algorithms*
   
   
   _*only in interactive mode_


About
-----------------

**Passwords**

Passwords are a real security threat. Impossible-to-crack passwords are complex with multiple types of 
characters (numbers, letters, and symbols). 
So if you want to safeguard your personal info and assets, creating secure passwords is a big first step and 
CryptOn will help you to achieve it.

It is usual in the computer industry to specify password strength in terms of information entropy which is measured 
in bits and is a concept from information theory. Instead of the number of guesses needed to find the password 
with certainty, the base-2 logarithm of that number is given, which is the number of "entropy bits" in a password.

**Cryptography**

Cryptography (or crypto) is one of the more advanced topics of information security, and one whose understanding 
requires the most schooling and experience. It is difficult to get right because there are many approaches to 
encryption, each with advantages and disadvantages that need to be thoroughly understood by web solution architects 
and developers. In addition, serious cryptography research is typically based in advanced mathematics and number theory,
providing a serious barrier to entry.

The proper and accurate implementation of cryptography is extremely critical to its efficacy. A small mistake in 
configuration or coding will result in removing a large degree of the protection it affords and rending the crypto 
implementation useless against serious attacks. A good understanding of crypto is required to be able to discern 
between solid products and snake oil. The inherent complexity of crypto makes it easy to fall for fantastic claims 
from vendors about their product. Typically, these are “a breakthrough in cryptography” or “unbreakable” or provide 
"military grade" security. If a vendor says "trust us, we have had experts look at this,” chances are they weren't 
experts!

Cryptography at its very core is math. Pure, simple, undiluted math. Math created the algorithms that are the basis 
for all encryption. And encryption is the basis for privacy and security on the internet. So, we love math. Even if it 
is a tad complicated. With that being said, algorithms have to be built to work against computers. As computers get 
smarter, algorithms become weaker and we must therefore look at new solutions. This is how cryptography evolves to beat 
the bad guys. So how is it done? First you need to build a cryptosystem that is both confidential and authentic. 
This cryptosystem is responsible for creating the key(s) that will be used to encrypt and then decrypt the data or 
message. A number of signing algorithms have been created over the years to create these keys, some of which have since 
been deprecated as computing power has increased.

It is commonly used in:

   - SSH Authentication
   - SSL Certficates
   - VPN Tunnel Encryption
   - Email & Messaging Encryption
   - Etc
   
 If you want more information about, try this glossaries and guides:
 
   - [cryptographic algorithms]
   - [cryptographic protocols]
   - [PGP in email]
   - [New Elliptic Curve]

Requirements
----------
  - python 3
  - pip
  - termcolor
  - cryptography
  - pycryptodomex
  - requests
  - validate_email
  - py3dns


Installation
-------------

First of all, we would python 3, pip and openssl installed in our computer.

**Linux**

 ```
 $ apt-get install python3-pip
 $ apt-get install openssl
 ```
 
**MacOS**
 ```
 $ brew install python3
 $ brew install pip
 $ brew install openssl
 
 ```
 **Windows**
 
Download python 3 and pip from [python webpage] and openssl from [openssl webpage].
 
 
Secondly, we install the tool using the traditional installation from **pip**

 ```
 $ easy_install3 -U pip # you have to install python3-setuptools , update pip
 $ pip3 install crypton
 $ crypton # installed successfully
```

Usage
----------

**Run**
```
$ crypton
```

**Options**
```
optional arguments:
  -h, --help            show this help message and exit
  -v, --version         See script version
  -g [length [number ...]], --generate-password [length [number ...]]
                        Secure passwords generation // Defaults: length (20) -
                        number of passwords (1)
  -c password, --check-password password
                        Passwords strength & security checks
  -i, --interactive     Run script in interactive mode

```

**Notes**

IN SOME CASES, if your password contains the special characters you may have problems when parsing. That's because of 
your shell. You should type ``` \ ``` before each special character in the password.

For macOS users maybe you need to setup these settings:

 ```
env ARCHFLAGS="-arch x86_64" 
    LDFLAGS="-L/usr/local/opt/openssl/lib" 
    CFLAGS="-I/usr/local/opt/openssl/include" 

pip install cryptography
 ```

Contributing
------------
For bug reports or enhancements, please open an [issue] here.

[OWASP criteria]: https://www.owasp.org/index.php/Authentication_Cheat_Sheet#Implement_Proper_Password_Strength_Controls
[issue]: https://github.com/OverwatchHeir/CryptOn/issues
[python webpage]: https://www.python.org
[openssl webpage]:https://slproweb.com/products/Win32OpenSSL.html
[OWASP Guidelines for enforcing secure passwords]: https://www.owasp.org/index.php/Authentication_Cheat_Sheet#Implement_Proper_Password_Strength_Controls
[New Elliptic Curve]: https://blog.cloudflare.com/ecdsa-the-digital-signature-algorithm-of-a-better-internet
[PGP in email]:https://www.youtube.com/watch?v=hbkB_jNG-zE
[cryptographic algorithms]: https://www.globalsign.com/en/blog/glossary-of-cryptographic-algorithms/
[cryptographic protocols]: https://dwheeler.com/secure-programs/Secure-Programs-HOWTO/crypto.html
