We have provided a script to generate some data in a format accept by [John The Ripper](http://www.openwall.com/john/). You can use it to generate password hashing by varying some parameters and see the impact it haves on the time needed to crack them. It uses internaly the Django default password hashers, so the hashes are "real". They have the same default settings as Django and can be cracked as fast as real ones.

It pick a random password from a wordlist named `password.list` so it's the worst case scenario as the password cracker also have access to the password list. The basic list is quite small (~3000 passwords), if you want to have a more realistic scenario, replace `password.list` by [one of password list downloaded here](https://wiki.skullsecurity.org/Passwords).

Here are some examples of run with MD5, BCrypt and PBKDF2:

<a href="https://asciinema.org/a/108744" target="_blank"><img src="https://asciinema.org/a/108744.png" width="1318"/></a>

<a href="https://asciinema.org/a/108746" target="_blank"><img src="https://asciinema.org/a/108746.png" width="1318"/></a>

<a href="https://asciinema.org/a/108756" target="_blank"><img src="https://asciinema.org/a/108756.png" width="1318"/></a>

### Generate some data locally

The script `generate_data.py` can be used to generate some data, first install the requirements:

```
pip install -r requirements.txt
```

```
usage: generate_data.py [-h] [--salt SALT] [--pepper PEPPER] [--rounds ROUNDS]
                        [--n N]
                        algorithm

Generate username / password list for john the ripper

positional arguments:
  algorithm        which algorithm to use (md5, bcrypt or pbkdf2)

optional arguments:
  -h, --help       show this help message and exit
  --salt SALT      which kind of salt to use (none, same, user)
  --pepper PEPPER  a pepper
  --rounds ROUNDS  Number of rounds to use
  --n N            number of users/password to generate
```

For example to generate 5 usernames / password with bcrypt and a different salt per user, you can do:

```
$> python generate_data.py --salt user --n=5 bcrypt
Generating 5 usernames/password with algorithm 'bcrypt' with salt 'user' [12 rounds] and pepper ''

drakeandrea:$2b$12$K2GNkU1jZBnrHntKRTeE/OauVFlpC3JzQ/5ZEZQL9h8gJMJhPTKre
darlene71:$2b$12$p69/XRS1fd/N.EYn/saBhO0DQoh/SX8SR6XnA5BpN/eJF523m.U7e
brandonbates:$2b$12$fRTHDpoiWePbm1dU8AihrOfkaqNsgXkyxcRbDAhIEYEvfwA0TNYKK
danielle29:$2b$12$Q5dqtlRuWzh.wZB1ZADCGOb3HOgOV2mjN3.x5/n33cS8IQxLLvi9O
jennifer93:$2b$12$l7m9vmEKLqfPrvLURDVn/OEbnkdDa0cPZugA/4O56B3mchkVRkEom

Output also write in file `passwd`
You can crack it with `john --wordlist=password.list --format=bcrypt passwd`
```

Then to crack it with john the ripper:

```
$> john --wordlist=password.list --format=bcrypt passwd
```

It can take a long time to crack, it's intended.

### Use docker

We also provided a Dockerfile that you can use if you don't want to install John.

First you can build with:

```
docker build -t safe_password_storage_python .
```

Then launch it with:

```
docker run -t -i --rm=true safe_password_storage_python
```

You can then use the same commands as shown above.
