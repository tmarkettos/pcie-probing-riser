#!/usr/bin/env python

import time
import sys

def header(lanes):
    print("(module BUS_PCIexpress_x%d (layer F.Cu) (tedit %X)" % (lanes, time.time() ))
    print("  (descr \"PCIexpress Bus Edge Connector x%d lanes\")" % (lanes))
    print("  (tags \"PCIexpress Bus Edge Connector x%d\")" % (lanes))
    print("  (attr virtual)")
    print("  (fp_text reference REF** (at 5.05 -3.31) (layer F.SilkS)")
    print("    (effects (font (size 1 1) (thickness 0.15)))")
    print("  )")
    print("  (fp_text value BUS_PCIexpress_x%d (at 16.48 -3.31) (layer F.Fab)" %(lanes))
    print("    (effects (font (size 1 1) (thickness 0.15)))")
    print("  )")
    print("  (fp_text user %R (at 9.5 0.662) (layer F.Fab)")
    print("    (effects (font (size 1 1) (thickness 0.15)))")
    print("  )")
    return

def footer(lanes):
    print(")")
    return

def outline(lanes):
    # length of the connector, based on the spec
    dims = {1:8.15, 4:22.15, 8:39.15, 16:72.15}
    b = dims[lanes]
    end = 12.15 + b; # 20.3 for x1
    silk_delta = -0.6 # 19.7 for x1
    crtyd_delta = -0.35 # 19.95 for x1
    print("  (fp_line (start 10.6 -2)  (end 10.6 -5.2)  (layer F.SilkS)  (width 0.12))")
    print("  (fp_line (start 10.6 -5.2)  (end 12.4 -5.2)  (layer F.SilkS)  (width 0.12))")
    print("  (fp_line (start 12.4 -5.2)  (end 12.4 -2)  (layer F.SilkS)  (width 0.12))")
    print("  (fp_line (start -0.7 -2)  (end 10.6 -2)  (layer F.SilkS)  (width 0.12))")
    print("  (fp_line (start 10.6 -2)  (end 10.6 3.8)  (layer F.SilkS)  (width 0.12))")
    print("  (fp_line (start 10.6 3.8)  (end -0.7 3.8)  (layer F.SilkS)  (width 0.12))")
    print("  (fp_line (start -0.7 3.8)  (end -0.7 -2)  (layer F.SilkS)  (width 0.12))")
    print("  (fp_line (start %g -2)  (end 12.4 -2)  (layer F.SilkS)  (width 0.12))" % (end + silk_delta))
    print("  (fp_line (start 12.4 3.8)  (end %g 3.8)  (layer F.SilkS)  (width 0.12))" % (end + silk_delta))
    print("  (fp_line (start 12.4 -2)  (end 12.4 3.8)  (layer F.SilkS)  (width 0.12))")
    print("  (fp_line (start %g -2)  (end %g 3.8)  (layer F.SilkS)  (width 0.12))" % (end + silk_delta, end + silk_delta))
    print("  (fp_line (start -0.95 -5.45)  (end %g -5.45)  (layer F.CrtYd)  (width 0.05))" % (end + crtyd_delta))
    print("  (fp_line (start -0.95 -5.45)  (end -0.95 4.05)  (layer F.CrtYd)  (width 0.05))")
    print("  (fp_line (start %g 4.05)  (end %g -5.45)  (layer F.CrtYd)  (width 0.05))" % (end + crtyd_delta, end + crtyd_delta))
    print("  (fp_line (start %g 4.05)  (end -0.95 4.05)  (layer F.CrtYd)  (width 0.05))" % (end + crtyd_delta))
    return

def draw_pin(side, pin, x, layer, short):
    height = 4.6
    pad_y = 0.5
    end_y = 2.8
    if short:
        height -= 1
        pad_y -= 0.5
    print("  (pad %s%d connect rect (at %g %g) (size 0.65 %g)  (layers %s.Cu %s.Mask))" % (side, pin, x, pad_y, height, layer, layer))
    if not short:
        print("  (pad %s%d connect circle (at %g %g) (size 0.65 0.65)  (layers %s.Cu %s.Mask))" % (side, pin, x, end_y, layer, layer))
#   print("  (pad \"\" connect oval (at %g 2.8 90) (size 0.65 0.65)  (layers %s.Cu %s.Mask))" % (x, layer, layer))
    

def power_group(lanes):
#    print("  (pad \"\" connect circle (at 19 2.8) (size 0.65 0.65) (layers F.Cu F.Mask))")
    for pin in range(1,11+1):
        x = pin-1
        for side in ["A", "B"]:
            layer = "B" if side=="A" else "F"
            # PRSNT# pins shorter by 1mm
            short = True if (side=="A" and pin==1) else False
            draw_pin(side, pin, x, layer, short)
    return

def data_group(lanes):
    pin_start = 12
    pin_end = pin_start
    if (lanes >= 1):
        pin_end += 7
    if (lanes >= 4):
        pin_end += 14
    if (lanes >= 8):
        pin_end += 17
    if (lanes >= 16):
        pin_end += 33

    for pin in range(pin_start, pin_end):
        x = pin+1
        for side in ["A", "B"]:
            layer = "B" if side=="A" else "F"
            short = True if (side=="B" and (pin==17 or pin==31 or pin==48 or pin==81)) else False
            draw_pin(side, pin, x, layer, short)
        
    return

def connector(lanes):
    header(lanes)
    outline(lanes)
    power_group(lanes)
    data_group(lanes)
    footer(lanes)
    return
    


if len(sys.argv) != 2:
    print("Syntax: %s <lanes>" % sys.argv[0])
    exit(1)
lanes = int(sys.argv[1])
variants=[1, 4, 8, 16]
if (lanes not in variants):
    print("Unrecognised PCIe lane count %d" % (lanes))
    exit(2)

connector(lanes)
    
