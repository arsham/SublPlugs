import sublime_plugin
import sublime


class MateCommandsCommand(sublime_plugin.TextCommand):
    """
    Dedicated quick panel for this plugin's commands.
    """

    commands = {
        0: ("unfold_all", "Unfold All", {}),
        1: ("fold_comments", "Fold Comments", {}),
        2: ("unfold_comments", "Unfold Comments", {}),
        3: ("fold_by_level", "Fold One", {"level": 1}),
        4: ("fold_by_level", "Fold Two", {"level": 2}),
        5: ("fold_by_level", "Fold Three", {"level": 3}),
        6: ("fold_by_level", "Fold Four", {"level": 4}),
        7: ("fold_by_level", "Fold Five", {"level": 5}),
        8: ("fold_by_level", "Fold Six", {"level": 6}),
    }

    def run(self, edit):
        commands = [c[1] for c in list(self.commands.values())]
        self.view.window().show_quick_panel(commands, self.run_command, sublime.MONOSPACE_FONT)

    def run_command(self, choice):
        if choice < 0:
            return
        command = self.commands[choice]
        self.view.run_command(command[0], command[2])
