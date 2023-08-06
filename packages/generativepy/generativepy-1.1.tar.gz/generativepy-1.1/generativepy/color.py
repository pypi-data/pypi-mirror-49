# Author:  Martin McBride
# Created: 2019-06-04
# Copyright (C) 2018, Martin McBride
# License: MIT

import colorsys

# Color modes
RGB = 1
HSL = 2

cssColors = {
"purple":(128,0,128),
"fuchsia":(255,0,255),
"lime":(0,255,0),
"teal":(0,128,128),
"aqua":(0,255,255),
"blue":(0,0,255),
"navy":(0,0,128),
"black":(0,0,0),
"gray":(128,128,128),
"silver":(192,192,192),
"white":(255,255,255),
"indianred":(205,92,92),
"lightcoral":(240,128,128),
"salmon":(250,128,114),
"darksalmon":(233,150,122),
"lightsalmon":(255,160,122),
"crimson":(220,20,60),
"red":(255,0,0),
"firebrick":(178,34,34),
"darkred":(139,0,0),
"pink":(255,192,203),
"lightpink":(255,182,193),
"hotpink":(255,105,180),
"deeppink":(255,20,147),
"mediumvioletred":(199,21,133),
"palevioletred":(219,112,147),
"coral":(255,127,80),
"tomato":(255,99,71),
"orangered":(255,69,0),
"darkorange":(255,140,0),
"orange":(255,165,0),
"gold":(255,215,0),
"yellow":(255,255,0),
"lightyellow":(255,255,224),
"lemonchiffon":(255,250,205),
"lightgoldenrodyellow":(250,250,210),
"papayawhip":(255,239,213),
"moccasin":(255,228,181),
"peachpuff":(255,218,185),
"palegoldenrod":(238,232,170),
"khaki":(240,230,140),
"darkkhaki":(189,183,107),
"lavender":(230,230,250),
"thistle":(216,191,216),
"plum":(221,160,221),
"violet":(238,130,238),
"orchid":(218,112,214),
"fuchsia":(255,0,255),
"magenta":(255,0,255),
"mediumorchid":(186,85,211),
"mediumpurple":(147,112,219),
"blueviolet":(138,43,226),
"darkviolet":(148,0,211),
"darkorchid":(153,50,204),
"darkmagenta":(139,0,139),
"purple":(128,0,128),
"rebeccapurple":(102,51,153),
"indigo":(75,0,130),
"mediumslateblue":(123,104,238),
"slateblue":(106,90,205),
"darkslateblue":(72,61,139),
"greenyellow":(173,255,47),
"chartreuse":(127,255,0),
"lawngreen":(124,252,0),
"lime":(0,255,0),
"limegreen":(50,205,50),
"palegreen":(152,251,152),
"lightgreen":(144,238,144),
"mediumspringgreen":(0,250,154),
"springgreen":(0,255,127),
"mediumseagreen":(60,179,113),
"seagreen":(46,139,87),
"forestgreen":(34,139,34),
"green":(0,128,0),
"darkgreen":(0,100,0),
"yellowgreen":(154,205,50),
"olivedrab":(107,142,35),
"olive":(128,128,0),
"darkolivegreen":(85,107,47),
"mediumaquamarine":(102,205,170),
"darkseagreen":(143,188,143),
"lightseagreen":(32,178,170),
"darkcyan":(0,139,139),
"teal":(0,128,128),
"aqua":(0,255,255),
"cyan":(0,255,255),
"lightcyan":(224,255,255),
"paleturquoise":(175,238,238),
"aquamarine":(127,255,212),
"turquoise":(64,224,208),
"mediumturquoise":(72,209,204),
"darkturquoise":(0,206,209),
"cadetblue":(95,158,160),
"steelblue":(70,130,180),
"lightsteelblue":(176,196,222),
"powderblue":(176,224,230),
"lightblue":(173,216,230),
"skyblue":(135,206,235),
"lightskyblue":(135,206,250),
"deepskyblue":(0,191,255),
"dodgerblue":(30,144,255),
"cornflowerblue":(100,149,237),
"royalblue":(65,105,225),
"blue":(0,0,255),
"mediumblue":(0,0,205),
"darkblue":(0,0,139),
"navy":(0,0,128),
"midnightblue":(25,25,112),
"cornsilk":(255,248,220),
"blanchedalmond":(255,235,205),
"bisque":(255,228,196),
"navajowhite":(255,222,173),
"wheat":(245,222,179),
"burlywood":(222,184,135),
"tan":(210,180,140),
"rosybrown":(188,143,143),
"sandybrown":(244,164,96),
"goldenrod":(218,165,32),
"darkgoldenrod":(184,134,11),
"peru":(205,133,63),
"chocolate":(210,105,30),
"saddlebrown":(139,69,19),
"sienna":(160,82,45),
"brown":(165,42,42),
"maroon":(128,0,0),
"white":(255,255,255),
"snow":(255,250,250),
"honeydew":(240,255,240),
"mintcream":(245,255,250),
"azure":(240,255,255),
"aliceblue":(240,248,255),
"ghostwhite":(248,248,255),
"whitesmoke":(245,245,245),
"seashell":(255,245,238),
"beige":(245,245,220),
"oldlace":(253,245,230),
"floralwhite":(255,250,240),
"ivory":(255,255,240),
"antiquewhite":(250,235,215),
"linen":(250,240,230),
"lavenderblush":(255,240,245),
"mistyrose":(255,228,225),
"gainsboro":(220,220,220),
"lightgray":(211,211,211),
"lightgrey":(211,211,211),
"silver":(192,192,192),
"darkgray":(169,169,169),
"darkgrey":(169,169,169),
"gray":(128,128,128),
"grey":(128,128,128),
"dimgray":(105,105,105),
"dimgrey":(105,105,105),
"lightslategray":(119,136,153),
"lightslategrey":(119,136,153),
"slategray":(112,128,144),
"slategrey":(112,128,144),
"darkslategray":(47,79,79),
"darkslategrey":(47,79,79),
"black":(0,0,0),
}

class Color():

    def __init__(self, *args):
        global cssColors
        self.useRange = True
        self.allowHSL = True
        if len(args) == 1:
            if args[0] in cssColors:
                self.color = cssColors[args[0]]
                self.useRange = False
                self.allowHSL = False
            else:
                self.color = (args[0],)*3
            self.alpha = ()
            self.allowHSB = False
        elif len(args) == 2:
            if args[0] in cssColors:
                self.color = cssColors[args[0]]
                self.useRange = False
                self.allowHSL = False
            else:
                self.color = (args[0],) * 3
            self.alpha = (args[1],)
            self.allowHSB = False
        elif len(args) == 3:
            self.color = tuple(args)
            self.alpha = ()
        elif len(args) == 4:
            self.color = tuple(args[:3])
            self.alpha = (args[3],)
        else:
            raise ValueError("Color takes 1, 2, 3 or 4 arguments")

    def getRGB(self, mode=RGB, scale=1):
        if not self.useRange:
            scale = 256
        c = tuple(x / scale for x in self.color)
        a = tuple(x / scale for x in self.alpha)
        if mode == RGB or not self.allowHSL:
            return c + a
        else:
            h, s, l = c
            return colorsys.hls_to_rgb(h, l, s) + a

    def lerp(self, other, ratio):
        ratio = min(1, max(0, ratio)) #Clamp ratio between 0 and 1
        col1 = self.getRGB()
        col2 = other.getRGB()
        col = [x*(1-ratio) + y*ratio for x, y in zip(col1, col2)]
        return Color(*col)

    def __str__(self):
        return str(self.color) + ' ' + str(self.alpha)

class Gradient():
    '''
    Create a colour gradient
    The gradient is defined by a set of stops - each stop has a positon and color
    The gradienr colour at a particular position is found by interpolating between the stop
    below and teh stop above.
    '''

    def __init__(self):
        self.stops = []

    def add(self, position, color):
        '''
        Add a new stop. Stops must be added in order of increasing position value
        :param position: Position of stop
        :param color: colour od stop
        :return: self
        '''
        self.stops.append((position, color))
        return self

    def getColor(self, position):
        '''
        Get colour at a position
        :param position:
        :return:
        '''
        if not self.stops:
            return Color(0)
        if position<=self.stops[0][0]:
            return self.stops[0][1]
        for i in range(len(self.stops)-1):
            if self.stops[i][0] < position <= self.stops[i+1][0]:
                ratio = (position - self.stops[i][0]) / (self.stops[i+1][0] - self.stops[i][0])
                return self.stops[i][1].lerp(self.stops[i+1][1], ratio)
        return self.stops[-1][1]

