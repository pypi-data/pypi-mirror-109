
#####################################################################
#
# ESPREM Client Misc
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
import hashlib

from . import s_log  

cache_dirpath = "/tmp/pyespremclient_cache/"

#####################################################################

def get_filepath( data ) :
    cache_dirpath + get_hash( data_str ) + ".json"
    return hashlib.sha256( msg.encode('utf-8') ).hexdigest( )

#####################################################################

def available( request_list ) :

    return False

    request_str = request_list[ 0 ] + json.dumps( request_list[ 1 ] )
    cache_hash = hashlib.sha256( request_str.encode('utf-8') ).hexdigest( )
    cache_filepath = cache_dirpath + cache_hash + ".json"

    return os.path.isfile( cache_filepath ) 

def update( request_list , response ) :
    request_str = request_list[ 0 ] + json.dumps( request_list[ 1 ] )
    cache_hash = hashlib.sha256( request_str.encode('utf-8') ).hexdigest( )
    cache_filepath = cache_dirpath + cache_hash + ".json"
    with open( cache_filepath , "w" ) as f :
        f.write( json.dumps( response ) )
    s_log.write_msg( "CACHE UPDATED" )

def get_data( request_list ) :
    request_str = request_list[ 0 ] + json.dumps( request_list[ 1 ] )
    cache_hash = hashlib.sha256( request_str.encode('utf-8') ).hexdigest( )
    cache_filepath = cache_dirpath + cache_hash + ".json"
    with open( cache_filepath , "r" ) as f :
        return(json.load(f))


def init_directory( ) :

    if( not os.path.isdir( cache_dirpath ) ) :
        os.makedirs( cache_dirpath )

#####################################################################

init_directory( )
    