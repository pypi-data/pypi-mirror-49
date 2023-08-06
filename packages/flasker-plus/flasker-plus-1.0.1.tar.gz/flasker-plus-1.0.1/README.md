
# FlaskerPlus

Simple Boilerplate to get started with Rest+ fast for building WebApps


# Installation and Usage

 - `pip install flaskerplus`
 - `flaskerplus start`


# Configuring
 - Project Uses PostgeSQL by default, however changing the `SQL_ALCHEMY_DATABASE_URL`
 in `config.py` will allow you to use other databases
 - Uses 3 environment variables, you must set these or make a shell script each session as they will disappear
    * `FLASK_ENV` - Flasks environment to run in. Options defined in `config.py`
    * `DATABASE_URL` - The URI of the database you are using
    * `SECRET_KEY` - The key you will use to encode your JSON Web Tokens


# Contributors
 - XzavierDunn - made the boilerplate repository

