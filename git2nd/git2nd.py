from enert import *
import re

regex_gi = re.compile(r'(gi$|git2nd$)')

main_usage = '''\
git2nd [s|status] [a|add] [c|commit] [p|push] [b|branch] [m|merge] [t|tag] [l|log]
       [ac] [acp]
'''

def clone_routine():
    clone_usage = '''\
Usage: git2nd clone
'''
    parser = mkparser(clone_usage)
    args = parser.parse_args()
    if args.help:
        print(clone_usage)
        exit()
    else:
        user_name = input(green('[+]user_name : ', 'bold'))
        repository_name = input(green('[+]repository_name : ', 'bold'))
        dest_dir = input(green('[+]destination_directory : ', 'bold'))
        inf('git clone https://github.com/' + user_name + '/' + repository_name + ' ' + dest_dir)
        shell('git clone https://github.com/' + user_name + '/' + repository_name + ' ' + dest_dir).call()

def status_func():
    if shell('git branch').linedata()[0]:
        branches = branch_func()
        print(green('now: ' + branches[0], 'bold'))
    size_y, size_x = get_term_size()
    print('='*size_x)
    os.system('ls --color=auto')
    print('='*size_x)
    shell('git status').call()

def add_routine():
    add_usage = '''\
Usage: git2nd add [file...]
   or: gia        [file...]

Options:
    file    file name
'''
    parser = mkparser(add_usage)
    if regex_gi.findall(argv[0]):
        args = parser.parse_args(argv[2:])
    else:
        args = parser.parse_args(argv[1:])
    if args.help:
        print(add_usage)
        exit()
    elif args.args:
        add_func(args.args)
    else:
        print(add_usage)
        exit()

def add_func(files):
    inf('add ' + ', '.join(files))
    if type(files) == list:
        for x in files:
            shell('git add ' + x).call()
    else:
        shell('git add ' + files).call()
    shell('git status').call()

def commit_routine():
    commit_usage = '''\
Usage: git2nd commit [-a|--amend] (title)
   or: gic           [-a|--amend] (title)

options:
  (None)        commit no title
  -a|--amend    re_commit(git commit --amend)
  title         add title auto
'''

    parser = mkparser(commit_usage)
    #parser.add_argument('-t', '--title', dest='title')
    parser.add_argument('-a', '--amend', action='store_true')
    if regex_gi.findall(argv[0]):
        args = parser.parse_args(argv[2:])
    else:
        args = parser.parse_args(argv[1:])

    if args.help:
        print(commit_usage)
        exit()
    elif args.amend:
        commit_func(amend=True)
    #elif args.title:
    #    commit_func(title=args.title)
    elif len(args.args) > 0:
        commit_func(title=args.args[0])
    else:
        commit_func()

def commit_func(amend=False, title=None):
    if amend:
        inf('commit --amend')
        shell('git commit --amend').call()
        shell('git log --decorate=short --oneline -1').call()
    else:
        f = fl('/tmp/.git2nd.tmp')
        if not f.exist():
            shell('touch /tmp/.git2nd.tmp').call()
        f.edit()
        data = f.data()
        if len(data) == 0:
            print(red('commit message is None'))
            exit()
        if title == None:
            data = re.compile(r'(^u |^u$)').sub('[update]', data)
            data = re.compile(r'(^n |^n$)').sub('[new]', data)
            data = re.compile(r'(^a |^a$)').sub('[add]', data)
            data = re.compile(r'(^b |^b$)').sub('[bugfix]', data)
            data = re.compile(r'(^d |^d$)').sub('[delete]', data)
        else:
            data = re.compile(r'(^u |^u$)').sub('[update]' + title + ' : ', data)
            data = re.compile(r'(^n |^n$)').sub('[new]' + title + ' : ', data)
            data = re.compile(r'(^a |^a$)').sub('[add]' + title + ' : ', data)
            data = re.compile(r'(^b |^b$)').sub('[bugfix]' + title + ' : ', data)
            data = re.compile(r'(^d |^d$)').sub('[delete]' + title + ' : ', data)
        stdout, stderr = shell('git commit -m "' + data + '"').linedata()
        inf('commit')
        for x in stderr:
            print(red(x, 'bold'))
        shell('git log --decorate=short --oneline -1').call()
        f.rm()

def push_routine():
    push_usage = '''\
Usage: git2nd push
   or: gip
'''
    parser = mkparser(push_usage)
    if regex_gi.findall(argv[0]):
        args = parser.parse_args(argv[2:])
    else:
        args = parser.parse_args(argv[1:])
    if args.help:
        print(push_usage)
        exit()
    else:
        push_func()

def push_func():
    branches = branch_func()
    inf('push ' + branches[0])
    if branches[0] == 'master':
        ans = select_input(blue('[+]', 'bold') + red('will push master. continue? [y/n]', 'bold') + blue(' : ', 'bold'), ['y', 'n'])
        if ans == 'n':
            print(red('\nquit.\n'))
            exit()
        elif ans == 'y':
            print(blue('\ncontinue.\n'))
    out, err = shell('git push origin ' + branches[0]).linedata()
    if len(err) == 2 and err[0].count('To') > 0 and err[1].count('->') > 0:
        for x in err:
            print(x)
    elif len(err) == 1 and err[0] == 'Everything up-to-date':
        for x in err:
            print(x)
    else:
        print(red('[') + blue('+', 'bold') + red(']WARNING'))
        for x in err:
            print(red(x, 'bold'))
    print('')

def branch_routine():
    branch_usage = '''\
Usage: git2nd branch [-d|--delete] [-D|--DELETE] (branch)
   or: gib           [-d|--delete] [-D|--DELETE] (branch)

Positional Options:
  (None)    show branches
  branch    change or create

Optional Options:
  -d        delete branch
  -D        force delete branch
'''
    #branch_args  = ['(None):print now branch', 'branch:make or change branch']
    parser = mkparser(branch_usage)
    parser.add_argument('-d', '--delete', dest='delete')
    parser.add_argument('-D', '--DELETE', dest='force')
    if regex_gi.findall(argv[0]):
        args = parser.parse_args(argv[2:])
    else:
        args = parser.parse_args(argv[1:])
    if args.help:
        print(branch_usage)
        exit()
    elif len(args.args) == 0 and not args.delete and not args.force:
        branch_func('out')
    elif args.delete:
        out, err = shell('git branch -d ' + args.delete).linedata()
        if err:
            for x in err:
                print(red(x))
        else:
            inf('delete ' + args.delete)
        branch_func('out')
    elif args.force:
        out, err = shell('git branch -D ' + args.force).linedata()
        if err:
            for x in err:
                print(red(x))
        else:
            inf('delete ' + args.force)
        branch_func('out')
    else:
        branches = branch_func()
        if args.args[0] in branches: #exist
            shell('git checkout ' + args.args[0] + ' > /dev/null').call()
            branch_func('out')
        else: #not exist
            print('add branch \'' + args.args[0] + '\'')
            shell('git branch ' + args.args[0] + ' > /dev/null').call()
            shell('git checkout ' + args.args[0]).call()
            branch_func('out')

def branch_func(fmt='ret'):
    """
    branch_func(type='ret') # return_value[0] == now branch
    branch_func(type='out')
    """
    branches = shell('git branch').linedata()[0]
    now_idx  = -1
    for i in range(len(branches)):
        if branches[i][0] == '*':
            now = re.compile(r'^\* *').sub('', branches[i])
            now_idx = i
    if now_idx == -1:
        print(red('Branch Not Found.'))
        exit()
    lst = []
    lst.append(now)
    for i in range(len(branches)):
        if i != now_idx:
            lst.append(regex_s.sub('', branches[i]))
    branches = lst
    if fmt == 'out':
        shell('git branch').call()
    return branches

def merge_routine():
    merge_usage = '''\
Usage: git2nd merge [branch]
   or: gim          [branch]

Optinos:
  branch   branch name
'''
    parser = mkparser(merge_usage)
    if regex_gi.findall(argv[0]):
        args = parser.parse_args(argv[2:])
    else:
        args = parser.parse_args(argv[1:])
    if args.help:
        print(merge_usage)
        exit()
    elif len(args.args) < 1:
        print(merge_usage)
        exit()
    else:
        now = branch_func()[0]
        if args.args[0] == 'm':
            branch = 'master'
        elif args.args[0] == 'd':
            branch = 'develop'
        else:
            branch = args.args[0]
        merge_func(now, branch)

def merge_func(now, to):
    """
    merge_func(str to)
    """
    out, err = shell('git checkout ' + to).linedata()
    inf('merge ' + blue(now, 'bold') + red(' -> ', 'bold') + blue(to, 'bold'))
    shell('git merge ' + now + ' 2> /tmp/.git2nd.tmp').call()
    f = fl('/tmp/.git2nd.tmp')
    linedata = f.linedata()
    if linedata:
        for x in linedata:
            print(red(x, 'bold'))
    if f.exist():
        f.rm()
    out, err = shell('git checkout ' + now).linedata()

def tag_routine():
    tag_usage = '''\
Usage: git2nd tag [-a] [-d] [name]

Positional options:
  name    tag name

Optional options:
  -a      git -a tag
  -d      delete tag
'''
    parser = mkparser(tag_usage)
    parser.add_argument('-a', action='store_true', dest='a')
    parser.add_argument('-d', action='store_true', dest='d')
    if regex_gi.findall(argv[0]):
        args = parser.parse_args(argv[2:])
    else:
        args = parser.parse_args(argv[1:])
    if args.help:
        print(tag_usage)
        exit()
    elif len(args.args) < 1:
        shell('git tag').call()
    elif args.a:
        tag_func(args.args[0], a_option=True)
    elif args.d:
        tag_func(args.args[0], d_option=True)
    else:
        tag_func(args.args[0])

def tag_func(tag, a_option=False, d_option=False):
    """
    tag_func(str tag, bool a_option)
    """
    if a_option:
        inf('create tag \'' + tag + '\' -> push')
        shell('git tag -a ' + tag).call()
        shell('git push origin --tags').call()
    elif d_option:
        inf('delete tag \'' + tag + '\' -> push')
        shell('git tag -d ' + tag).call()
        shell('git push origin :' + tag).call()
    else:
        inf('create tag \'' + tag + '\' -> push')
        shell('git tag ' + tag).call()
        shell('git push origin --tags').call()

def log_routine():
    log_usage = '''\
Usage: git2nd log [-v|--verbose]
   or: gil        [-v|--verbose]

Options:
  -v    show verbose(show detail)
'''
    parser = mkparser(log_usage)
    parser.add_argument('-v', '--verbose', action='store_true')
    if regex_gi.findall(argv[0]):
        args = parser.parse_args(argv[2:])
    else:
        args = parser.parse_args(argv[1:])
    if args.help:
        print(log_usage)
        exit()
    elif args.verbose:
        shell('git log --decorate=short -p').call()
    else:
        shell('git log --decorate=short --oneline -3').call()

def diff_routine():
    diff_usage = '''\
Usage: git2nd diff [file]
   or: giff       [file]

Options:
  file    file name
'''
    parser = mkparser(diff_usage)
    if regex_gi.findall(argv[0]):
        args = parser.parse_args(argv[2:])
    else:
        args = parser.parse_args(argv[1:])
    if args.help:
        print(diff_usage)
        exit()
    elif len(args.args) < 1:
        print(diff_usage)
        exit()
    else:
        shell('git diff ' + args.args[0]).call()

def ac_routine():
    ac_usage = '''\
Usage: git2nd ac [-t|--title <title>] [file]
   or: giac      [-t|--title <title>] [file]

Positional Options:
  file    file name

Optional Options:
  -t      Add original title. If no this option, title is first file name.
'''
    parser = mkparser(usage=ac_usage)
    parser.add_argument('-t', '--title', dest='title')
    if regex_gi.findall(argv[0]):
        args = parser.parse_args(argv[2:])
    else:
        args = parser.parse_args(argv[1:])

    if args.help:
        print(ac_usage)
        exit()
    elif len(args.args) < 1:
        print(ac_usage)
        exit()
    else:
        if args.title:
            ac_func(args.args, title=args.title)
        else:
            if len(args.args) == 1:
                ac_func(args.args, title=args.args[0])
            else:
                ac_func(args.args)

def ac_func(files, title=None):
    add_func(files)
    if title:
        commit_func(title=title)
    else:
        commit_func()

def acp_routine():
    acp_usage = '''\
Usage: git2nd acp [-t|--title <title>] [files...]
   or: giacp      [-t|--title <title>] [files...]

Positional Options:
  files    file name

Optional Options:
  -t       title message 
'''
    parser = mkparser(acp_usage)
    parser.add_argument('-t', '--title', dest='title')
    if regex_gi.findall(argv[0]):
        args = parser.parse_args(argv[2:])
    else:
        args = parser.parse_args(argv[1:])
    if args.help:
        print(acp_usage)
        exit()
    elif len(args.args) < 1:
        print(acp_usage)
        exit()
    if args.title:
        title = args.title
    else:
        title = args.args[0]
    acp_func(args.args, title)

def acp_func(files, title=None):
    ac_func(files, title=title)
    push_func()

def cp_routine():
    cp_usage = '''\
Usage: git2nd cp [-t|--title <title>] [-a|--amend]
   or: gicp      [-t|--title <title>] [-a|--amend]

Optional Options:
  -t    title message
  -a    git commit --amend
'''
    parser = mkparser(cp_usage)
    parser.add_argument('-t', '--title', dest='title')
    parser.add_argument('-a', '--amend', action='store_true')
    if regex_gi.findall(argv[0]):
        args = parser.parse_args(argv[2:])
    else:
        args = parser.parse_args(argv[1:])
    if args.help:
        print(cp_usage)
        exit()
    elif args.title:
        if args.amend:
            print(cp_usage)
            exit()
        else:
            cp_func(title=args.title)
    elif args.amend:
        if args.title:
            print(cp_usage)
            exit()
        else:
            cp_func(amend=True)
    else:
        cp_func()

def cp_func(amend=False, title=None):
    if amend:
        commit_func(amend=True)
        push_func()
    elif title:
        commit_func(title=title)
        push_func()
    else:
        commit_func()
        push_func()

def mp_routine():
    branches = branch_func()
    mp_usage = '''\
Usage: git2nd mp [branch]
   or: gimp      [branch]

Positional Options:
  branch   dest branch name ''' + '{' + ','.join(branches[1:]) + '} (now: ' + branches[0] + ')'

    parser = mkparser(mp_usage)
    parser.add_argument('branch', choices=branches)
    if regex_gi.findall(argv[0]):
        if argv[2] == 'm':
            lst = ['master']
        elif argv[2] == 'd':
            lst = ['develop']
        else:
            lst = argv[2:]
        args = parser.parse_args(lst)
    else:
        if argv[1] == 'm':
            lst = ['master']
        elif argv[1] == 'd':
            lst = ['develop']
        else:
            lst = argv[1:]
        args = parser.parse_args(lst)
    if args.help:
        print(mp_usage)
        exit()
    elif not args.branch in branches:
        print(mp_usage)
        exit()
    else:
        now = branches[0]
        mp_func(now, args.branch)

def mp_func(now, to):
    merge_func(now, to)
    shell('git checkout ' + to).call()
    push_func()
    shell('git checkout ' + now).call()
    inf('checkout ' + now)

def stash_routine():
    stash_usage = '''\
Usage: git2nd stash
'''

def main():
    usage = '''\
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
    '''

    lst = ['status', 's', 'add', 'a', 'commit', 'c', 'push', 'p', 'branch', 'b', 'merge', 'm', 'tag', 't', 'log', 'l', 'diff', 'stash', 'd', 'f', 'clone', 'ac', 'cp', 'acp', 'mp']
    parser = mkparser(usage, lst)

    if argc < 2:
        print(usage)
        exit()
    elif argv[1] in lst:
        args = parser.parse_args()
    else:
        print(usage)
        exit()

    if args.command in ['status', 's']:
        status_func()
    elif args.command in ['add', 'a']:
        add_routine()
    elif args.command in ['commit', 'c']:
        commit_routine()
    elif args.command in ['push', 'p']:
        push_routine()
    elif args.command in ['branch', 'b']:
        branch_routine()
    elif args.command in ['merge', 'm']:
        merge_routine()
    elif args.command in ['tag', 't']:
        tag_routine()
    elif args.command in ['log', 'l']:
        log_routine()
    elif args.command in ['diff', 'd', 'f']:
        diff_routine()
    elif args.command == 'stash':
        stash_routine()
    elif args.command == 'clone':
        clone_routine()
    elif args.command == 'ac':
        ac_routine()
    elif args.command == 'acp':
        acp_routine()
    elif args.command == 'cp':
        cp_routine()
    elif args.command == 'mp':
        mp_routine()
    elif args.help:
        print(usage)
        exit()
    else:
        print(usage)
        exit()

if __name__ == '__main__':
    main()
