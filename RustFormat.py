import sublime
import sublime_plugin
import subprocess


def is_rust(view):
    return "source.rust" in view.scope_name(0)


def settings():
    return sublime.load_settings('RustFormat.sublime-settings')


class RustFormatCommand(sublime_plugin.TextCommand):

    def is_enabled(self):
        return is_rust(self.view)

    def run(self, edit):
        binary = settings().get('rust_format_binary') or 'rustfmt'
        rustfmt = subprocess.Popen(
            [binary, '--write-mode=overwrite', self.view.file_name()],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=False,
            universal_newlines=True)
        output, errors = rustfmt.communicate()
        if settings().get('rust_format_debug', False):
            print('RustFormat: ', output, '\nErrors:', errors)


class RustFormatListener(sublime_plugin.EventListener):

    def on_post_save_async(self, view):
        if is_rust(view) and settings().get('rust_format_on_save', False):
            view.run_command('rust_format')
