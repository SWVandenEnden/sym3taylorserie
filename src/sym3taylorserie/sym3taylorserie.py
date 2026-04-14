#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Taylor series

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


    Based on: https://en.wikipedia.org/wiki/Taylor_series

"""
# from datetime import datetime

import symexpress3

class Sym3TaylorSerie():
  """
  Caluculate the Taylor serie of a given sym3 expression
  """

  def __init__( self ):
    # defaults
    self._formula       = ""    # sym3 formula in string format
    self._steps         = 20    # max number of iterations
    self._output        = None  # symexpress3.SymToHtml object
    self._baseValue     = 0     # the base value of the Taylor series
    self._diffVar       = 'x'   # the differentiate variable
    self._taylorValues  = []    # array of the Taylor values
    self._taylorSerie   = None  # sym3 expression of Taylor serie
    self._complete      = False # Is Taylor expansion complete (serie is ended in the given steps)

  @property
  def formula(self):
    """
    Symexpress3 formula
    """
    return self._formula

  @formula.setter
  def formula(self, val):
    self._formula = symexpress3.ConvertToSymexpress3String( val )


  @property
  def steps(self):
    """
    Number of iterations
    """
    return self._steps

  @steps.setter
  def steps(self, val):
    if not isinstance( val, int ):
      raise NameError( f'steps is incorrect: {type(val)}, expected int' )
    if val < 2:
      raise NameError( f'steps ({val}) must be greate or equal then 2' )

    self._steps = val

  @property
  def htmlOutput(self):
    """
    Set html output object
    """
    return self._output

  @htmlOutput.setter
  def htmlOutput(self, val):
    if val != None and ( not isinstance( val, symexpress3.SymToHtml )) :
      raise NameError( f'htmlOutput is incorrect: {type(val)}, expected SymToHtml object ' )
    self._output = val

  @property
  def baseValue(self):
    """
    The base (start) value of Taylor serie
    """
    return self._baseValue

  @baseValue.setter
  def baseValue(self, val):
    if not isinstance( val, int ):
      raise NameError( f'baseValue is incorrect: {type(val)}, expected int' )
    self._baseValue = val


  @property
  def diffVar(self):
    """
    The differentiate variable
    """
    return self._diffVar

  @diffVar.setter
  def diffVar(self, val):
    if not isinstance( val, str ):
      raise NameError( f'diffVar is incorrect: {type(val)}, expected str' )
    if len( val ) == 0:
      raise NameError( 'diffVar may not be empty' )
    self._diffVar = val

  @property
  def taylorComplete(self):
    """
    Is the Taylor serie ended within the given steps
    """
    return self._complete

  @property
  def taylorValues(self):
    """
    The Taylor values, each value is a sym3 expression
    """
    return self._taylorValues


  @property
  def taylorSerie(self):
    """
    The Taylor serie as sym3 expression
    """
    return self._taylorSerie

  #
  # Calculate the Taylor serie
  #
  def calcTaylorSerie(self):
    """
    Calculate the Taylor values and serie
    """
    #
    # a = base value
    # Taylor Serie = f(a) + f'(a) ( x - a )^1   f''(a) ( x - a )^2   f'''(a) ( x - a )^3
    #                       ---------------   + ------------------ + -------------------
    #                           1!                2!                   3!

    # reset global answer
    self._taylorValues = []
    self._taylorSerie  = None
    self._complete     = False

    if self._output != None:
      # curDateTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

      # self._output.writeLine( 'Taylorserie solution' )
      self._output.writeLine( 'Based on <a target="_blank" href="https://en.wikipedia.org/wiki/Taylor_series">https://en.wikipedia.org/wiki/Taylor_series</a>' )
      self._output.writeLine( '' )
      # self._output.writeLine( f'Date/time: {curDateTime}' )
      # self._output.writeLine( '' )
      self._output.writeLine( f'Calculation point: {self.baseValue}' )
      self._output.writeLine( f'Differentiate variable: {self.diffVar}' )
      self._output.writeLine( f'Maximum number of steps: {self.steps}' )
      self._output.writeLine( '' )

    objStartFormula = symexpress3.SymFormulaParser( self.formula )
    objStartFormula.optimize()

    if self._output != None:
      self._output.writeSymExpressWithStr( objStartFormula, "Formula to convert into Taylor serie" )

    dVars = objStartFormula.getVariables()

    if self.diffVar not in dVars:
      cError = f"Differentiate variable '{self.diffVar}' does not exist in the formula"
      if self._output != None:
        self._output.writeLine( cError )
      raise NameError( cError )

    # calc value
    dVarReplace = {}
    dVarReplace[ self.diffVar ] = str( self.baseValue )

    sym3DiffVar = symexpress3.SymVariable( self.diffVar )

    iStep = 0
    while iStep < self.steps:

      # check if derivative or integral is available in formula
      dFunc = objStartFormula.getFunctions()
      if 'integral' in dFunc:
        cError = "Integrals not supported in Taylor series"
        if self._output != None:
          self._output.writeLine( cError )
        raise NameError( cError )

      if 'derivative' in dFunc:
        cError = "Derivative not supported in Taylor series"
        if self._output != None:
          self._output.writeLine( cError )
        raise NameError( cError )


      objCalcFormula = objStartFormula.copy()

      objCalcFormula.replaceVariable( dVarReplace )
      if self._output != None:
        self._output.writeSymExpressWithStr( objCalcFormula, f"Step {iStep} value" )

      objCalcFormula.optimizeExtended()
      if self._output != None:
        self._output.writeSymExpressWithStr( objCalcFormula, f"Step {iStep} value optimized" )

      # collect all the Taylor values
      self._taylorValues.append( objCalcFormula )

      # check if var still exist
      dVars = objStartFormula.getVariables()
      if self.diffVar not in dVars:
        break

      iStep += 1

      # next derivative formula
      nextFormula = symexpress3.SymExpress( '*' )
      fncDerivative = symexpress3.SymFunction( 'derivative' )
      fncDerivative.add( objStartFormula )
      fncDerivative.add( sym3DiffVar )
      nextFormula.add( fncDerivative )
      nextFormula.optimize()

      if self._output != None:
        self._output.writeSymExpressWithStr( nextFormula, f"Step {iStep} derivative" )

      nextFormula.optimizeExtended()
      objStartFormula = nextFormula



    if len( self._taylorValues ) < self._steps:
      self._complete  = True

    self._taylorSerie = symexpress3.SymExpress( '+' )
    for iStep, taylorVar in enumerate( self._taylorValues ):
      if iStep == 0:
        self._taylorSerie.add( taylorVar )
      else:
        # x^<step>  | (x-a)^<step>
        symX  = None
        if self.baseValue != 0 :
          # x - a
          symA = symexpress3.SymFormulaParser( '-1 * ' + str( self.baseValue  ))
          symX = symexpress3.SymExpress( '+' )
          symX.add( sym3DiffVar )
          symX.add( symA )
        else :
          symX = sym3DiffVar.copy()

        symX.powerCounter = iStep

        # 1/<step>!
        symFact = symexpress3.SymFunction( 'factorial' )
        symFact.add( symexpress3.SymNumber( 1, iStep, 1 ))
        symFact.powerCounter =  1
        symFact.powerSign    = -1

        # all to gather
        symStep = symexpress3.SymExpress( '*' )
        symStep.add( taylorVar )
        symStep.add( symX )
        symStep.add( symFact )

        self._taylorSerie.add( symStep )

    self._taylorSerie.optimize()

    if self._output != None:
      self._output.writeLine( '' )
      self._output.writeSymExpressWithStr( self._taylorSerie, "Taylor serie" )

      if self.taylorComplete != True:
        self._output.writeLine( f'Taylor serie is not ended within the given steps ({self._steps})' )


# ---------------------------
# The end
# ---------------------------
