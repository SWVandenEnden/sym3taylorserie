#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Command line interface

    Copyright (C) 2026 Gien van den Enden - swvandenenden@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import symexpress3
import sym3taylorserie


def CalcSolution( taylorString, taylorSteps, taylorVar, taylorValue, outputFormat ):
  """
  Create the Taylor serie
  """
  if len( taylorString ) == 0:
    print( "No parameters are given, nothing to do" )
    return

  # default output format, solutions as string and calculated values
  if outputFormat in( "", None ):
    outputFormat = "s"

  try:

    clsTaylor = sym3taylorserie.Sym3TaylorSerie()
    output   = None

    # set variables
    # pylint: disable=multiple-statements
    if taylorSteps != None: clsTaylor.steps     = taylorSteps
    if taylorVar   != None: clsTaylor.diffVar   = taylorVar
    if taylorValue != None: clsTaylor.baseValue = taylorValue

    clsTaylor.formula  = taylorString

    if 'h' in outputFormat:
      output = symexpress3.SymToHtml( None, "Taylor serie" )
      clsTaylor.htmlOutput = output

    # calculate the solutions
    clsTaylor.calcTaylorSerie()

    # output data
    for cOutput in outputFormat:
      if cOutput == "s":
        print( f"Taylor serie: {clsTaylor.taylorSerie}" )

      elif cOutput == "h":
        pass # do nothing html (output) is already set

      else:
        print( f"Unknown output format '{cOutput}' ignored" )

    if output != None:
      output.closeFile()
      output = None

  except Exception as exceptAll: # pylint: disable=broad-exception-caught
    print( f"Error: {str( exceptAll )}" )



def DisplayVersion():
  """
  Display version information
  """
  print( "Version    : " + sym3taylorserie.__version__    )

  print( "Author     : " + sym3taylorserie.__author__     )
  print( "Copyright  : " + sym3taylorserie.__copyright__  )
  print( "License    : " + sym3taylorserie.__license__    )
  print( "Maintainer : " + sym3taylorserie.__maintainer__ )
  print( "Email      : " + sym3taylorserie.__email__      )
  print( "Status     : " + sym3taylorserie.__status__     )


def DisplayHelp():
  """
  Display help
  """
  print( "Create a Taylor series of a given formula" )
  print( " " )
  print( "usage: python -m sym3taylorserie [options] [arg]" )
  print( "options: " )
  print( "  -h           : Help" )
  print( "  -v           : Version information" )
  print( "  -o <format>  : Output format" )
  print( "                 s - string format (default)" )
  print( "                 h - html" )
  print( "  -s           : Number of derivative to do, default is 20" )
  print( "  -d           : Variable to differentiate, default is 'x'" )
  print( "  -p           : Point to evaluate, default is 0. It must be an integer" )
  print( "arg: <symexpress3 string>" )
  print( " " )
  print( "Example: " )
  print( 'python -m sym3taylorserie "(x+1)^^3"' )
  print( 'python -m sym3taylorserie -o s -s 20 -d x -p 0 "(x+1)^^3"' )

def CommandLine( argv ):
  """
  Process the command line parameters
  """
  outputFormat = ""
  taylorString = ""
  taylorSteps  = None  # number of steps
  taylorVar    = None  # variable to differentiate
  taylorValue  = None  # point to evalutatie

  nrarg = len( argv )

  # nothing given, then display help
  if nrarg <= 1:
    DisplayHelp()

  mode = ""
  for iCnt in range( 1, nrarg ) :
    cArg = argv[ iCnt ]

    if mode == "output":
      outputFormat = cArg
      mode = ""
      continue

    if mode == "steps":
      taylorSteps = int( cArg )
      mode = ""
      continue

    if mode == "variable":
      taylorVar = cArg
      mode = ""
      continue

    if mode == "point":
      taylorValue = int( cArg )
      mode = ""
      continue


    if cArg == "-h" :
      DisplayHelp()
      return  # direct stop by help

    if cArg == "-v" :
      DisplayVersion()
      return  # direct stop by version information

    # pylint: disable=multiple-statements
    if   cArg == "-o": mode = "output"
    elif cArg == "-s": mode = "steps"
    elif cArg == "-d": mode = "variable"
    elif cArg == "-p": mode = "point"

    else:
      if cArg.startswith( "-" ):
        print( f"Unknown option: {cArg}, use -h for help")
      else:
        # collect arguments
        taylorString = cArg

  CalcSolution( taylorString, taylorSteps, taylorVar, taylorValue, outputFormat )


# ---------------------------
# The end
# ---------------------------
