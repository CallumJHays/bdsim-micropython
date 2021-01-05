from subprocess import check_call, check_output
from pathlib import Path
from bdsim.core import blocklist


def generate_bdsim_pyi(self, input, output):
    """
    input: the input file or module directory path
    output: the output file or output package path (parent of output module directory)
    """

    print('called transpile', input, output)
    print(Path(input), Path(output))

    # produce pyi files for each file in the module
    # call stubgen with the specific python version (a little hacky but it works)
    check_call(['python', '-c', """import sys
from mypy.stubgen import main
sys.argv = ["stubgen", "%s", "-o", "%s"]
main()""" % (str(input), str(output))])
