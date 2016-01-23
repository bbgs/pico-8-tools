#!/usr/bin/env python 

import base64
import sys
import os
import zlib

# Empty pico-8 cart created using pico-8 Alpha 0.1.4d.
# Launch application, save, gzip, base64.
empty_p8 = 'H4sICKMxo1YAA2VtcHR5LnA4AO3dTUrDYBiF0XlWkQ3YWI0gbiaU2NaAtaU/1uVbC84dvHAVzzP6IJPDJcPwZTeN25vHdlzsj/vpeb1su659OR53T113Pp9nu+vj2bjdNO/L/WHavrUPzTC8nhbD0FwO69XH5XAbDgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIA/4uodg9QvuIUhngGHYLHbeBG+CAdKAdAZIA9IZIA1IZ4A0IJ0B0oB0BkgD0hkgDUhngDQgnQHSgHQGSAPSGSANSGeANCCdAdKAdAZIA9IZIA1I1wzD4fvPFfM05ic1f8QJWh5odaDVgVYHWh1odaDVgVYHWh1odaDVgVYHWh1odaDVgVYHWh1odaDVgVYHWh1odaDVgVYHWh1odaDVgVYHWh1odaDVfd03dTpM4/VL0raf93f9fd87O/+7c/MJtmPQnEqQAAA='

pico8_cart_dir = os.path.expanduser('~/Library/Application Support/pico-8/carts/')

def add_lua_to_cart(lua_name, cart_name):
    
    # Check dependencies.
    if not os.path.isdir(pico8_cart_dir):
        print 'PICO-8 user directory (%s) not found' % (pico8_cart_dir)
        return False
        
    # Read lua
    try:
        with open('%s' % (lua_name), 'r') as f:
            lua = f.read()
    except IOError:
        print 'Unable to find lua script %s' % (lua_name)
        return False

    # Read original cart (or create a new empty cart if not found).
    try:
        with open('%s/%s' % (pico8_cart_dir, cart_name), 'r') as f:
            print 'Updating %s' % (cart_name)
            cart = f.read()
    except IOError:
        print 'Creating %s' % (cart_name)
        cart = zlib.decompress(base64.b64decode(empty_p8), 16+zlib.MAX_WBITS)

    split = cart.split('__gfx__')
    if len(split) != 2:
        print '%s invalid cart' % (cart_name)
        return False

    # Create backup just in case
    with open('%s/%s.backup' % (pico8_cart_dir, cart_name), 'w') as f:
        f.write(cart)
    
    with open('%s/%s' % (pico8_cart_dir, cart_name), 'w') as f:
        f.write('pico-8 cartridge // http://www.pico-8.com\n')
        f.write('version 5\n')
        f.write('__lua__\n')
        f.write(lua)            
        f.write('__gfx__')
        f.write(split[1])

    return True

if __name__ == '__main__':
    add_lua_to_cart(sys.argv[1], sys.argv[2])
