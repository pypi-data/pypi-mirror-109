
#####################################################################
#
# ESPREM Client 
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

import os
import re
import io
import json
#from pathlib import Path


#####################################################################

from . import s_log , s_config , s_net

####################################################################

def config_set_key( config_key , config_val ) :
    s_config.set_key( config_key , config_val )

def config_init_fromfile( config_path , config_key ) :
    return s_config.init_fromfile( config_path , config_key )

####################################################################

def do_request( request_endpoint , request_params , request_id = 0 , request_timeout = 60 ) :

    response = s_net.get_response( request_endpoint , request_params , request_id , request_timeout = 60 ) 

    if( "code" in response ) :
        res_str = json.dumps( response , indent = 4 )
        s_log.write_msg( res_str )
        assert False , "code"

    if( "_error" in response ) :
        res_str = json.dumps( response , indent = 4 )
        s_log.write_msg( res_str )
        assert False , "_error"

    return( response )

def log_msg( msg ) :
    s_log.write_msg( msg )
