#!/usr/bin/env python

"""
First version of pandocPyrun
@author : D'hulst Thomas
@author : Tayebi Ajwad

@version : 0.1.0
"""

import code as c
import hashlib
import os
import sys
from io import StringIO

from pandocfilters import (
    CodeBlock, Div, Image, LineBreak, Para, Str, Strong, get_caption,
    get_extension, get_value, toJSONFilter)


def init_console():
    """
    Initialize the interactive console with necessary functions we made

    Returns:
        code.InteractiveConsole: the console initialized
    """
    res = c.InteractiveConsole()
    res.push("import turtle")
    # command that set maximum speed to turtle [disabled because displays turtle screen for each convert]
    # res.push("turtle.speed(0)")
    # command that hides turtle screen [disabled because crashes]
    # res.push("turtle.getscreen()._root.withdraw()")
    res.push("from PIL import Image")
    res.push("""def turtle2image(destination):
        turtle.getscreen().getcanvas().postscript(file='tmp.eps')
        fig = Image.open('tmp.eps')
        fig.save(destination, lossless = True)
""")
    return res


logger = []  # debug array to print print using logger.append("hey there debug")
console = init_console()  # global console which execute code

#  keywords of possible classes
OUT_CODE = "CODE"
OUT_RES = "RES"
OUT_ALL = "ALL"
OUT_SHELL = "SHELL"
OUT_NONE = "NONE"

TYPE_PY = "PY"
TYPE_TURTLE = "TURTLE"
TYPE_PLOT = "PLOT"

SCOPE_GLOBAL = "GLOBAL"
SCOPE_LOCAL = "LOCAL"

MODE_STUDENT = "STUDENT"
MODE_DEBUG = "DEBUG"
MODE_PROF = "PROF"


GLOBAL_META = None  # global meta value
DEFAULT_OUT = OUT_CODE  # default value for OUT class
DEFAULT_MODE = MODE_STUDENT  # default value for MODE class
DEFAULT_SCOPE = SCOPE_GLOBAL  # default value for SCOPE class
DEFAULT_TYPE = TYPE_PY  # default value for TYPE class

URL_IMAGE_ERROR = "https://developers.google.com/maps/documentation/streetview/images/error-image-generic.png"

KEYWORD_CHECKED = "pyrunPass"  # keyword for checked codeblock

KEYWORD_BACKSLASH_N = "BACKSLASH_N"  # keyword for \n


def out_factory(params):
    """
    Factory method to return the Pandoc object of pyrun

    Args:
        out_val (str): the value associated to the out key
        out_type (str): the value associated to the type key
        id_block (str): the pandocfilters.CodeBlock's id_block
        code (str): the code to be processed
        local (str): the value associated to the scope key
        keyval (list): the associated key/values representing the classes

    Returns:
        list: the object containing all the pandocfilters blocks to display
    """
    out_val, out_type, id_block, code, local, keyval = params

    global MODE_PROF, MODE_DEBUG, MODE_STUDENT
    global TYPE_PLOT, TYPE_PY, TYPE_TURTLE
    global DEFAULT_MODE, DEFAULT_OUT, DEFAULT_SCOPE, DEFAULT_TYPE
    global OUT_ALL, OUT_CODE, OUT_NONE, OUT_RES, OUT_SHELL
    # change the stdout and execute the code
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    new_stdout = StringIO()
    sys.stdout = new_stdout
    sys.stderr = new_stdout

    new_console = None

    if local:
        new_console = init_console()

    # result string for the shell by shell version
    result_shell = ""
    for code_to_push in format_code(code):
        # if we have rafters in the block, we interpret it without them
        line = code_to_push[3:].lstrip() if code_to_push.startswith(">>> ") else code_to_push

        # capture of the string ".show()" for plot type
        if out_type == TYPE_PLOT:
            if line.find(".show()") != -1:
                caption, typef, dest, rep = get_dest_of_plot(keyval, code)
                line = line.replace(".show()", rep)
            else:
                caption, typef, _ = get_caption(keyval)
                dest = URL_IMAGE_ERROR

        if local:
            new_console.push(line)
        else:
            console.push(line)

        # if the shell by shell mode is selected
        if DEFAULT_MODE != MODE_DEBUG and out_type == TYPE_PY and out_val == OUT_SHELL:
            # get output line by line
            result_shell += code_to_push + new_stdout.getvalue()
            # reset stdout
            new_stdout = StringIO()
            sys.stdout = new_stdout
            sys.stderr = new_stdout

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    # get the out and print it in a new codeblock
    res = new_stdout.getvalue()

    # by default the result block is the codeblock with the code in it
    block = out_code(id_block, code)

    # we check the mode, then the type, then the val if needed
    if DEFAULT_MODE == MODE_DEBUG:
        if out_type == TYPE_PY:
            block = out_code(id_block, code) + out_res(id_block, res)
        elif out_type == TYPE_TURTLE:
            block = out_code(id_block, code) + out_turtle(id_block, keyval, code, new_console)
        elif out_type == TYPE_PLOT:
            block = out_code(id_block, code) + out_plot(id_block, caption, dest, typef)
    elif DEFAULT_MODE == MODE_PROF:
        if out_val == OUT_NONE:
            return out_none()
        if out_type == TYPE_PY:
            block = out_code(id_block, code) + out_res(id_block, res)
        elif out_type == TYPE_TURTLE:
            block = out_code(id_block, code) + out_turtle(id_block, keyval, code, new_console)
        elif out_type == TYPE_PLOT:
            block = out_code(id_block, code) + out_plot(id_block, caption, dest, typef)
        else:
            block = out_code(id_block, code)
    else:
        if out_type == TYPE_PY:
            if out_val == OUT_ALL:
                block = out_code(id_block, code) + out_res(id_block, res)
            elif out_val == OUT_NONE:
                return out_none()
            elif out_val == OUT_RES:
                block = out_res(id_block, res)
            elif out_val == OUT_SHELL:
                block = out_shell(id_block, result_shell)
        elif out_type == TYPE_PLOT:
            if out_val == OUT_RES:
                block = out_plot(id_block, caption, dest, typef)
            elif out_val == OUT_CODE:
                block = out_code(id_block, code)
            elif out_val == OUT_ALL:
                block = out_code(id_block, code) + out_plot(id_block, caption, dest, typef)
            elif out_val == OUT_NONE:
                return out_none()
            else:
                block = out_code(id_block, code)
        elif out_type == TYPE_TURTLE:
            if out_val == OUT_CODE:
                block = out_code(id_block, code)
            elif out_val == OUT_ALL:
                block = out_code(id_block, code) + out_turtle(id_block, keyval, code, new_console)
            elif out_val == OUT_RES:
                block = out_turtle(id_block, keyval, code, new_console)
            elif out_val == OUT_NONE:
                return out_none()
        else:
            block = out_code(id_block, code)

    # return a pandoc object with the right block.s in it
    return Div([id_block, ["pyrun"], []], block)


def out_none():
    """
    Manages NONE's out display which means nothing

    Returns:
        list: an empty list
    """
    return []


def out_res(id_block, res):
    """
    Manages RES's out display which means only the results

    Args:
        id_block (str): the pandocfilters.CodeBlock's id_block
        res (str): the results to print

    Returns:
        list: a list containing the pandocfilters.Div which represents the RES representation
    """
    return [Div([id_block, ["out"], []], [CodeBlock([id_block, ["python", KEYWORD_CHECKED], []], res)])]


def out_code(id_block, code):
    """
    Manages CODE's out display which means only the code

    Args:
        id_block (str): the pandocfilters.CodeBlock's id_block
        code (str): the code to print

    Returns:
        list: a list containing the pandocfilters.Div which represents the CODE representation
    """
    return [Div([id_block, ["in"], []], [CodeBlock([id_block, ["python", KEYWORD_CHECKED], []], code)])]


def out_shell(id_block, shell):
    """
    Manages SHELL's out display which means the code and the results shell by shell

    Args:
        id_block (str): the pandocfilters.CodeBlock's id_block
        shell (str): the shell to print

    Returns:
        list: a list containing the pandocfilters.Div which represents the SHELL representation
    """
    return [Div([id_block, ["inout"], []], [CodeBlock([id_block, ["python", KEYWORD_CHECKED], []], shell)])]


def out_plot(id_block, caption, dest, typef):
    """
    Manages PLOT's out display which means the mathplot image render

    Args:
        id_block (str): the pandocfilters.CodeBlock's id_block
        caption (str): the alt of the image
        dest (str): the url of the image
        typef (str): the title of the image

    Returns:
        list: a list containing the pandocfilters.Div which represents the PLOT representation
    """
    block = [Image([id_block, [], []], caption, [dest, typef])]
    # if the .show() isn't found, then add an error image
    if dest == URL_IMAGE_ERROR:
        block += [LineBreak(), Str("Command "), Strong([Str(".show()")]), Str(" not found.")]
    return [Div([id_block, ["plot"], []], [Para(block)])]


def out_turtle(id_block, keyval, code, new_console):
    """
    Manages TURTLE's out display which means the turtle image render

    Args:
        id_block (str): the pandocfilters.CodeBlock's id_block
        keyval (list): the associated key/values representing the classes
        code (str): the code for the turtle render
        new_console (code.InteractiveConsole): the interactive console

    Returns:
        list: a list containing the pandocfilters.Div which represents the TURTLE representation
    """
    # we push the line at the end of the code block, that's why we do it here
    # and not in the for loop in the factory method
    caption, typef, dest, rep = get_dest_of_turtle(keyval, code)
    if new_console is None:
        console.push(rep)
    else:
        new_console.push(rep)

    # gérer les erreurs avec la stdout et gérer le resize
    block = [Image([id_block, [], []], caption, [dest, typef])]
    return [Div([id_block, ["turtle"], []], [Para(block)])]


def pandoc_pyrun(key, value, format_block, meta):
    """
    Main receptacle of the filter's execution

    Args:
        key (str): the type of the read structure
        value (list): the native object beeing read
        format_block (str): the format_block of the targeted output
        meta (pandocfilters.Meta): the associated key/values representing the meta values

    Returns:
        list: the list of pandocfilters.Div if the read structure is a pandocfilters.CodeBlock, None otherwise
    """
    # get all global informations
    global GLOBAL_META, DEFAULT_OUT, DEFAULT_SCOPE, DEFAULT_MODE, DEFAULT_TYPE

    # use format_block or pypi doesn't compile
    _ = format_block

    # if the meta isn't set, take the input stream's pandoc meta
    if GLOBAL_META is None:

        # transform all key and data of metadata in uppercase to manage the case
        tmp_kv = list(meta.items())
        tmp_meta = dict()
        for key_kv, value_kv in tmp_kv:
            try:
                tmp_meta[key_kv.upper()] = value_kv["c"][0]["c"].upper()
            except AttributeError:
                # if the user input is incorrect
                continue

        GLOBAL_META = tmp_meta
        DEFAULT_OUT = tmp_meta["PANDOC_PYRUN_OUT"] if "PANDOC_PYRUN_OUT" in tmp_meta else DEFAULT_OUT
        DEFAULT_SCOPE = tmp_meta["PANDOC_PYRUN_SCOPE"] if "PANDOC_PYRUN_SCOPE" in tmp_meta else DEFAULT_SCOPE
        DEFAULT_MODE = tmp_meta["PANDOC_PYRUN_MODE"] if "PANDOC_PYRUN_MODE" in tmp_meta else DEFAULT_MODE
        DEFAULT_TYPE = tmp_meta["PANDOC_PYRUN_TYPE"] if "PANDOC_PYRUN_TYPE" in tmp_meta else DEFAULT_TYPE

    # if the block is a codeblock
    if key == "CodeBlock":
        # get values of this codeblock
        [[id_block, classes, keyval], code] = value

        # if the codeblock have to be compiled
        if not(KEYWORD_CHECKED in classes or (
            "pandocPyrun" not in classes
            and "py" not in classes
            and "python" not in classes
        )):

            # create the list of all keys
            # transform all key and data of metadata in uppercase to manage the case
            tmp_keyval = dict()
            for item_assoc in keyval:
                try:
                    # the file options must have the right file name
                    if item_assoc[0].upper() == "FILE":
                        tmp_keyval["FILE"] = item_assoc[1]
                    tmp_keyval[item_assoc[0].upper()] = item_assoc[1].upper()
                except AttributeError:
                    # if the user input is incorrect
                    continue

            # boolean true iff the scope is local
            local = tmp_keyval["SCOPE"] == SCOPE_LOCAL if "SCOPE" in tmp_keyval else DEFAULT_SCOPE == SCOPE_LOCAL
            # string value of out class
            out_val = tmp_keyval["OUT"] if "OUT" in tmp_keyval else DEFAULT_OUT
            # string value of type class
            out_type = tmp_keyval["TYPE"] if "TYPE" in tmp_keyval else DEFAULT_TYPE

            # add all code from file
            code = code if "FILE" not in tmp_keyval else get_code_from_file(tmp_keyval["FILE"], code)

            # start factory method to create the result's block
            return out_factory((out_val, out_type, id_block, code + "\n", local, keyval))
    # return nothing else
    return None


def get_code_from_file(filename, code):
    """
    Returns all the code contained in the given file

    Args:
        filename (str): the name of the file
        code (str): the code content of the block

    Returns:
        str: the content of the file
    """
    if not filename.endswith(".py"):
        return code
    precode = ""
    try:
        with open(filename, "r") as out:
            for line in out:
                precode += line
    except IOError as ioe:
        precode += f"#Something wrong happened while trying to open the file\n#{str(ioe)}\n"
    finally:
        precode += "\n" + code
    return precode


def format_code(code):
    """
    Format the content to get the code and the exec part split

    Args:
        code (str): the split code to compile
    """
    final = []
    code = code.replace("\\n", KEYWORD_BACKSLASH_N)
    lines = code.split("\n")
    res = ""
    # for each line in a codeblock
    for line in lines:
        # replace BACKSLASH_N by \n
        line = line.replace(KEYWORD_BACKSLASH_N, "\\n")

        # if it starts by an indent or a def, it means that we are in a function's definition
        if line.startswith("\t") or line.startswith(" ") or line.startswith("def"):
            # we add it to the function's definition
            res += line + "\n"
        else:
            # we flush the buffer of the last function's definition
            final.append(res)
            res = ""
            # we append the line
            final.append(line + "\n")
    # we take everything except the empty lines
    return [x.lstrip() for x in final if x != "" if x != "\n"]


def get_dest_of_plot(keyval, code):
    """
    Create the line which will generate the plot image

    Args:
        keyval (list): the associated key/values representing the classes
        code (str): the code for the plot

    Returns:
        tuple: the alt, the title and the url for the generated image and the line to compile to generate the plot image
    """
    caption, typef, keyvals = get_caption(keyval)
    _, keyvals = get_value(keyvals, "prog", "dot")
    filetype = get_extension(format, "png", html="png", latex="pdf")
    dest = (
        hashlib.sha1(code.encode(sys.getfilesystemencoding())).hexdigest()
        + "."
        + filetype
    )
    return caption, typef, dest, f".savefig('{dest}', bbox_inches='tight')"


def get_dest_of_turtle(keyval, code):
    """
    Create the line which will generate the turtle image

    Args:
        keyval (list): the associated key/values representing the classes
        code (str): the code for the turtle

    Returns:
        tuple: the alt, the title and the url for the generated image and the line to compile to generate turtle image
    """
    caption, typef, keyvals = get_caption(keyval)
    _, keyvals = get_value(keyvals, "prog", "dot")
    filetype = get_extension(format, "png", html="png", latex="pdf")
    dest = (
        hashlib.sha1(code.encode(sys.getfilesystemencoding())).hexdigest()
        + "."
        + filetype
    )
    return caption, typef, dest, f"turtle2image('{dest}')"


def main():
    """Main function for this pandoc filter
    """
    # start our filter in input stream
    toJSONFilter(pandoc_pyrun)

    # if the logger isn't empty, create a log.txt file
    if logger != []:
        with open("log.txt", "w") as file:
            file.writelines(logger)

    # remove all temporary file
    if os.path.exists("tmp.eps"):
        os.remove("tmp.eps")


if __name__ == "__main__":
    main()
