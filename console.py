#!/usr/bin/python3
"""Custom Command Console
"""
import cmd

class HBNBCommand(cmd.Cmd):
    """Create the HBNB command interpreter

    Attributes:
        prompt (str): command prompt
    """

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """
        Quit the interpreter
        """
        print("")
        return True

    
    def do_EOF(self, arg):
        """
        Handles the EOF (End of File) signal

        Args:
            line: input line that triggers EOF signal
        """
        return True

if __name__ == "__main__":
    HBNBCommand().cmdloop()
