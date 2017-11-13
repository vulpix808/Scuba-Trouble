[level]
tileset = tileset.gif
map =   .................
        .ooo.ooo.oooo.oo.
        .oFo?ooo.oooo?oo.
        .ooo?ooooooPo?oo.
        .ooo.oooooooo....
        ......?.......oo.
        .ooo.ooo.oo.oooo.
        .oPo?oooooo?o.oo.
        .ooo.oooooo?o....
        .oo..oooooo?o.oo.
        .ooo.ooo.oo.oooo.
        ...o.ooo.oo.ooPo.
        .ooooooo.oo..ooo.
        .ooooo.ooooo.....
        .oSoo..ooPoo?ooo.
        .ooooooooooo?ooo.
        .................

[.]
name = wall
wall = true
tile = 0, 1
block = true

[o]
name = floor
tile = 0, 0
block = false

[?]
name = secret
tile = 0, 1
wall = true

[P]
name = puzzle
tile = 0, 1
puzzle = true

[F]
name = finish
tile = 0, 1
