#!/usr/bin/env python

#
#  Pysnakes 1 or 2 player snake game
#  Copyright (C) 2009-2016  Nathan Dumont
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  Contact nathan@nathandumont.com
#  Visit http://www.nathandumont.com/blog/pysnakes
#

import pygame, sys, os, random, copy

class Snake:
  def __init__(self,x,y,dir = "right",lives = 3, colour = (255,255,0)):
    self.start = (x,y)
    self.start_dir = dir
    self.points = [(x,y)]
    self.dir = [dir]
    self.inputs = 0
    self.moved = True
    self.score = 0
    self.togrow = 2
    self.colour = colour
    self.lives = lives
    self.status = "alive"
    self.life_time = 0
    self.last_update = pygame.time.get_ticks()

  def move_up(self):
    if self.moved and (not self.dir[-1] == "down") and (len(self.dir) < 3):
      if self.inputs > 0:
        self.dir.append("up")
      else:
        self.dir = ["up"]
      self.inputs += 1
      self.moved = False

  def move_down(self):
    if self.moved and (not self.dir[-1] == "up") and (len(self.dir) < 3):
      if self.inputs > 0:
        self.dir.append("down")
      else:
        self.dir = ["down"]
      self.inputs += 1
      self.moved = False

  def move_left(self):
    if self.moved and (not self.dir[-1] == "right") and (len(self.dir) < 3):
      if self.inputs > 0:
        self.dir.append("left")
      else:
        self.dir = ["left"]
      self.inputs += 1
      self.moved = False

  def move_right(self):
    if self.moved and (not self.dir[-1] == "left") and (len(self.dir) < 3):
      if self.inputs > 0:
        self.dir.append("right")
      else:
        self.dir = ["right"]
      self.inputs += 1
      self.moved = False

  def move(self):
    if not self.status == "dead": 
      di = self.dir[0]
      if self.inputs > 0:
        self.inputs -= 1
        if len(self.dir) > 1:
          self.dir = self.dir[1:]
      if di == "up":
        head = [(self.points[0][0],self.points[0][1]-1)]
        if head[0][1] < 0:
          head = [(head[0][0],29+head[0][1])]
      elif di == "down":
        head = [(self.points[0][0],self.points[0][1]+1)]
        if head[0][1] > 28:
          head = [(head[0][0],head[0][1]-29)]
      elif di == "left":
        head = [(self.points[0][0]-1,self.points[0][1])]
        if head[0][0] < 0:
          head = [(40+head[0][0],head[0][1])]
      elif di == "right":
        head = [(self.points[0][0]+1,self.points[0][1])]
        if head[0][0] > 39:
          head = [(head[0][0]-40,head[0][1])]
      if self.togrow > 0:
        self.points = head + self.points
        self.togrow -= 1
      else:
        self.points = head + self.points[:-1]
      self.moved = True

  def got_target(self,x,y):
    if self.points[0] == (x,y):
      return True
    return False

  def grow(self,n):
    self.togrow += n

  def reset(self):
    self.points = [self.start]
    self.togrow = 2
    self.dir = [self.start_dir]
    self.inputs = 0

  def snake_collision(self,os):
    if not self.status == "dead":
      for p in os.points:
        if p == self.points[0]:
          return True
    return False

  def self_collision(self):
    for p in self.points[1:]:
      if p == self.points[0]:
        return True
    return False

  def wall_collision(self,lvlmap):
    if lvlmap[self.points[0][1]][self.points[0][0]] == "1":
      return True
    return False

  def draw(self):
    global screen
    if not self.status == "dead":
      for p in self.points:
        pygame.draw.rect(screen,self.colour,pygame.Rect(p[0]*16,p[1]*16,16,16))

  def die(self):
    global live_snakes
    self.lives -= 1
    self.score -= 5
    if self.lives == 0:
      self.status = "dead"
      live_snakes -= 1
      self.update_lifetime()
    else:
      self.reset()

  def pause(self):
    self.update_lifetime()

  def unpause(self):
    self.last_update = pygame.time.get_ticks()

  def update_lifetime(self):
    self.life_time += pygame.time.get_ticks() - self.last_update
    self.last_update = pygame.time.get_ticks()

class Level:
  def __init__(self,filename,level):
    level_file = file(filename,"r")
    d = level_file.read()
    level_file.close()

    d = d.split("\n")
    self.levels = []
    lvl = []
    for l in d:
      if len(l) >= 40:
        lvl.append(l)
        if len(lvl) == 29:
          self.levels.append(lvl)
          lvl = []
    self.texture = pygame.image.load("textures/wall.png")
    self.change_level(level)

  def current_map(self):
    return self.levels[self.level]

  def current_image(self):
    return self.image

  def change_level(self,level):
    self.level = level
    self.image = pygame.Surface((640,464))
    for i in range(len(self.levels[self.level])):
      for j in range(len(self.levels[self.level][0])):
        if self.levels[self.level][i][j] == "1":
          self.image.blit(self.texture,(j*16,i*16))

  def num_levels(self):
    return len(self.levels)

def init():
  global screen
  global frames
  global start_ticks

  pygame.init()
  screen = pygame.display.set_mode((640,480),pygame.DOUBLEBUF)
  pygame.display.set_caption("pysnakes")
  frames = 0
  start_ticks = pygame.time.get_ticks()
  load_controls()
  pygame.mouse.set_visible(False)

def load_controls():
  global controls

  # set all controls and variables to defaults
  controls = {}
  controls["player"] = []
  controls["player"].append({"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN})
  controls["player"].append({"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s})
  controls["global"] = {}
  controls["global"]["levelset"] = "default"
  controls["global"]["movetime"] = 125

  # then try and load customised values from disk.  These overwrite defaults where set.
  if os.path.exists(os.path.expanduser("~/.pysnakes/controls")):
    fr = file(os.path.expanduser("~/.pysnakes/controls"),"r")
    d = fr.read()
    fr.close()
    controls = {"player": [], "global": {}}
    pno = None
    for l in d.split("\n"):
      if len(l)>0:
        if l[:6] == "player":
          pno = int(l.split()[1])
          controls["player"].append({})
        elif l == "global":
          pno = None
        else:
          if not pno==None:
            var = l.split()
            if var[2] == "int":
              var[1] = int(var[1])
            controls["player"][pno][var[0]] = var[1]
          else:
            var = l.split()
            if var[2] == "int":
              var[1] = int(var[1])
            controls["global"][var[0]] = var[1]

def save_controls():
  global controls

  fw = file(os.path.expanduser("~/.pysnakes/controls"),"w")
  for p in controls["player"]:
    fw.write("player %d\n" % controls["player"].index(p))
    for (k,v) in p.items():
      if type(v) == int:
        t = "int"
      else:
        t = "str"
      fw.write(str(k) + " " + str(v) + " " + t +"\n")
  fw.write("global\n")
  for (k,v) in controls["global"].items():
    if type(v) == int:
      t = "int"
    else:
      t = "str"
    fw.write(str(k) + " " + str(v) + " " + t + "\n")
  fw.close()

def menu_loop(junk):
  global screen
  global frames

  logo = pygame.image.load("textures/logo.png")
  screen.fill((0,0,0))
  menu_height = 200
  screen.blit(logo,(20,10))

  # prepare menu option bitmaps here to save doing it every loop

  font = pygame.font.Font(pygame.font.get_default_font(),20)

  options = []
  options.append({"caption": "Single Player", "id": 0, "top": 0, "left": 0, "width": 0, "height": 0})
  options.append({"caption": "Two Player", "id": 1, "top": 0, "left": 0, "width": 0, "height": 0})
  options.append({"caption": "High Scores", "id": 4, "top": 0, "left": 0, "width": 0, "height": 0})
  options.append({"caption": "Controls", "id": 2, "top": 0, "left": 0, "width": 0, "height": 0})
  options.append({"caption": "Exit", "id":  3, "top": 0, "left": 0, "width": 0, "height": 0})

  widest = 0
  highest = 0
  for i in range(len(options)):
    widest = max([font.size(options[i]["caption"])[0], widest])
    highest = max([font.size(options[i]["caption"])[1], highest])

  widest += 20
  highest += 20

  for i in range(len(options)):
    options[i]["norm"] = pygame.Surface((widest,highest))
    options[i]["high"] = pygame.Surface((widest,highest))
    pygame.draw.rect(options[i]["norm"],(0,0,255), pygame.Rect(0,0,widest,highest),1)
    pygame.draw.rect(options[i]["high"],(255,255,0), pygame.Rect(0,0,widest,highest),1)
    options[i]["norm"].blit(font.render(options[i]["caption"],True,(0,0,255),(0,0,0)),((widest-font.size(options[i]["caption"])[0])/2,10))
    options[i]["high"].blit(font.render(options[i]["caption"],True,(255,255,0),(0,0,0)),((widest-font.size(options[i]["caption"])[0])/2,10))

    options[i]["left"] = (640-widest)/2
    options[i]["top"] = menu_height + i*50
    options[i]["height"] = highest
    options[i]["width"] = widest

  opt = 0

  while 1:
    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        exit()
      if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_DOWN:
          opt += 1
          if opt == len(options):
            opt -= 1
        elif e.key == pygame.K_UP:
          opt -= 1
          if opt == -1:
            opt += 1
        elif e.key == pygame.K_RETURN:
          if options[opt]["id"] == 3:
            exit()
          if options[opt]["id"] == 2:
            return [options_loop,""]
          elif options[opt]["id"] == 1:
            return [game_loop,2]
          elif options[opt]["id"] == 0:
            return [game_loop,1]
          elif options[opt]["id"] == 4:
            return [highscore_loop,[[],[]]]

    # render the options in case the highlight has changed.
    for i in range(len(options)):
      if i == opt:
        screen.blit(options[i]["high"],(options[i]["left"],options[i]["top"]))
      else:
        screen.blit(options[i]["norm"],(options[i]["left"],options[i]["top"]))

    frames += 1
    pygame.display.flip()

def game_loop(players):
  global screen
  global controls
  global live_snakes
  global target_no

  # game_init
  start_params = []
  start_params.append([10,15,"right",3,(255,255,0)])
  start_params.append([30,15,"left",3,(255,0,255)])
  snakes = []
  for i in range(players):
    p = start_params[i]
    snakes.append(Snake(p[0],p[1],p[2],p[3],p[4]))
    snakes[i].up_key = controls["player"][i]["up"]
    snakes[i].down_key = controls["player"][i]["down"]
    snakes[i].left_key = controls["player"][i]["left"]
    snakes[i].right_key = controls["player"][i]["right"]


  levelset = os.path.join(os.path.expanduser("~/.pysnakes/levelsets"),controls["global"]["levelset"])
  if (controls["global"]["levelset"] == "default") or (not os.path.exists(levelset)):
    levelset = "default"

  lvl = Level(levelset,0)
  level = 0

  last_move = pygame.time.get_ticks()

  live_snakes = players

  target_no = 0
  (tx,ty) = new_target(lvl.current_map(),snakes)
  target_image = pygame.image.load("textures/target.png")

  font = pygame.font.Font(pygame.font.get_default_font(),14)

  player1status = font.render("Player 1; lives: %02i; points: %04i" % (snakes[0].lives,snakes[0].score),True,snakes[0].colour,(0,0,0))
  if players > 1:
    player2status = font.render("Player 2; lives: %02i; points: %04i" % (snakes[1].lives,snakes[1].score),True,snakes[1].colour,(0,0,0))
  else:
    player2status = pygame.Surface((300,16))
    player2status.fill((0,0,0))
  
  while 1:
    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        exit()
      if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_PAUSE:
          for s in snakes:
            s.pause()
          last_move += pause()
          for s in snakes:
            s.unpause()
        for s in snakes:
          if e.key == s.up_key:
            s.move_up()
          elif e.key == s.down_key:
            s.move_down()
          elif e.key == s.left_key:
            s.move_left()
          elif e.key == s.right_key:
            s.move_right()

    if pygame.time.get_ticks()-last_move > controls["global"]["movetime"]:
      for s in snakes:
        s.move()
        if s.wall_collision(lvl.current_map()) or s.self_collision():
          s.die()
        if s.got_target(tx,ty):
          s.score += target_no
          s.grow(target_no)
          if target_no < 10:
            (tx,ty) = new_target(lvl.current_map(),snakes)
          else:
            if lvl.num_levels() > (level+1):
              level += 1
              lvl.change_level(level)
              target_no = 0
              (tx,ty) = new_target(lvl.current_map(),snakes)
              for s in snakes:
                s.reset()
            else:
              if players > 1:
                snakes[0].update_lifetime()
                snakes[1].update_lifetime()
                return [highscore_loop, [[snakes[0].score,snakes[1].score],[snakes[0].life_time,snakes[1].life_time]]]
              else:
                snakes[0].update_lifetime()
                return [highscore_loop,[[snakes[0].score],[snakes[0].life_time]]]
      if len(snakes)>1:
        if snakes[0].snake_collision(snakes[1]):
          snakes[0].die()
        if snakes[1].snake_collision(snakes[0]):
          snakes[1].die()
      
      if live_snakes == 0:
        if len(snakes)>1:
          return [highscore_loop, [[snakes[0].score,snakes[1].score], [snakes[0].life_time, snakes[1].life_time]]]
        else:
          return [highscore_loop,[[snakes[0].score],[snakes[0].life_time]]]

      last_move = pygame.time.get_ticks()
      player1status = font.render("Player 1; lives: %02i; points: %04i" % (snakes[0].lives,snakes[0].score),True,snakes[0].colour,(0,0,0))
      if players > 1:
        player2status = font.render("Player 2; lives: %02i; points: %04i" % (snakes[1].lives,snakes[1].score),True,snakes[1].colour,(0,0,0))
      else:
        player2status = pygame.Surface((300,16))
        player2status.fill((0,0,0))
    screen.fill((0,0,0))
    screen.blit(lvl.current_image(),(0,0))
    for s in snakes:
      s.draw()
    screen.blit(target_image,(tx*16,ty*16))
    screen.blit(player1status,(10,465))
    screen.blit(player2status,(300,465))
    pygame.display.flip()

def highscore_loop(args):
  global screen
  global frames

  [scores, times] = args

  font = pygame.font.Font(pygame.font.get_default_font(),16)

  # Ask player(s) for their name(s)
  if len(scores) > 0:
    screen.fill((0,0,0))
    screen.blit(font.render("Player 1, please enter your name:",True,(255,255,0),(0,0,0)),(40,40))
    screen.blit(font.render("Once done, press ENTER",True,(255,255,0),(0,0,0)),(40,120))

    p1name = "_" * 20
    cursor = 0

    screen.blit(font.render(p1name,True,(255,255,0),(0,0,0)),(40,80))

    pygame.display.flip()

    while 1:
      e  = pygame.event.wait()
      if e.type == pygame.QUIT:
        exit()
      if e.type == pygame.KEYDOWN:
        if len(e.unicode) > 0:
          if (ord(e.unicode) > 31) and (ord(e.unicode) < 127):
            # printable characters just get put into the string
            if cursor < 20:
              p1name = p1name[:cursor] + e.unicode + p1name[cursor+1:]
              cursor += 1
        if e.key == 8:
          if cursor > 0:
            cursor -= 1
            p1name = p1name[:cursor]+"_"+p1name[cursor+1:]
        if e.key == pygame.K_RETURN:
          break
      screen.blit(font.render(p1name + "     ",True,(255,255,0),(0,0,0)),(40,80))
      frames += 1
      pygame.display.flip()
    p1name = p1name[:cursor]

  if len(scores) > 1:
    screen.fill((0,0,0))
    screen.blit(font.render("Player 2, please enter your name:",True,(255,0,255),(0,0,0)),(40,40))
    screen.blit(font.render("Once done, press ENTER",True,(255,0,255),(0,0,0)),(40,120))

    p2name = "_" * 20
    cursor = 0

    screen.blit(font.render(p2name,True,(255,0,255),(0,0,0)),(40,80))

    pygame.display.flip()

    while 1:
      e  = pygame.event.wait()
      if e.type == pygame.QUIT:
        exit()
      if e.type == pygame.KEYDOWN:
        if len(e.unicode) > 0:
          if (ord(e.unicode) > 31) and (ord(e.unicode) < 127):
            # printable characters just get put into the string
            if cursor < 20:
              p2name = p2name[:cursor] + e.unicode + p2name[cursor+1:]
              cursor += 1
        if e.key == 8:
          if cursor > 0:
            cursor -= 1
            p2name = p2name[:cursor]+"_"+p2name[cursor+1:]
        if e.key == pygame.K_RETURN:
          break
      screen.blit(font.render(p2name + "     ",True,(255,0,255),(0,0,0)),(40,80))
      frames += 1
      pygame.display.flip()
    p2name = p2name[:cursor]

  # Load old top-scores
  highscores = []
  if os.path.exists(os.path.expanduser("~/.pysnakes/highscores")):
    fr = file(os.path.expanduser("~/.pysnakes/highscores"),"r")
    d = fr.read()
    fr.close()
    for l in d.split("\n")[:-1]:
      highscores.append([l.split("\t")[1],int(l.split("\t")[0]),int(l.split("\t")[2])])

  # Rank new player score(s)
  if len(scores) > 0:
    highscores.append([p1name,int(scores[0]),int(times[0])])
  if len(scores) > 1:
    highscores.append([p2name,int(scores[1]),int(times[1])])

  # save new top-scores
  if not os.path.exists(os.path.expanduser("~/.pysnakes")):
    os.mkdir(os.path.expanduser("~/.pysnakes"))
  fw = file(os.path.expanduser("~/.pysnakes/highscores"),"w")

  for k in topten(highscores):
    fw.write(str(k[1]) + "\t" + str(k[0]) + "\t" + str(k[2]) + "\n")
  fw.close()
  
  # draw top score list
  screen.fill((0,0,0))

  high_title = pygame.image.load("textures/highscores.png")
  screen.blit(high_title,((640-high_title.get_width())/2,0))

  colour = (0,0,255)
  sortscores = topten(highscores)
  screen.blit(font.render("Score",True,colour,(0,0,0)),(20,50))
  screen.blit(font.render("Player",True,colour,(0,0,0)),(120,50))
  screen.blit(font.render("Time",True,colour,(0,0,0)),(500,50))
  for i in range(len(sortscores)):
    screen.blit(font.render(str(sortscores[i][1]),True,colour,(0,0,0)),(100 - font.size(str(sortscores[i][1]))[0],80 + i*30))
    screen.blit(font.render(str(sortscores[i][0]),True,colour,(0,0,0)),(120,80+i*30))
    hrs = sortscores[i][2]/(1000*3600)
    mins = (sortscores[i][2]-hrs*1000*3600)/(1000*60)
    secs = (sortscores[i][2]-hrs*1000*3600-mins*1000*60)/1000
    screen.blit(font.render("%02i:%02i:%02i" % (hrs,mins,secs),True,colour,(0,0,0)),(500,80+i*30))

  pygame.draw.line(screen,colour,(20,70),(620,70))
  pygame.draw.line(screen,colour,(115,50),(115,365))
  pygame.draw.line(screen,colour,(495,50),(495,365))

  # draw player scores()
  if len(scores) > 0:
    hrs = times[0]/(1000*3600)
    mins = (times[0]-hrs*1000*3600)/(1000*60)
    secs = (times[0]-hrs*1000*3600-mins*1000*60)/1000

    screen.blit(font.render("Player 1: " + p1name,True,(255,255,0),(0,0,0)),(20,380))
    screen.blit(font.render("Score: " + str(scores[0]) + " Time: %02i:%02i:%02i" % (hrs,mins,secs),True,(255,255,0),(0,0,0)),(20,400))
    pygame.draw.rect(screen,(255,255,0),pygame.Rect(15, 375,290,50),1)

  if len(scores) > 1:
    hrs = times[1]/(1000*3600)
    mins = (times[1]-hrs*1000*3600)/(1000*60)
    secs = (times[1]-hrs*1000*3600-mins*1000*60)/1000

    screen.blit(font.render("Player 2: " + p2name,True,(255,0,255),(0,0,0)),(340,380))
    screen.blit(font.render("Score: " + str(scores[1]) + " Time: %02i:%02i:%02i" % (hrs,mins,secs),True,(255,0,255),(0,0,0)),(340,400))
    pygame.draw.rect(screen,(255,0,255),pygame.Rect(335,375,290,50),1)

  # write a message telling user to press a key to return to the menu
  screen.blit(font.render("Press ESC to return to the menu.",True,colour,(0,0,0)),((640-font.size("Press ESC to return to the menu.")[0])/2,450))

  # wait for key presses
  while 1:
    e = pygame.event.wait()
    if e.type==pygame.QUIT:
      exit()
    elif e.type == pygame.KEYDOWN:
      if e.key == pygame.K_ESCAPE:
        return [menu_loop,""]
    frames += 1
    pygame.display.flip()

def options_loop(junk):
  global screen
  global controls
  global frames
  global new_keys
  # Present any (and all) game options that can be customised
  
  # Make a list of variables to make remembering indexes easier:
  LEVELSET = 0
  SPEED = 1
  CONTROLS = 2
  SAVE = 3
  EXIT = 4

  # speed is best picked from a list so:
  speeds = [62,125,250,500]
  game_speed = speeds.index(controls["global"]["movetime"])

  # make a list of level sets in the levels directory
  if not os.path.exists(os.path.expanduser("~/.pysnakes/")):
    os.mkdir(os.path.expanduser("~/.pysnakes/"))
  if not os.path.exists(os.path.expanduser("~/.pysnakes/levelsets/")):
    os.mkdir(os.path.expanduser("~/.pysnakes/levelsets/"))
  sets = os.listdir(os.path.expanduser("~/.pysnakes/levelsets/"))
  sets = ["default"] + sets
  try:
    level_set = sets.index(controls["global"]["levelset"])
  except:
    level_set = 0

  # initialise the key bindings to an unchanged state
 
  new_keys = []

  font = pygame.font.Font(pygame.font.get_default_font(),16)
  font_big = pygame.font.Font(pygame.font.get_default_font(),30)

  settings_logo = pygame.image.load("textures/settings.png")
  screen.fill((0,0,0))

  mode = LEVELSET

  menu_text = {}
  menu_text[LEVELSET] = "Level set: " + sets[level_set]
  menu_text[SPEED] = "Game speed: " + str(speeds[game_speed])
  menu_text[CONTROLS] = "Customise controls"
  menu_text[SAVE] = "Save and Exit"
  menu_text[EXIT] = "Exit without saving"

  instruction_text = {}
  instruction_text[LEVELSET] = ["Press Enter to select the levelset you wish to use.", "Default is the set that came with PySnakes,", "others can be placed in .pysnakes/levelsets/ in your home folder."]
  instruction_text[SPEED] = ["Press Enter to set game speeds"]
  instruction_text[CONTROLS] = ["Press Enter to go into the controls config wizard."]
  instruction_text[SAVE] = ["Press Enter to save these settings to disk, and return to main menu"]
  instruction_text[EXIT] = ["Press Enter to return to the main menu without changing any settings."]

  inner = False

  while True:
    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        exit()
      elif e.type == pygame.KEYDOWN:
        if e.key == pygame.K_ESCAPE:
          return [menu_loop,""]
        
        if mode == LEVELSET:
          if inner == False:
            if e.key == pygame.K_RETURN:
              inner = True
            elif e.key == pygame.K_DOWN:
              mode = SPEED
          else:
            if e.key == pygame.K_DOWN:
              level_set += 1
              if level_set > len(sets)-1:
                level_set = len(sets)-1
            elif e.key == pygame.K_UP:
              level_set -= 1
              if level_set < 0:
                level_set = 0
            elif e.key == pygame.K_RETURN:
              menu_text[LEVELSET] = "Level set: " + sets[level_set]
              inner = False

        elif mode == SPEED:
          if inner == False:
            if e.key == pygame.K_RETURN:
              inner = True
            elif e.key == pygame.K_DOWN:
              mode = CONTROLS
            elif e.key == pygame.K_UP:
              mode = LEVELSET
          else:
            if e.key == pygame.K_UP:
              game_speed += 1
              if game_speed > 3:
                game_speed = 3
            elif e.key == pygame.K_DOWN:
              game_speed -= 1
              if game_speed < 0:
                game_speed = 0
            elif e.key == pygame.K_RETURN:
              menu_text[SPEED] = "Game speed: " + str(speeds[game_speed])
              inner = False

        elif mode == CONTROLS:
          if e.key == pygame.K_RETURN:
            return [controls_loop,""]
          elif e.key == pygame.K_UP:
            mode = SPEED
          elif e.key == pygame.K_DOWN:
            mode = SAVE

        elif mode == SAVE:
          if e.key == pygame.K_RETURN:
            if len(new_keys) > 0:
              controls["player"] = copy.copy(new_keys)
            controls["global"]["movetime"] = speeds[game_speed]
            controls["global"]["levelset"] = sets[level_set]
            save_controls()
            return [menu_loop,""]
          elif e.key == pygame.K_UP:
            mode = CONTROLS
          elif e.key == pygame.K_DOWN:
            mode = EXIT

        elif mode == EXIT:
          if e.key == pygame.K_RETURN:
            return [menu_loop,""]
          elif e.key == pygame.K_UP:
            mode = SAVE

      screen.fill((0,0,0))
      screen.blit(settings_logo,((640-settings_logo.get_width())/2,5))

      if mode == LEVELSET and inner == True:
        sets_pic = []
        sets_height = []
        sets_width = []
        for l in sets:
         if l == sets[level_set]:
           colour = (255,255,0)
         else:
           colour = (0,0,255)
         sets_pic.append(font.render(l,True,colour,(0,0,0)))
         sets_height.append(sets_pic[-1].get_height())
         sets_width.append(sets_pic[-1].get_width())
        menu_surf = pygame.Surface((max(sets_width)+10, sum(sets_height)+5+5*len(sets)))
        for i in range(len(sets_pic)):
         menu_surf.blit(sets_pic[i],(5,5+sum(sets_height[:i])+5*i))
        pygame.draw.rect(menu_surf,(255,255,0),pygame.Rect(0,0,menu_surf.get_width(),menu_surf.get_height()),1)
        
        instructions = ["Select level set using up/down and press enter."]

      elif mode == SPEED and inner == True:
        speed_pic = []
        speed_height = []
        speed_width = []
        spd2 = copy.copy(speeds)
        spd2.reverse()
        spd2[0] = str(spd2[0]) + "(Slowest)"
        spd2[-1] = str(spd2[-1]) + "(Fastest)"
        for l in range(len(spd2)):
          if l == len(speeds)-game_speed-1:
            colour = (255,255,0)
          else:
            colour = (0,0,255)
          speed_pic.append(font.render(str(spd2[l]),True,colour,(0,0,0)))
          speed_height.append(speed_pic[-1].get_height())
          speed_width.append(speed_pic[-1].get_width())
        menu_surf = pygame.Surface((max(speed_width)+10, sum(speed_height)+5+5*len(speeds)))
        for i in range(len(speed_pic)):
          menu_surf.blit(speed_pic[i],(5,5+sum(speed_height[:i])+5*i))
        pygame.draw.rect(menu_surf,(255,255,0),pygame.Rect(0,0,menu_surf.get_width(),menu_surf.get_height()),1)

        instructions = ["Press up/down to select speed, enter to confirm"]

      for i in range(len(menu_text)):
        if i==mode:
          colour = (255,255,0)
        else:
          colour = (0,0,255)
        
        menu_img = font_big.render(menu_text[i],True,colour,(0,0,0))
        screen.blit(menu_img,((640-menu_img.get_width())/2,80+50*i))

      lines = 0
      if inner == False:
        instructions = instruction_text[mode]
      for l in instructions:
        limg = font.render(l,True,(255,255,0),(0,0,0))
        screen.blit(limg,(40,400+20*lines))
        lines += 1

      pygame.draw.rect(screen,(255,255,0),pygame.Rect(35,395,570,70),1)

      if inner == True:
        screen.blit(menu_surf,(320,80+50*mode))

      pygame.display.flip()
      frames += 1

def controls_loop(junk):
  global new_keys
  global screen
  global frames

  font = pygame.font.Font(pygame.font.get_default_font(),30)

  new_keys = []
  new_keys.append({"left": None, "right": None, "up": None, "down": None})
  new_keys.append({"left": None, "right": None, "up": None, "down": None})

  key_error = False

  for i in range(len(new_keys)):
    for k in new_keys[i].keys():
      message = "Press new key for Player %i %s key" % (i+1,k)
      while 1:
        screen.fill((0,0,0))
        # render message
        screen.blit(font.render(message,True,(255,255,0),(0,0,0)),((640-font.size(message)[0])/2,200))
        # wait for key press
        new_key = None
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
          exit()
        elif e.type == pygame.KEYDOWN:
          key_error = False
          new_key = e.key
        # check if key is already used
        if not new_key == None:
          # print error message
          for j in new_keys:
            if new_key in j.values():
              key_error = True
              new_key = None
        if not new_key == None:
          new_keys[i][k] = new_key
          break
        if key_error:
          screen.blit(font.render("That key is already used,",True,(255,0,0),(0,0,0)), ((640-font.size("That key is already used,")[0])/2,300))
          screen.blit(font.render("please try another.",True,(255,0,0),(0,0,0)), ((640-font.size("please try another.")[0])/2,340))
        pygame.display.flip()
        frames += 1
  return [options_loop,""]

def pause():
  global screen
  start_pause = pygame.time.get_ticks()
  while True:
    e = pygame.event.wait()
    if e.type == pygame.QUIT:
      exit()
    elif e.type == pygame.KEYDOWN:
      if e.key == pygame.K_PAUSE:
        return pygame.time.get_ticks()-start_pause
    pygame.display.flip()

def new_target(lvl,snakes):
  global target_no
  collides = True
  while collides:
    collides = False
    tx = random.randrange(0,40)
    ty = random.randrange(0,29)
    if (lvl[ty][tx] == "1"):
      collides = True
    for s in snakes:
      if (tx,ty) in s.points:
        collides = True
  target_no += 1
  return (tx,ty)

def topten(scores):
  if len(scores) > 10:
    maxlen = 10
  else:
    maxlen = len(scores)
  changed = True
  while changed:
    changed = False
    for i in range(1,len(scores)):
      if scores[i][1] > scores[i-1][1]:
        temp = scores[i]
        scores[i] = scores[i-1]
        scores[i-1] = temp
        changed = True
      elif (scores[i][2] < scores[i-1][2]) and (scores[i][1] == scores[i-1][1]):
        temp = scores[i]
        scores[i] = scores[i-1]
        scores[i-1] = temp
        changed = True
        
  return scores[:maxlen]

def exit():
  global start_ticks
  global frames

  # uncomment the following line to show an fps count.
  # this doesn't always give sensible results some menus are only refresh on event
  # and if the game is paused this time is not counted.
  #print (frames * 1000)/(pygame.time.get_ticks()-start_ticks), "fps"
  pygame.display.quit()
  sys.exit(0)

if __name__=="__main__":
  init()
  ret = [menu_loop,""]
  while 1:
    ret = ret[0](ret[1])
