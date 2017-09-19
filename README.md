# git2nd - easy to use git wrapper

[![Twitter](https://imgur.com/Ibo0Twr.png)](https://twitter.com/miyagaw61)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)

This is very easy to use git.

![git2nd](https://i.imgur.com/o0PdcOa.png)

## Install

※/path/to is any directory

```bash
git clone https://github.com/miyagaw61/git2nd /path/to/git2nd
cd /path/to/git2nd
python setup.py install
```

## Usage

* git2nd -h
```
Usage: git2nd [clone] [s|status] [a|add] [c|commit]
              [p|push] [b|branch] [m|merge] [t|tag]
              [l|log] [d|f|diff] [ac] [cp] [acp] [mp]

SubCommands:
  clone     easy clone
  status    print status
  add       git add
  commit    git commit -m
  push      git push origin now branch
  branch    git branch and git checkout
  merge     git merge command
  tag       git tag , git tag -a
  log       git log and git log --oneline
  diff      git diff
  ac        git2nd add -> git2nd commit
  cp        git2nd commit -> git2nd push
  acp       git2nd ac -> git2nd push
  mp        git2nd merge -> git2nd push
 
aliaces:
  gis       git2nd status
  gia       git2nd add
  gic       git2nd commit
  gip       git2nd push
  gib       git2nd branch
  gil       git2nd log
  giff      git2nd diff
  giac      git2nd ac
  gicp      git2nd cp
  giacp     git2nd acp
  gimp      git2nd mp
```

* clone

```
Usage: git2nd clone
```

![clone](https://i.imgur.com/vF6j8Fo.png)

* status

![status](https://i.imgur.com/GiaviLS.png)

* add

```
Usage: git2nd add [file...]
   or: gia        [file...]

Options:
    file    file name
```

![add](https://i.imgur.com/wrVvlcM.png)

* commit

```
Usage: git2nd commit [-a|--amend] (title)
   or: gic           [-a|--amend] (title)

options:
  (None)        commit no title
  -a|--amend    re_commit(git commit --amend)
  title         add title auto
```

* auto sed
```
^u -> [update]
^a -> [add]
^n -> [new]
^b -> [bugfix]
^d -> [delete]
```

* title sed
```
u foobar -> [update]title : foobar
```


![commit1](https://i.imgur.com/TOHDPMP.png)
![commit2](https://i.imgur.com/VxR0qz6.png)
![commit3](https://i.imgur.com/5Y36oUU.png)

* push

push now branch

```
Usage: git2nd push
   or: gip
```

![push](https://i.imgur.com/apAN4ob.png)

* branch

```
Usage: git2nd branch [-d|--delete] [-D|--DELETE] (branch)
   or: gib           [-d|--delete] [-D|--DELETE] (branch)

Positional Options:
  (None)    show branches
  branch    change or create

Optional Options:
  -d        delete branch
  -D        force delete branch
```

![branch](https://i.imgur.com/Ux7wmXW.png)

* merge

```
Usage: git2nd merge [branch]
   or: gim          [branch]

Optinos:
  branch   branch name
```

![merge](https://i.imgur.com/FaJwAl8.png)

* tag

```
Usage: git2nd tag [-a] [-d] [name]

Positional options:
  name    tag name

Optional options:
  -a      git -a tag
  -d      delete tag
```

![tag](https://i.imgur.com/P6kkgwz.png)

* log

```
Usage: git2nd log [-v|--verbose]
   or: gil        [-v|--verbose]

Options:
  -v    show verbose(show detail)
```

![log](https://i.imgur.com/sPEfhPp.png)

* diff

```
Usage: git2nd diff [file]
   or: giff        [file]

Options:
  file    file name
```

![diff](https://i.imgur.com/Hq4Szp5.png)

* ac

add -> commit

```
Usage: git2nd ac [-t|--title <title>] [file]
   or: giac      [-t|--title <title>] [file]

Positional Options:
  file    file name

Optional Options:
  -t      Add original title. If no this option, title is first file name.
```

![ac1](https://i.imgur.com/yXbkcVD.png)
![ac2](https://i.imgur.com/IBq72I2.png)
![ac3](https://i.imgur.com/MPDCMMO.png)

* cp

commit -> push

```
Usage: git2nd cp [-t|--title <title>] [-a|--amend]
   or: gicp      [-t|--title <title>] [-a|--amend]

Optional Options:
  -t    title message
  -a    git commit --amend
```

![cp1](https://i.imgur.com/FRf92bm.png)
![cp2](https://i.imgur.com/AJNBrRo.png)
![cp3](https://i.imgur.com/BEHhF8O.png)

* acp

add -> commit -> push

```
Usage: git2nd acp [-t|--title <title>] [files...]
   or: giacp      [-t|--title <title>] [files...]

Positional Options:
  files    file name

Optional Options:
  -t       title message 
```

![acp1](https://i.imgur.com/PvPdNk2.png)
![acp2](https://i.imgur.com/4g97ytF.png)

* mp

merge -> push

```
Usage: git2nd mp [branch]
   or: gimp      [branch]

Positional Options:
  branch   dest branch name {master} (now: develop)
```

![mp](https://i.imgur.com/sl3qHMj.png)
