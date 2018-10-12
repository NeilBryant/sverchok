# This file is part of project Sverchok. It's copyrighted by the contributors
# recorded in the version control history of the file, available from
# its original location https://github.com/nortikin/sverchok/commit/master
#  
# SPDX-License-Identifier: GPL3
# License-Filename: LICENSE

def check_bgl_availability():
    import importlib
    bgl_spec = importlib.util.find_spec("bgl")
    return bgl_spec is not None
