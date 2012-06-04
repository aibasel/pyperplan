#
# This file is part of pyperplan.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

import logging
import os
import subprocess
import sys
import traceback


def command_available(command):
    """Returns true iff command can be called without errors.

    command should be a list. For checking the availbability of a command it
    is common prectice to call the command's help method, e.g.

    ['validate', '-h'] or ['minisat', '--help']
    """
    try:
        subprocess.check_call(command, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, OSError) as err:
        return False


def remove(filename):
    """Removes the file under "filename" and catches any errors.

    If filename points to a directory it is not removed.
    """
    try:
        os.remove(filename)
    except OSError:
        pass


def import_python_file(filename, dirs=None):
    filename = os.path.abspath(filename)
    dirs = dirs or []
    parent_dir = os.path.dirname(filename)
    dirs.append(parent_dir)
    for dir in dirs:
        if dir not in sys.path:
            sys.path.insert(0, dir)
    filename = os.path.normpath(filename)
    filename = os.path.basename(filename)
    if filename.endswith('.py'):
        module_name = filename[:-3]
    elif filename.endswith('.pyc'):
        module_name = filename[:-4]
    else:
        module_name = filename

    # Reload already loaded modules to actually get the changes.
    if module_name in sys.modules:
        return reload(sys.modules[module_name])

    try:
        module = __import__(module_name)
        return module
    except ImportError as err:
        print(traceback.format_exc())
        logging.critical('File "%s" could not be imported: %s' % (filename, err))
