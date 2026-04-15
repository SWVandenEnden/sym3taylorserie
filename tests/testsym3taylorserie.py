#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Test Taylor serie

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

from datetime import datetime

import symexpress3
import sym3taylorserie

testData = [ # 1
             { 'formula'   : '(x+1)^^3'
             , 'steps'     : 20
             , 'diffVar'   : 'x'
             , 'baseValue' : 0
             , 'check'     : '1 + 3 * x *  factorial( 1 )^^-1 + 6 * x^^2 *  factorial( 2 )^^-1 + 6 * x^^3 *  factorial( 3 )^^-1'
             }
           , # 2
             { 'formula'   : '(x+1)^^3'
             , 'steps'     : 10
             , 'diffVar'   : 'x'
             , 'baseValue' : 3
             , 'check'     : '64 + 48 * (x + (-1) * 3) *  factorial( 1 )^^-1 + 24 * (x + (-1) * 3)^^2 *  factorial( 2 )^^-1 + 6 * (x + (-1) * 3)^^3 *  factorial( 3 )^^-1'
             }
           , # 3
             { 'formula'   : 'sin(x)'
             , 'steps'     : 10
             , 'diffVar'   : 'x'
             , 'baseValue' : 0
             , 'check'     : 'x *  factorial( 1 )^^-1 + (-1) * x^^3 *  factorial( 3 )^^-1 + x^^5 *  factorial( 5 )^^-1 + (-1) * x^^7 *  factorial( 7 )^^-1 + x^^9 *  factorial( 9 )^^-1'
             }
           , # 4
             { 'formula'   : '1/(1+x)'
             , 'steps'     : 4
             , 'diffVar'   : 'x'
             , 'baseValue' : 0
             , 'check'     : '1 + (-1) * x *  factorial( 1 )^^-1 + 2 * x^^2 *  factorial( 2 )^^-1 + (-6) * x^^3 *  factorial( 3 )^^-1'
             }
           ]

startTime = datetime.now()

# test taylor serie
iTests = 0
iGood  = 0
iBad   = 0

clsTaylor = sym3taylorserie.Sym3TaylorSerie()

for dData in testData :
  iTests += 1
  print( f"Test: {iTests}", end='\r')

  clsTaylor.formula   = dData.get( 'formula'   )
  clsTaylor.steps     = dData.get( 'steps'     )
  clsTaylor.diffVar   = dData.get( 'diffVar'   )
  clsTaylor.baseValue = dData.get( 'baseValue' )

  clsTaylor.calcTaylorSerie()

  clsCheck = symexpress3.SymFormulaParser( dData.get( 'check' )  )

  clsCheck.optimize()

  if not clsCheck.isEqual( clsTaylor.taylorSerie ) :
    iBad += 1

    print( f'Entry {iTests} not equal'  )
    print( f'{clsTaylor.taylorSerie}, expected: {clsCheck}' )

  else:
    iGood += 1

endTime   = datetime.now()
timeInSec = ( endTime - startTime ).total_seconds()

print( f"Number of tests: {iTests}, passed: {iGood}, failed; {iBad}, total time: {timeInSec} (sec)" )
