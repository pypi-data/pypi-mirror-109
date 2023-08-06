# bashmocker

A Python helper for unit testing shell scripts. It's intended for use with Bash but
in fact any program that runs other programs and respects $PATH is testable this way.
I made it originally for a mostly-Python project which had some embedded shell scripts,
and I wanted to be able to test everything in one test framework.

The idea is based on the `patch` and `Mock` features in the standard `unittest.mock`
but rather than replacing Python functions it replaces executables. It works by making
a directory of decoy scripts, then adding this directory to the front of the PATH when
running whatever you want to test. You can then query which of the decoy scripts were
run, and with what parameters.

This way you can use Python to write unit tests that invoke shell scripts and probe
aspects of their internal behaviour. You can probably do other things with it as well -
it's not tied to any particular testing framework.

## A quick example

Say you have a shell script named cleanup.sh:

```sh
#!/bin/bash
echo "Cleaning the database now"
data_cleanup server1.example.com
data_cleanup server2.example.com
mail_report -t steve@example.com "All servers cleaned"
```

To test the behaviour of the script without actually cleaning any databases or spamming
Steve, we can run the script with these commands mocked out:

```python
with BashMocker('data_cleanup', 'mail_report') as bm:
    bm.runscript('cleanup.sh')

    # Check that cleanup.sh called 'data_cleanup' twice.
    assert len(bm.last_calls['data_cleanup']) == 2

    # Check that 'mail_report' was run once with expected args
    assert bm.last_calls['mail_report'] == \
            [ ["-t", "steve@example.com", "All servers cleaned"] ]

    # And we can also see the message that was printed
    assert bm.last_stdout == "Cleaning the database now\n"
```

## Adding side effects

In the above example, when the script calls `data_cleanup` in the BashMocker sandbox it
actually calls a small script which simply logs the calling arguments and exits with
status 0. If `cleanup.sh` expected some output from the `data_cleanup` program then it
may get confused:

```sh
#!/bin/bash
result=$( data_cleanup server1.example.com )
[ "$result" = OK ] || mail_report -t steve@example.com "All is not well!!!"
```

To provide the output you can add a side effect. This needs to be added with an explicit
call to `add_mock()`, as you can't specify side effects in the constructor. Note that the
`side_effect` is a line to be run by Bash not a Python callback.

```python
with BashMocker('mail_report') as bm:
    bm.add_mock('data_cleanup', side_effect="echo OK")
    bm.runscript('cleanup.sh')
```

You can also have a mocked command return a failure status.

```python
with BashMocker() as bm:
    bm.add_mock('data_cleanup', side_effect="echo OK")
    bm.add_mock('mail_report', fail=True)
    bm.runscript('cleanup.sh')
```

## Scripts that read and write files

This module does not aim to help you with constructing a sandbox for your script to run in,
or inspecting the results of files written (apart from STDIN and STDOUT). You'll need to set
that up yourself.

## What if my script invokes programs /by/explicit/path?

`BashMocker` tries to patch these by defining functions, which are then fed to Bash via the
BASH_ENV setting. This is very hacky but can work sometimes. If you're only using this module
for writing regression tests then often a hacky solution is fine.

## What cannot be mocked out?

Shell builtins, because Bash does not look for these in the PATH. I've not found a good reason
to mock them out in any case.
They could be done with the hack described above I guess - at present you'll have to call the
internal `_add_mockfunc()` directly to make that work.

## Does it only work with Bash?

The main mocking mechanism simply pokes dummy programs into a directory added to the PATH, so
CSH scripts or Makefiles or compiled applications or even Python scripts (please don't!) can
be tested this way.

Internally the module creates these dummy programs as little Bash Scripts, but you can also force
a different interpreter to be set using eg. `BashMocker(shell="/bin/dash")`. The mechanism will
work with Dash or with compatibility-mode Bash, but seriously who has Python3 and not Bash on
their system??

The hack that allows mocking of programs with '/' in the name, ie. programs that are invoked
directly without searching the PATH, only works for Bash. POSIX shell doesn't let you make
functions with '/' in the name. I thought I could achieve it with aliases, but I hit a dead end.
