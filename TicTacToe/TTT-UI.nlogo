extensions [py csv]

patches-own [the-move the-turtle maybe-move]

globals [
  temp
  python-file
  python-save-file
  pos-list
  wins
  playing?
  comp-error
  out-filename
]

to startup
  set python-save-file "TTT-UI-python-filename.txt"
end

to setup
  cp
  cd
  ct
  clear-output
  set pos-list [ [-1 1] [0 1] [1 1] [-1 0] [0 0] [1 0] [-1 -1] [0 -1] [1 -1]]
  set wins [[0 1 2] [3 4 5] [6 7 8] [0 3 6] [1 4 7] [2 5 8] [0 4 8] [2 4 6]]
  draw-lines 1.3 6 gray
  draw-lines 1.3 6 gray
  Get-python-filename
  CreatePlayTurtles
  set playing? True
  set comp-error ""
  set out-filename "TTT-UI-result.txt"
  ;reset-ticks
end

to draw-lines [part width mcolor ]
  draw-line (0 - part)  .5  part .5 width mcolor
  draw-line (0 - part) -.5 part -.5 width mcolor
  draw-line -.5 (0 - part) -.5 part width mcolor
  draw-line  .5 (0 - part) .5 part width mcolor
end

to draw-line [x1 y1 x2 y2 width mcolor]
  crt 1 [
    set size .1
    set color mcolor
    setxy x1 y1
    set pen-size width
    pd
    let xm .5 * (x1 + x2)
    let ym .5 * (y1 + y2)
    setxy xm ym
    setxy x2 y2
    die
  ]
end

to set-python-file
  let filename user-file
  if filename != false [
    ; Check that the suffix is ".py"
    let pos position "." reverse filename
    ifelse pos != 2 or (substring filename (length filename - 3) length filename) != ".py"
    [  user-message "The suffix of the filename must be '.py'"]
    [  set python-file filename
       set python-file replace-all python-file "\\" "/"
       if file-exists? python-save-file [file-delete python-save-file]
       file-open python-save-file
       file-print python-file
       file-close
       output-print "Saved the name of file: "
       output-print python-file
    ]
  ]
end

to Get-Python-filename
  ifelse python-file = 0 or file-exists?  python-save-file
  [  file-open python-save-file
     set python-file file-read-line
     file-close
     output-print "Python-filename is:"
     output-print python-file
  ]
  [  user-message "No python program file named.  Use 'Change Python program file' to set it."
  ]
end

to CreatePlayTurtles
  let i 0
  repeat 9 [
    crt 1 [
      set size .6
      let t-pos item i pos-list
      set xcor item 0 t-pos
      set ycor item 1 t-pos
      let this-turtle self
      ask patch xcor ycor [set the-turtle this-turtle]
      ht
    ]
    set i i + 1
  ]
end

to play
  ;if not playing? [stop]
  ; First move for computer?
  if IsFirstMove? and First-Move-Computer [
    ;let comp-move ComputerMove
    ;; For first move by Computer, chose randomly between moves 0, 1 and 4
    let comp-move one-of [0 1 4]
    print "First move"
    print comp-move
    if comp-error != "" [
      user-message comp-error
      stop
    ]
    MakeCompMove comp-move
  ]

  if mouse-inside? and any? patches with [the-move = 0] [

    ; whose move next?
    let this-move-will-be NextMove

    ; set maybe move
    let px round mouse-xcor
    let py round mouse-ycor
    if ([the-move] of patch px py) = 0 [
      Set-Maybe-Move px py this-move-will-be
      if mouse-down? [
        Set-Actual-Move px py this-move-will-be
        if CheckEnd [stop]
        let comp-move ComputerMove
        if comp-error != ""
        [  user-message comp-error
           stop
        ]
        MakeCompMove comp-move
        if CheckEnd [stop]
      ]
    ]
  ]
end

to-report IsFirstMove?
  let moves [the-move] of patches
  foreach moves [x -> if x != 0 [report False]]
  report True
end

to-report NextMove
  let xs count patches with [the-move = "x"]
  let os count patches with [the-move = "o"]
  let this-move-will-be "x"
  if xs != os [set this-move-will-be "o"]
  report this-move-will-be
end

to Set-Maybe-Move [px py this-move]
  ask patch px py [
    if maybe-move != this-move [
      ask patches with [maybe-move != 0 and the-move = 0] [
        set maybe-move 0
        ask the-turtle [ht]
      ]
      set maybe-move this-move
      ask the-turtle [
        ifelse this-move = "x"
        [ set shape "X" ]
        [ set shape "circle 2" ]
        set color green - 2
        st
      ]
    ]
  ]
end

to Set-Actual-Move [px py this-move]
  ask patch px py [
    ask the-turtle [
      set color white
      st
    ]
    set the-move this-move
  ]
end

to MakeCompMove [move]
  let px item 0 (item move pos-list)
  let py item 1 (item move pos-list)
  ask patch px py [
    let symbol ""
    ifelse NextMove = "x"
    [  set symbol "X"
       set the-move "x"
    ]
    [  set symbol "circle 2"
       set the-move "o"
    ]
    ask the-turtle [
      set color 0.9
      set shape symbol
      st
      repeat 9 [
        wait 0.05
        set color color + 1
      ]
    ]
  ]
end

to-report CheckEnd
  ; first check for a win
  let iwin 0
  repeat 8 [
    let this-win item iwin wins
    let pxy0 item (item 0 this-win) pos-list
    let pxy1 item (item 1 this-win) pos-list
    let pxy2 item (item 2 this-win) pos-list
    let patch0 patch (item 0 pxy0) (item 1 pxy0)
    let patch1 patch (item 0 pxy1) (item 1 pxy1)
    let patch2 patch (item 0 pxy2) (item 1 pxy2)
    if ([the-move] of patch0 != 0) and ([the-move] of patch0 = [the-move] of patch1) and ([the-move] of patch1 = [the-move] of patch2) [
      ask patch0 [ask the-turtle [set color red]]
      ask patch1 [ask the-turtle [set color red]]
      ask patch2 [ask the-turtle [set color red]]
      report True
    ]
    set iwin iwin + 1
  ]

  ; check for draw
  if member? 0 [the-move] of patches [report False]
  report True
end

to-report ComputerMove-old
  let poss []
  let i 0
  repeat 9 [
    let curr item i pos-list
    let px item 0 curr
    let py item 1 curr
    if [the-move] of patch px py = 0 [set poss lput i poss]
    set i i + 1
  ]
  report one-of poss
end

to-report ComputerMove
  ; build the board string
  let board ""
  let i 0
  repeat 9 [
    let pos item i pos-list
    let p patch (item 0 pos) (item 1 pos)
    let move "x"
    if [the-move] of p = "o" [set move "o"]
    if [the-move] of p = 0 [set move "_"]
    set board (word board move)
    set i i + 1
  ]
  ; let command (word "python3 " python-file " " out-filename " " board)
  let command (word Which-Python? " \"" python-file "\" " out-filename " " board)
  set command (word "os.system('" command "')")
  print command

  ; run the Python program
  py:setup py:python3
  py:run "import os"
  py:run command

  ; no file?
  if not file-exists? out-filename [
    set comp-error (word out-filename " is empty")
    report False
  ]

  ; read results
  let lines csv:from-file out-filename
  let comp-move item 0 (item 0 lines)
  output-print ""
  output-print "Results:"
  foreach lines [x -> output-print item 0 x]

  ; check for errors
  if not is-number? comp-move or comp-move < 0 or comp-move > 8 [
    set comp-error (word "First line returned not a number or invalid  move: " comp-move)
    report False
  ]

  let pos item comp-move pos-list
  let p patch (item 0 pos) (item 1 pos)
  if [the-move] of p != 0 [
    set comp-error (word "Returned move " comp-move " but is already occupied")
    report False
  ]

  report comp-move
end

to-report replace-all [the-string from-char to-chars]
  while [True] [
    let pos position from-char the-string
    if pos = False [report the-string]
    set the-string replace-item pos the-string to-chars
  ]
end
@#$#@#$#@
GRAPHICS-WINDOW
252
10
560
319
-1
-1
100.0
1
10
1
1
1
0
1
1
1
-1
1
-1
1
0
0
1
ticks
30.0

BUTTON
69
200
158
233
New game
Setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SWITCH
29
239
200
272
First-move-computer
First-move-computer
1
1
-1000

BUTTON
20
87
206
120
Select Python program file
Set-Python-File
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
78
277
141
310
NIL
Play
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

OUTPUT
15
329
683
505
11

CHOOSER
37
124
175
169
Which-Python?
Which-Python?
"python3" "python" "python2"
1

TEXTBOX
21
10
196
59
Tic-Tac-Toe GUI\nfor Python competitor
17
0.0
1

@#$#@#$#@
## WHAT IS IT?
A User-Interface to a TicTacToe competitor Python3 program.

## Version
v.1.2 -- Apr. 22, 2020
v.1.0 -- Dec. 26, 2019

## Startup

1. Press the "Select Python program file" and navigate to and choose your Python competitor program

2. Choose the name of your command-line Python interpeter

## The Python program calling sequence:
You may name the Python program file anything, but for the discussion below, assume it's "TTT.py"

Your Python program will be called by this NetLogo program using the command-line (assuming you chose "python3" in the drop-down):

`python3 TTT.py {output-filename} {board-string}`

Your Python program will receive the current board state in the second argument and output its results to the filename in the first argument.

For instance, assume that the first move already made was to the upper-right cell:

  `python3 TTT.py TTT-result.txt __x______`

## Python program output:
Your Python program should, under normal circumstances print 3 lines to the output file:
1. the recommended move -- a number between 0 and 8
2. The English version of that move (e.g. Upper-center, Middle-right, Bottom-left)
3. A prediction (e.g. x wins in 3 moves, draw, o loses in 1 move)

For instance:

    4
    Middle-center
    o wins in 3 moves
 
## CREDITS AND REFERENCES

Peter Brooks
Artificial Intelligence Course
Stuyvesant High School
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.1.1
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@
