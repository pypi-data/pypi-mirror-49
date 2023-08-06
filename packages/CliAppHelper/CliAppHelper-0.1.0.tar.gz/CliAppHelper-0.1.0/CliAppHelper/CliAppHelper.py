from sys import argv

from CliAppHelper.Flags import Flags


class CliAppHelper:
    def __init__(self, help_text, options):
        args = argv[1:]

        self.help_text = help_text

        spec = options.get("flags")
        auto_help = options.get("auto_help", True)

        if auto_help:
            spec.update({"help": {
                "type": "boolean",
                "alias": "h",
                "default": True
            }})

        self.__flags = Flags(spec)

        self.__flags.parse_args(args)

        if auto_help and self.__flags.flags.get("help"):
            self.show_help()

    def get_flags(self):
        return self.__flags.flags

    def show_help(self):
        print(self.help_text)
