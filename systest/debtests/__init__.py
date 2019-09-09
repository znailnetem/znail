import sys

# What follows is a bit of a hack:
#
# There is a name collision in K2 and Znail, where both provide a package named "znail".
# "znail" is a very reasonable name for the package in both cases.
#
# As the system tests require importing the "znail" package to access the examples data,
# it is important that the correct "znail" package is loaded. By default, the K2 version
# will exist in the module cache, which is no good. Force unload it here to enable the
# system tests to import the local "znail" package instead.
del sys.modules['znail']
