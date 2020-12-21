#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Class to interface a double-optical single-mechanical system."""

__name__    = 'qom.systems.DOSMSystem'
__authors__ = ['Sampreet Kalita']
__created__ = '2020-12-04'
__updated__ = '2020-12-21'

# dependencies
import logging

# dev dependencies
from qom.systems.BaseSystem import BaseSystem

# module logger
logger = logging.getLogger(__name__)

class DOSMSystem(BaseSystem):
    """Class to interface a double-optical single-mechanical system.
    
    Inherits :class:`qom.systems.BaseSystem`.
        
    Parameters
    ----------
    params : dict
        Parameters for the system.
    """

    def __init__(self, params):
        """Class constructor for DOSMSystem."""

        # initialize super class
        super().__init__(params)

        # set attributes
        self.code = 'dosms'
        self.name = 'DOSMSystem'