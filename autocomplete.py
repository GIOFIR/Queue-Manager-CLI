import readline

COMMANDS = [
    "new",
    "add",
    "save",
    "save-all",
    "load",
    "show-all",
    "show-queue",
    "delete",
    "exit",
    "clear-logs",
    "set-log-level"
]

def completer(text, state):
    """Return the next possible completion for 'text'."""
    options = [cmd for cmd in COMMANDS if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    return None

def enable_autocomplete():
    """Enable tab completion in CLI."""
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
