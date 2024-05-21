#!/usr/bin/python3
"""Custom Command Console
"""
import cmd
from models import storage
from models.base_model import BaseModel

def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            output_token = [i.strip(",") for i in lexer]
            output_token.append(brackets.group())
            return output_token
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        output_token = [i.strip(",") for i in lexer]
        output_token.append(curly_braces.group())
        return output_token

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
    
    def do_create(self, arg):
        """Usage: create <class>
        Create new instance of BaseModel,saves it (to the JSON file) and prints the id
        """
        output_arg = parse(arg)
        if len(output_arg) == 0:
            print("** class name missing **")
        elif output_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(output_arg[0])().id)
            storage.save()
    
    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Prints the string representation of an instance based on the class name and id
        """
        output_arg = parse(arg)
        objdict = storage.all()
        if len(output_arg) == 0:
            print("** class name missing **")
        elif output_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(output_arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(output_arg[0], output_arg[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(output_arg[0], output_arg[1])])
    
    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Deletes an instance based on the class name and id.(save the change into the JSON file)
        """
        output_arg = parse(arg)
        objdict = storage.all()
        if len(output_arg) == 0:
            print("** class name missing **")
        elif output_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(output_arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(output_arg[0], output_arg[1]) not in objdict:
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(output_arg[0], output_arg[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Prints all string representation of all instances based or not on the class name.
        """
        output_arg = parse(arg)
        if len(output_arg) > 0 and output_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objt = []
            for obj in storage.all().values():
                if len(output_arg) > 0 and output_arg[0] == obj.__class__.__name__:
                    objt.append(obj.__str__())
                elif len(output_arg) == 0:
                    objt.append(obj.__str__())
            print(objt)

    def do_update(self, arg):
        """Usage: update <class name> <id> <attribute name> <attribute value>
        """

        output_arg = parse(arg)
        objdict = storage.all()

        if len(output_arg) == 0:
            print("** class name missing **")
            return False
        if output_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(output_arg) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(output_arg[0], output_arg[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(output_arg) == 2:
            print("** attribute name missing **")
            return False
        if len(output_arg) == 3:
            try:
                type(eval(output_arg[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(output_arg) == 4:
            obj = objdict["{}.{}".format(output_arg[0], output_arg[1])]
            if output_arg[2] in obj.__class__.__dict__.keys():
                result = type(obj.__class__.__dict__[output_arg[2]])
                obj.__dict__[output_arg[2]] = result(output_arg[3])
            else:
                obj.__dict__[output_arg[2]] = output_arg[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(output_arg[0], output_arg[1])]
            for i, j in eval(output_arg[2]).items():
                if (i in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[i]) in {str, int, float}):
                    result = type(obj.__class__.__dict__[i])
                    obj.__dict__[i] = result(j)
                else:
                    obj.__dict__[i] = j
        storage.save()

    def do_EOF(self, arg):
        """
        Handles the EOF (End of File) signal

        Args:
            line: input line that triggers EOF signal
        """
        return True

if __name__ == "__main__":
    HBNBCommand().cmdloop()
