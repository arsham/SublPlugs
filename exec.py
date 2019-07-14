import sublime
import sublime_plugin


class ExecCommand(sublime_plugin.WindowCommand):
    """
    Runs a series of commands one by one.
    """

    def run(self, commands):

        for command in commands:
            if not command:
                continue

            name, args = command[0], command[1:]
            self.window.run_command(name, *args)
