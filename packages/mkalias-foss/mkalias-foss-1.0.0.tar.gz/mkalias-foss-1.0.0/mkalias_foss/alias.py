import osascript


class Alias:
    #  Constants used for create method to access returned tuple
    CMD_STRING = 0
    CODE = 1
    OUT = 2
    ERROR = 3

    @staticmethod
    def create(source, destination, name=None) -> tuple:
        """
        Creates and runs the AppleScript required to create the alias
        :param source: File or Directory to create an alias of
        :param destination: Destination directory of the new alias
        :param name: Name of new alias - OPTIONAL
        :return: tuple containing the AppleScript Created, Code, Output of AppleScript, and Errors - in that order
        """

        if name is None:
            cmd_string = 'tell application "Finder" to make alias file to POSIX file "{}" at POSIX file "{}"' \
                .format(source, destination)
        else:
            cmd_string = 'tell application "Finder" to make alias file to POSIX file "{}" at POSIX file "{}"' \
                         ' with properties {{name:"{}"}}'.format(source, destination, name)

        code, out, error = osascript.run(cmd_string)

        return cmd_string, code, out, error
