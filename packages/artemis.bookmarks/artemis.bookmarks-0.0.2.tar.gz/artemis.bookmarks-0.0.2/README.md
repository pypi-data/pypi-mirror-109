# bookmarks

![trans rights!](https://awoo.systems/trans_rights_badge.svg)

a small bookmark api

## Quickstart

```
$ python -m pip install artemis.bookmarks
$ export FLASK_APP=bookmarks.app
$ python -m flask db:init
$ python -m flask run
```

## Configuration

By default, the DB is configured to stay in RAM, so it simply won't work.

The configuration file's name is `bookmarks.toml`, and it can reside in the following paths.

- `./bookmarks.toml`
- `~/.config/bookmarks/bookmarks.toml`
- `~/.config/bookmarks.toml`
- `/etc/bookmarks/bookmarks.toml`
- `/etc/bookmarks.toml`

### Example configuration

```toml
SQLALCHEMY_DATABASE_URI='sqlite:////usr/share/bookmarks.db'
SERVER_NAME='bookmarks.example.com'
```

You need to check your WSGI runner's configuration to configure its listen interface.
