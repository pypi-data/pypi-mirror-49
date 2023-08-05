# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Frootlab
# Copyright (C) 2013-2019 Patrick Michl
#
# This file is part of Nemoa, https://www.frootlab.org/nemoa
#
#  Nemoa is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Nemoa is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with
#  Nemoa. If not, see <http://www.gnu.org/licenses/>.
#

__copyright__ = '2019 Frootlab'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Frootlab Developers'
__email__ = 'contact@frootlab.org'
__authors__ = ['Patrick Michl <patrick.michl@frootlab.org>']

import nemoa.model.analysis
import nemoa.model.builder
import nemoa.model.classes
import nemoa.model.evaluation
import nemoa.model.exports
import nemoa.model.imports
import nemoa.model.morphisms

def build(*args, **kwds):
    """Create model dictionary from building script."""
    return nemoa.model.builder.build(*args, **kwds)

def copy(model, *args, **kwds):
    """Create copy of model instance."""
    return new(**model.get('copy'))

def create(*args, **kwds):
    """Create model instance from building script."""
    return new(**build(*args, **kwds))

def evaluate(*args, **kwds):
    """Evaluate model instance."""
    return nemoa.model.evaluation.evaluate(*args, **kwds)

def evaluate_new(*args, **kwds):
    """Evaluate model instance."""
    return nemoa.model.analysis.evaluate(*args, **kwds)

def load(*args, **kwds):
    """Import model dictionary from file."""
    return nemoa.model.imports.load(*args, **kwds)

def new(*args, **kwds):
    """Create model instance from model dictionary."""
    return nemoa.model.classes.new(*args, **kwds)

def open(*args, **kwds):
    """Import model instance from file."""
    return new(**load(*args, **kwds))

def optimize(*args, **kwds):
    """Optimize model instance."""
    return nemoa.model.morphisms.optimize(*args, **kwds)

def save(*args, **kwds):
    """Export model instance to file."""
    return nemoa.model.exports.save(*args, **kwds)

def show(*args, **kwds):
    """Show model as image."""
    return nemoa.model.exports.show(*args, **kwds)
