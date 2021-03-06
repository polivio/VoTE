#!/usr/bin/env python
# encoding: utf-8
# Copyright (C) 2018 John Törnblom
#
# This file is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not see
# <http://www.gnu.org/licenses/>.
'''
Ensure that the probabilities predicted by a random forest classifier
trained to classify digits are always within the range [0, 1].
'''

import sys
import vote

from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_digits


def is_valid_probability(mapping):
    minval = min([mapping.outputs[dim].lower
                  for dim in range(mapping.nb_outputs)])
                   
    maxval = max([mapping.outputs[dim].upper
                  for dim in range(mapping.nb_outputs)])

    if minval >= 0 and maxval <= 1:
        return vote.PASS
    elif vote.mapping_precise(mapping):
        return vote.FAIL
    else:
        return vote.UNSURE


print('Training classifier')
digits = load_digits()
m = RandomForestClassifier(n_estimators=10)
m.fit(digits.data, digits.target)

print('Verifying classifier')
e = vote.Ensemble.from_sklearn(m)
if e.absref(is_valid_probability):
    print('PASS')
else:
    print('FAIL')
    sys.exit(1)

