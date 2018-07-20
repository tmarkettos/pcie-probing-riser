#!/usr/bin/env python

import time
import sys

def header(lanes):
    print("(module PCIExpress_TH_x%d (layer F.Cu) (tedit %X)" % (lanes, time.time() ))
    print("  (descr \"PCIexpress Bus Through Hole Connector x%d lanes\")" % (lanes))
    print("  (tags \"PCIexpress Bus Through Hole Connector x%d\")" % (lanes))
    print("  (attr virtual)")
    print("  (fp_text reference REF** (at 0 5) (layer F.SilkS)")
    print("    (effects (font (size 1 1) (thickness 0.15)))")
    print("  )")
    print("  (fp_text value PCIExpress_TH_x%d (at 0 5) (layer F.Fab)" %(lanes))
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
    origin_x = 0
    origin_y = 0
    # length of the connector, based on the PCI Express CEM 1.1
    dims_b = {1:25, 4:39, 8:56, 16:89}
    # other dimensions
    b = dims_b[lanes]
    a = b - 17.35
    c = b - 15.85
    width = 7.50
    # lip on A side of connector
    lip = 1.35
    
    # top and bottom edges
    y_a = -width/2;
    y_b = -y_a;
    
    x_low = origin_x - 14.5
    x_high = origin_x + b - 14.5

    end = 12.15 + b; # 20.3 for x1
    silk_delta = -0.6 # 19.7 for x1
    crtyd_delta = -0.35 # 19.95 for x1
    for i in range(0,4):
        x = x_low if (i==0 or i==1) else x_high
        y = y_a if (i==0 or i==3) else y_b
        j = i + 1
        x_next = x_low if (j==0 or j==1 or j==4) else x_high
        y_next = y_a if (j==0 or j==3 or j==4) else y_b
        y_crt = y if (i==0 or i==3) else y_b+lip
        y_crt_next = y_next if (j==0 or j==3 or j==4) else y_b+lip
        print("  (fp_line (start %g %g)  (end %g %g)  (layer F.SilkS)  (width 0.12))" % (x, y, x_next, y_next))
        print("  (fp_line (start %g %g)  (end %g %g)  (layer F.CrtYd)  (width 0.12))" % (x, y_crt, x_next, y_crt_next))
    return
    

def mounting_hole(x, y):
#    print("  (pad ~ thru_hole %s (at %g %g) (drill 2.35) (layers *.Cu *.Mask))" % (side, pin, shape, x, y))
    print("  (pad \"\" np_thru_hole circle (at %g %g) (size 2.35 2.35) (drill 2.35) (layers *.Cu *.Mask))" % (x,y))


def draw_pin(side, pin, x, y):
    if side=='A' and pin==1:
        shape='rect'
    else:
        shape='circle'
    print("  (pad %s%d thru_hole %s (at %g %g) (size 1.5 1.5) (drill 0.7) (layers *.Cu *.Mask))" % (side, pin, shape, x, y))
    return


def draw_row(side, lanes, n):
    origin_x = -1.65 - 10

    # reflection around centre line
    a_origin_y = -1.25
    b_origin_y = -a_origin_y
    origin_y = a_origin_y if side=='A' else b_origin_y
    y_delta = -2 if side=='A' else 2

    for pin in range(1, n+1):
        x = origin_x + (pin-1)
        y = (origin_y + y_delta) if (pin % 2==0) else origin_y
        draw_pin(side, pin, x, y)
        
        # account for origin hole
        if pin==11:
            origin_x = origin_x + 2
    return


def connector(lanes):
    # number of columns in second half, based on number of lanes
    cols = { 1:6, 4:20, 8:37, 16:70 }
    header(lanes)
    outline(lanes)
    mounting_hole(0,0)
    mounting_hole(3.15 + cols[lanes], 0) 
    draw_row('A', lanes, 11+cols[lanes]+1)
    draw_row('B', lanes, 11+cols[lanes]+1)
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
    
