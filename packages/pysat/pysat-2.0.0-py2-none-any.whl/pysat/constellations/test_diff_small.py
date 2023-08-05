import pysat

"""
Creates a constellationfor testing difference with two small test instruments
"""

inst1 = pysat.Instrument('pysat', 'testsmall', clean_level='clean', tag='6000')
inst2 = pysat.Instrument('pysat', 'testsmall', clean_level='clean', tag='6000')
instruments = [inst1, inst2]
