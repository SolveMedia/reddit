# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://code.reddit.com/LICENSE. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is reddit.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is reddit Inc.
#
# All portions of the code written by reddit are Copyright (c) 2006-2012 reddit
# Inc. All Rights Reserved.
###############################################################################

import random, string
from pylons import g
import urllib
import urllib2
import sha

from r2.lib.cache import make_key

def valid_solution(challenge, response, remoteip):
    req = urllib2.Request( 'http://api.solvemedia.com/papi/verify',
                           urllib.urlencode( {
                              'privatekey'  : g.solve_privkey,
                              'remoteip'    : remoteip,
                              'challenge'   : challenge,
                              'response'	: response,
                           } ), {
                              'User-Agent'  : 'solvemedia-python-client',
                           } )
    try:
        resp = urllib2.urlopen(req)
    except:
        return False
    line = resp.read().splitlines()
    # validate message authenticator

    if g.solve_hashkey:
        hash = sha.new( line[0] + challenge + g.solve_hashkey ).hexdigest()
        if hash != line[2]:
            return False #'error' : 'hash-fail' 

    if line[0] == 'true':
        return True
    else:
        return False

