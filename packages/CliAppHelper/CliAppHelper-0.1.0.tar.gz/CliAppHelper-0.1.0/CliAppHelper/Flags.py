class Flags:
    def __init__(self, spec):
        self.spec = spec
        self.alias_map = self.populate_alias_map()
        self.flags = {}

    def populate_alias_map(self):
        alias_map = {}

        for key in self.spec.keys():
            alias = self.spec.get(key).get("alias")

            if alias is not None:
                alias_map.update({alias: key})

        return alias_map

    @staticmethod
    def is_long_arg(arg):
        return arg.startswith("--")

    @staticmethod
    def is_short_arg(arg):
        return arg.startswith("-") and not Flags.is_long_arg(arg)

    def is_flag(self, arg):
        if Flags.is_long_arg(arg):
            flag = arg[2:]
        elif Flags.is_short_arg(arg):
            short_arg = arg[1:]
            flag = self.alias_map.get(short_arg)
        else:
            flag = None

        return flag and self.spec.get(flag)

    def get_flag_from_arg(self, arg):
        if not self.is_flag(arg):
            return None

        if Flags.is_long_arg(arg):
            return arg[2:]

        short_arg = arg[1:]
        return self.alias_map.get(short_arg)

    def parse_args(self, args):
        i = 0
        while i < len(args):
            arg = args[i]

            if self.is_flag(arg):
                flag = self.get_flag_from_arg(arg)
                flag_spec = self.spec.get(flag)
                next_arg = args[i + 1] if i + 1 < len(args) else None

                if flag_spec == "boolean":
                    if next_arg == "True":
                        value = True
                    elif next_arg == "False":
                        value = False
                    else:
                        value = flag_spec.get("default")
                elif next_arg and not self.is_flag(next_arg):
                    value = next_arg
                else:
                    value = flag_spec.get("default")

                self.flags.update({flag: value})

            i += 1



