import argparse
import hashlib
import random

import faker
import django.contrib.auth.hashers


FAKE = faker.Factory.create()

with open("password.list") as file:
    PASSWORDS = [line.strip() for line in file.readlines()]


def remove_pepper(encoded, pepper):
    index = encoded.index(pepper)
    return encoded[:index] + encoded[index+len(pepper):]


class MD5Hasher(object):

    def __init__(self, salt=None, pepper=None, rounds=None):
        self.django_hasher = django.contrib.auth.hashers.MD5PasswordHasher()
        self.global_salt = self.django_hasher.salt()

        self.salt = salt
        self.pepper = pepper

        if rounds:
            print("MD5 don't take rounds argument, ignore")

    def encode(self, password):
        if self.salt is None:
            return hashlib.md5(password).hexdigest()
        elif self.salt == 'same':
            salt = self.global_salt
        elif self.salt == 'user':
            salt = self.django_hasher.salt()

        encoded = self.django_hasher.encode(password, self.pepper + salt)
        # Replace 'md5$' by '$1$'
        _, salt, passwd = encoded.split('$')
        return '$dynamic_4$%s$%s' % (passwd, remove_pepper(salt, self.pepper))

    @property
    def iterations(self):
        return 1

    def jtr_format(self):
        if self.salt is None:
            return 'Raw-MD5'
        else:
            return "dynamic_4"


class BCryptHasher(object):

    def __init__(self, salt=None, pepper=None, rounds=None):
        self.django_hasher = django.contrib.auth.hashers.BCryptPasswordHasher()

        if rounds:
            self.django_hasher.rounds = rounds

        self.global_salt = self.django_hasher.salt()

        if salt is None:
            raise NotImplementedError("BCRYPT NEEDS A SALT MORON")

        self.salt = salt
        self.pepper = pepper

    def encode(self, password):
        if self.salt == 'same':
            encoded = self.django_hasher.encode(password, self.pepper + self.global_salt)
            # Replace 'md5$' by '$1$'
            # Remove 'bcrypt$'
            return encoded[7:]
        elif self.salt == 'user':
            encoded = self.django_hasher.encode(password, self.pepper + self.django_hasher.salt())
            # Replace 'md5$' by '$1$'
            return encoded[7:]

    @property
    def iterations(self):
        return self.django_hasher.rounds

    def jtr_format(self):
        return 'bcrypt'


class PBKDF2Hasher(object):

    def __init__(self, salt=None, pepper=None, rounds=None):
        self.django_hasher = django.contrib.auth.hashers.PBKDF2PasswordHasher()

        if rounds:
            self.django_hasher.iterations = rounds

        self.global_salt = self.django_hasher.salt()

        if salt is None:
            raise NotImplementedError("PBKDF2 NEEDS A SALT MORON")

        self.salt = salt
        self.pepper = None

    def encode(self, password):
        if self.salt == 'same':
            encoded = self.django_hasher.encode(password, self.global_salt)
            # Replace 'md5$' by '$1$'
            return "$django$*1*" + encoded
        elif self.salt == 'user':
            encoded = self.django_hasher.encode(password, self.django_hasher.salt())
            # Replace 'md5$' by '$1$'
            return "$django$*1*" + encoded

    @property
    def iterations(self):
        return self.django_hasher.iterations

    def jtr_format(self):
        return 'Django'


def get_hasher(algorithm, salt, pepper, rounds):
    if algorithm == 'md5':
        return MD5Hasher(salt, pepper, rounds)
    elif algorithm == 'bcrypt':
        return BCryptHasher(salt, pepper, rounds)
    elif algorithm == 'pbkdf2':
        return PBKDF2Hasher(salt, pepper, rounds)
    else:
        raise NotImplementedError("Bad algorithm %s" % algorithm)


def main():
    parser = argparse.ArgumentParser(description='Generate username / password list for john the ripper')
    parser.add_argument('algorithm', help='which algorithm to use (md5, bcrypt or pbkdf2)')
    parser.add_argument('--salt', help='which kind of salt to use (none, same, user)')
    parser.add_argument('--pepper', default='', help='a pepper')
    parser.add_argument('--rounds', type=int, help='Number of rounds to use')
    parser.add_argument('--n', type=int, default=10, help='number of users/password to generate')
    args = parser.parse_args()

    hasher = get_hasher(args.algorithm, args.salt, args.pepper, args.rounds)

    msg = "Generating %s usernames/password with algorithm %r with salt %r [%r rounds] and pepper %r\n"
    print(msg % (args.n, args.algorithm, args.salt, hasher.iterations, args.pepper))
    with open('passwd', 'w') as output_file:
        for i in range(args.n):
            username = FAKE.profile(fields='username')['username']
            password = hasher.encode(random.choice(PASSWORDS))
            print("%s:%s" % (username, password))
            output_file.write("%s:%s\n" % (username, password))

    print("\nOutput also write in file `passwd`")
    print("You can crack it with `john --wordlist=password.list --format=%s passwd`" % hasher.jtr_format())

if __name__ == '__main__':
    main()
