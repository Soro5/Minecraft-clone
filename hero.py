class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.mode = True
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()
    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)

    def cameraUp(self):
        pos = self.hero.get_pos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def accept_events(self):
        base.accept('c', self.changeView)
        base.accept('j', self.turn_left)
        base.accept('j'+'-repeat', self.turn_left)
        base.accept('l', self.turn_right)
        base.accept('l'+'-repeat', self.turn_right)
        base.accept('a', self.left)
        base.accept('a'+'-repeat', self.left)
        base.accept('d', self.right)
        base.accept('d'+'-repeat', self.right)
        base.accept('w', self.forward)
        base.accept('w'+'-repeat', self.forward)
        base.accept('s', self.back)
        base.accept('s'+'-repeat', self.back)
        base.accept('', self.cha)


    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
            return 0, -1
        elif angle >= 0 and angle <= 335:
            return 0, -1
        elif angle <= 335 and angle >= 290:
            return -1, -1
        elif angle <= 290 and angle >= 245:
            return -1, 0
        elif angle <= 245 and angle >= 200:
            return -1, 1
        elif angle <= 200 and angle >= 155:
            return 0, 1
        elif angle <= 155 and angle >= 110:
            return 1, 1
        elif angle <= 110 and angle >= 65:
            return 1, 0
        elif angle <= 65 and angle >= 20:
            return 1, -1

    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)
    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    def lookAt(self, angle):
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from

    def just_move(self, angle):
        pos = self.lookAt(angle)
        self.hero.setPos(pos)

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)

    def forward(self):
        angle = self.hero.getH() % 360
        self.move_to(angle)
    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)
    def left(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)
    def right(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)
    def try_move(self, angle):
        pos = self.lookAt(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)
    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.lookAt(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)
    def build(self):
        angle = self.hero.getH() % 360
        pos = self.lookAt(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

