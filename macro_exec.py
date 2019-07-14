import sublime
import sublime_plugin


MACRO_FILE = "SublimeMate.sublime-macro"


class MacroExecCommand(sublime_plugin.WindowCommand):
    """
    Runs a series of commands one by one.
    """

    def run(self, commands):

        for command in commands:
            if not command:
                continue

            name, args = command[0], command[1:]
            self.window.run_command(name, *args)


class MacroRecordCommand(sublime_plugin.WindowCommand):
    """
    Start/Stop recording macros.
    """

    command_list = []
    is_recording = False
    macros = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_macros()

    def _load_macros(self):
        resource = sublime.find_resources(MACRO_FILE)
        if not resource:
            return

        resource = sublime.load_resource(resource[0])
        if not resource:
            return

        for key, value in enumerate(sublime.decode_value(resource)):
            self.macros[key] = value

    def run(self, action="record"):
        """
        Starts recording if not started already, otherwise it stops recording.
        Available actions: record, repeat, save. Default action is record.
        """
        if action == "repeat" and MacroRecordCommand.is_recording:
            sublime.status_message("cannot repeat in middle of recording")
            return

        if action not in ["record", "repeat", "save", "select", ""]:
            sublime.status_message("unknown action")
            return

        if action == "repeat":
            self._repeat(MacroRecordCommand.command_list)
            return

        if action == "save":
            self.window.show_input_panel(
                "caption",
                "initial_text",
                self._persist,
                None,
                None,
            )
            return

        if action == "select":
            self._list()
            return

        self._record()

    def _record(self):
        if not MacroRecordCommand.is_recording:
            sublime.status_message("recording macro")
            MacroRecordCommand.is_recording = True
            MacroRecordCommand.command_list = []
        else:
            sublime.status_message("finished recording macro")
            MacroRecordCommand.is_recording = False

    def _repeat(self, commands):
        sublime.status_message("repeating last macro")
        for command in commands.copy():
            if not command:
                continue

            name, args = command[0], command[1:]
            self.window.run_command(name, *args)

    def _persist(self, caption):
        sublime.status_message("saving last macro")
        sublime.load_settings(MACRO_FILE) \
            .set(caption, MacroRecordCommand.command_list)

        sublime.save_settings(MACRO_FILE)
        self._load_macros()

    def _list(self):
        if not self.macros:
            sublime.status_message("no macros recorded yet")
            return

        items = []
        for i in range(len(self.macros)):
            items.append(self.macros[i])
        sublime.active_window().show_quick_panel(items, self._run_macro, sublime.MONOSPACE_FONT)

    def _run_macro(self, choice):
        if choice < 0:
            return
        name = self.macros[choice]
        macro = sublime.load_settings(MACRO_FILE).get(name)
        self._repeat(macro)


class MacroExecListener(sublime_plugin.EventListener):
    """
    Records user's actions after the trigger has been made, then records them as
    a command that can be run with exec command.
    """

    excempt = ('sublime_bookmark', 'macro_record')

    def record(self, input):
        if not input or input[0] in self.excempt:
            return

        if MacroRecordCommand.is_recording:
            MacroRecordCommand.command_list.append(input)

    def on_new(self, view):
        self.record(('new_file',))

    def on_close(self, view):
        self.record(('close',))

    def on_modified(self, view):
        if not MacroRecordCommand.is_recording:
            return

        regions = view.sel()
        for region in regions:
            last_reg = sublime.Region(region.a - 1, region.a)
            char = view.substr(last_reg)
            self.record(("insert", {"characters": char}))

    def on_text_command(self, view, command_name, args):
        self.record((command_name, args))

    def on_window_command(self, window, command_name, args):
        self.record((command_name, args))
