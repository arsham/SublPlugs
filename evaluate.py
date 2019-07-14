"""This module evaluates the selected text"""

import datetime
import math
import sublime
import sublime_plugin


class EvaluateCommand(sublime_plugin.TextCommand):
    """
    Evaluates selected text in all regions
    """

    def run(self, edit):
        for region in self.view.sel():
            string = self.view.substr(region)
            result, err = evaluate_string(string)
            if err:
                msg = "Error evaluating {input}: {err}".format(
                    err=err,
                    input=string,
                )
                sublime.status_message(msg)
                print(msg)
                continue
            self.view.replace(edit, region, str(result))


def evaluate_string(string):
    """
    Returns the result as integer and an error if could not evaluate the string
    as second value.
    """
    result = 0
    err = None
    try:
        sanitized = string.strip()
        result = eval(sanitized, {
            "math": math,
            "datetime": datetime
        })
    except Exception as e:
        err = e
    return result, err
