"""
This file contains the blocklist of JWT tokens. It will be imported by the app and the lougout resource so that the
tokens can be added to the blocklist when the user logs out.

"""

BLOCKLIST = set()