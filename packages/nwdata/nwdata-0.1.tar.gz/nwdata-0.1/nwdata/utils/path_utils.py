import os
from typing import Optional, Union
from pathlib import Path

def changeDirectory(Dir:Union[str, Path], expectExist:Optional[bool]=None):
	if isinstance(Dir, str):
		Dir = Path(Dir)
	assert isinstance(Dir, Path), "Got: %s" % Dir
	assert expectExist in (True, False, None)
	if expectExist in (True, False):
		assert Dir.exists() == expectExist, "Exists: %s" % Dir
	Dir.mkdir(exist_ok=True, parents=True)
	print("[changeDirectory] Changing to working directory: %s" % Dir)
	os.chdir(Dir)

# Given a path to a file/directory, return the absolute real path.
def fullPath(x:str):
	return Path(os.path.abspath(os.path.realpath(x))) if not x is None else None
