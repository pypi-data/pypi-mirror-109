
#####################################################################
#
# ESPREM Client Config
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
import json

#####################################################################

from . import s_log  

#####################################################################

config = { }

#####################################################################

def set_key( config_key , config_val ) :
    global config
    config[ config_key ] = config_val

def get_key( config_key ) :
    return config[config_key]

def init_fromfile( config_path , config_key ) :

    global config

    #s_log.write_msg(os.getcwd()+","+config_path)
    #s_log.write_msg(os.getcwd())

    try :

        with open( config_path ) as f :
            config_all = json.load( f )
    
    except IOError :

        s_log.write_msg( "ERROR IOError " + config_path )
        return False

    ####################################################################

    if config_key in config_all :
        config = config_all[ config_key ]
    else :
        s_log.write_msg( "ERROR config_key " + config_key )
        return False

    ####################################################################

    s_log.write_msg( "LOADED " + config_path )

    s_log.write_msg( config )

    if( not "url_endpoint" in config ) :
        s_log.write_msg( "ERROR url_endpoint not found in config" )
        return False

    s_log.write_msg( config[ "url_endpoint" ] )

    return True


if( "NOM_SERVER_CONFIGURATION" in os.environ ) :
    s_log.write_msg("found NOM_SERVER_CONFIGURATION")
    init_fromfile( os.environ[ "NOM_SERVER_CONFIGURATION" ] , "sparc_esprem" )
    