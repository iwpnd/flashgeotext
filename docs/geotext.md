
  FileNotFoundError

  [Errno 2] No such file or directory: b'/Users/benjaminramser/.rvm/bin/-I'

  at ~/.pyenv/versions/3.7.7/lib/python3.7/os.py:607 in _execvpe
       603│         path_list = map(fsencode, path_list)
       604│     for dir in path_list:
       605│         fullname = path.join(dir, file)
       606│         try:
    →  607│             exec_func(fullname, *argrest)
       608│         except (FileNotFoundError, NotADirectoryError) as e:
       609│             last_exc = e
       610│         except OSError as e:
       611│             last_exc = e
