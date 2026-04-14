# pylint: disable=invalid-name
"""
Command line handling
"""

import sys

if __name__ == '__main__':
  from sym3taylorserie import taylorseriecmd
  taylorseriecmd.CommandLine( sys.argv )
