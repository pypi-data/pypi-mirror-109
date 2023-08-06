
#####################################################################
#
# ESPREM Client Log
#
# Project   : PYESPREMCLIENT
# Author(s) : Zafar Iqbal < zaf@saparc.gr >
# Copyright : (C) 2021 SPARC PC < https://sparc.space/ >
#
# All rights reserved. No warranty, explicit or implicit, provided.
# SPARC PC is and remains the owner of all titles, rights
# and interests in the Software.
#
#####################################################################

import json

#####################################################################

from . import get_version

#####################################################################
def default_json(t):
    return f'{t}'

def write_msg( msg_raw ) :

    msg = msg_raw
    
    if( isinstance( msg,list ) ) :
        msg = msg.tostring( )
    
    if( isinstance( msg,dict ) ) :
        msg = json.dumps( msg , default=default_json )

    with open( "/tmp/pyespremclient.log" , "a+" , 1 ) as log_file :
        log_file.write( msg + "\n" )

#####################################################################

write_msg( "PYESPREMCLIENT" + get_version( ) )

    