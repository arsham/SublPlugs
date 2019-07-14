# SublimeMate

SublimeMate is a plugin for Sublime Text 3 that adds a few missing
functionalities. It has a few little tools and missing commands in quick panel.

## Features

The commands listed below are automatically added to the quick panel. For
example ST can fold/unfold comments but there is no commands. Now you can invoke
the quick panel and choose `Fold/Unfold Comments`.

1. Commands for folding and unfolding comments, and fold levels.
2. Evaluate selected text:
    * Example of mathematical evaluation: `666*13`
    * Invoke `math` and `datetime` packages' functions.
3. Run ST commands. This is particularly useful for commands that would not run
in a macro.
4. Add entries to command panel. Invoke `SublPlugs: User commands` and add any
ST commands.
5. A version of Hipster theme for a better contrast for Go development.

An example for running commands: assuming you have `Increment Selection` plugin
installed, you can easily create a list of `a` to `f` with this command, which
is not possible with ST macros.
Add this to user defined commands by invoking `SublPlugs: User commands`:

```json
    {
        "caption": "Create a-z",
        "command": "chain",
        "args": {
            "commands": [
                ["insert",          {"characters": "a"}],
                ["move_to",         {"extend": false, "to": "bol"}],
                ["set_mark"],
                ["duplicate_line"],
                ["duplicate_line"],
                ["duplicate_line"],
                ["duplicate_line"],
                ["duplicate_line"],
                ["move_to",         {"extend": false, "to": "eol"}],
                ["select_to_mark"],
                ["split_selection_into_lines"],
                ["increment_selection"],
                ["move_to",         {"extend": false, "to": "eol"}],
                ["insert",          {"characters": ","}],
                ["join_lines"],
                ["clear_bookmarks", {"name": "mark"}],
                ["move_to",         {"extend": false, "to": "eol"}],
            ]
        }
    },
```

In case you are wondering how I came up with the commands, I recorded a macro
and copied the commands here and just cleaned them up.

## Install

To install this plugin you need to clone this repo under
`~/.config/sublime-text-3/Packages` folder.

## Todo

* Provide a repeat number for executing commands.
* Add more functionality to evaluating strings: `^`, `avg`, and `!` for factorial.
