from os import getenv, access, R_OK
from os.path import isfile
from pathlib import Path
from typing import Optional

user_home = Path(getenv('HOME'))
default_config_paths = [
	'bookmarks.toml',
	user_home / '.config/bookmarks/bookmarks.toml',
	user_home / '.config/bookmarks.toml',
	'/etc/bookmarks/bookmarks.toml',
	'/etc/bookmarks.toml',
]


def get_config_path(additional: Optional[str] = None) -> Optional[str]:
	paths = default_config_paths
	if None is not additional:
		paths.append(additional)
	for path in paths:
		if isfile(path) and access(path, R_OK):
			return path
