import phylib;
import os;
import sqlite3;
import math; 

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;

HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;

SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;

FRAME_RATE = 0.01;
# add more here

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg(self):
        result = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, \
                                                                        self.obj.still_ball.pos.y, BALL_RADIUS, \
                                                                        BALL_COLOURS[self.obj.still_ball.number]);
        return result;

################################################################################

class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;


    # add an svg method here
    def svg(self):
        result = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, \
                                                                        self.obj.rolling_ball.pos.y, BALL_RADIUS, \
                                                                        BALL_COLOURS[self.obj.rolling_ball.number]);
        return result;

################################################################################

class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a Hole class
        self.__class__ = Hole;


    # add an svg method here
    def svg(self):
        result = """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, \
                                                                        self.obj.hole.pos.y, HOLE_RADIUS);
        return result;

################################################################################

class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, y):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y );
      
        # this converts the phylib_object into a HCushion class
        self.__class__ = HCushion;


    # add an svg method here
    def svg(self):
        # on top ?
        if (self.obj.hcushion.y == 0):
            tempY = -25;
        # on bottom?
        elif(self.obj.hcushion.y == 2700):
            tempY = 2700;
        result = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (tempY);
        return result;

################################################################################

class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, x):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0 );
      
        # this converts the phylib_object into a VCushion class
        self.__class__ = VCushion;


    # add an svg method here
    def svg(self):
        # on left ?
        if (self.obj.vcushion.x == 0):
            tempX = -25;
        # on right?
        elif(self.obj.vcushion.x == 1350):
            tempX = 1350;
        result = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (tempX);
        return result;

################################################################################
class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retrieval support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.6f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        result = HEADER;
        for i,obj in enumerate(self):
            if (obj != None):
                result += obj.svg();
        result += FOOTER;
        return result;
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                                    Coordinate(0,0),
                                                    Coordinate(0,0),
                                                    Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                                Coordinate( ball.obj.still_ball.pos.x,
                                                                    ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

"""=========================================================================================
    ========================================================================================="""
# PART 3

class Database():
    conn = None;
    def __init__(self, reset=False):
        if (reset == True):
            if os.path.exists( 'phylib.db' ):
                os.remove( 'phylib.db' );
        self.conn = sqlite3.connect("phylib.db");
    
    def createDB(self):
        cur = self.conn.cursor();
        cur.execute("""SELECT * FROM sqlite_master
                                WHERE TYPE = 'table';""");
        #print("STARTING");
        tableList = cur.fetchall();
        #print ('\n'.join(str(e) for e in tableList));
        if not(any (table[1] == 'Ball' for table in tableList)):
            print("BALL DOESNT EXIST");
            cur.execute( """CREATE TABLE Ball 
                        ( BALLID    INTEGER    NOT NULL,
                        BALLNO   INTEGER    NOT NULL,
                        XPOS       FLOAT         NOT NULL,
                        YPOS       FLOAT         NOT NULL,
                        XVEL       FLOAT,
                        YVEL       FLOAT,
                        PRIMARY KEY (BALLID AUTOINCREMENT) );""" );
            #print("ball table created");
        if not (any (table[1] == 'TTable' for table in tableList)):
            cur.execute( """CREATE TABLE TTable 
                        ( TABLEID INTEGER    NOT NULL,
                        TIME       FLOAT        NOT NULL,
                        PRIMARY KEY (TABLEID AUTOINCREMENT) );""" );
            #print("ttable created");
        if not (any (table[1] == 'BallTable' for table in tableList)):
            cur.execute( """CREATE TABLE BallTable 
                        ( BALLID INTEGER    NOT NULL,
                        TABLEID INTEGER    NOT NULL,
                        FOREIGN KEY (BALLID) REFERENCES Ball,
                        FOREIGN KEY (TABLEID) REFERENCES TTable );""" );
            #print("balltable created");
        if not (any (table[1] == 'Shot' for table in tableList)):
            cur.execute( """CREATE TABLE Shot 
                        ( SHOTID INTEGER    NOT NULL,
                        PLAYERID INTEGER    NOT NULL,
                        GAMEID    INTEGER    NOT NULL,
                        PRIMARY KEY (SHOTID AUTOINCREMENT),
                        FOREIGN KEY (PLAYERID) REFERENCES Player,
                        FOREIGN KEY (GAMEID) REFERENCES Game );""" );
            #print("shot table created");
        # assume shots occur in increasing order of SHOTID
        if not (any (table[1] == 'TableShot' for table in tableList)):
            cur.execute( """CREATE TABLE TableShot 
                        ( TABLEID INTEGER    NOT NULL,
                        SHOTID    INTEGER    NOT NULL,
                        FOREIGN KEY (TABLEID) REFERENCES TTable,
                        FOREIGN KEY (SHOTID) REFERENCES Shot );""" );
            #print("table shot table created");
        # assume TABLEIDs are in chronological order
        if not (any (table[1] == 'Game' for table in tableList)):
            cur.execute( """CREATE TABLE Game 
                        ( GAMEID     INTEGER           NOT NULL,
                        GAMENAME VARCHAR(64)    NOT NULL,
                        PRIMARY KEY (GAMEID AUTOINCREMENT) );""" );
            #print("game table created");
        if not (any (table[1] == 'Player' for table in tableList)):
            cur.execute( """CREATE TABLE Player 
                        ( PLAYERID     INTEGER           NOT NULL,
                        GAMEID          INTEGER           NOT NULL,
                        PLAYERNAME  VARCHAR(64)    NOT NULL,
                        PRIMARY KEY (PLAYERID AUTOINCREMENT),
                        FOREIGN KEY (GAMEID) REFERENCES Game );""" );
            #print("player table created");
        cur.close();
        self.conn.commit();
    def readTable (self, tableID):
        """create Balls whose BALLIDs are in the BallTable table with a TABLEID that
            is one larger than the method's argument"""
        retTable = Table();
        cur = self.conn.cursor();
        temp = cur.execute("""SELECT * FROM BallTable
                                                WHERE (BallTable.TABLEID = ?);""", (tableID + 1,)).fetchall();
        if (not temp):
            return None;
        cur.execute("""SELECT * FROM Ball, BallTable
                                    WHERE (Ball.BALLID = BallTable.BALLID
                                    AND BallTable.TABLEID = ?);""", (tableID + 1,));
        ballsTemp = cur.fetchall();
        #for column in tempBalls.description: 
        #    print(column[0]);
        #print ('\n'.join(str(e) for e in ballsTemp));
        for ball in ballsTemp:
            if (ball[4] == 'NULL' and ball[5] == 'NULL'):
                sb = StillBall(ball[1], Coordinate(ball[2], ball[3]));
                retTable.add_object(sb);
            else:
                velX = float(ball[4]);
                velY = float(ball[5]);
                ballLen = math.sqrt(velX * velX + velY * velY);
                accX = 0;
                accY = 0;
                if ballLen > VEL_EPSILON:
                    accX = (velX * (-1)) / ballLen * DRAG;
                    accY = (velY * (-1)) / ballLen * DRAG;
                rb = RollingBall(ball[1], Coordinate(ball[2], ball[3]), Coordinate(ball[4], ball[5]),
                                                    Coordinate(accX, accY));
                retTable.add_object(rb);

        cur.close();
        self.conn.commit();
        return retTable;

    def writeTable(self, table):
        cur = self.conn.cursor();
        cur.execute("""INSERT INTO TTable (TIME)
                                VALUES (?);""", (table.time,));
        cur.execute("""SELECT TABLEID FROM TTable;""");
        tableID = max(cur.fetchall())[0];
        #print("tableid ", tableID);
        for object in table:
            if isinstance( object, StillBall ):
                cur.execute("""INSERT INTO Ball
                                        VALUES (?, ?, ?, ?, ?, ?);""", (None, object.obj.still_ball.number,\
                                        object.obj.still_ball.pos.x, object.obj.still_ball.pos.y, "NULL", "NULL"));
                ballID = max(cur.execute("""SELECT BALLID FROM Ball;""").fetchall())[0];
                #print("ballid ", ballID);
                cur.execute("""INSERT INTO BallTable
                                        VALUES (?, ?);""", (ballID, tableID));
            if isinstance( object, RollingBall ):
                cur.execute("""INSERT INTO Ball
                                        VALUES (?, ?, ?, ?, ?, ?);""", (None, object.obj.rolling_ball.number,\
                                        object.obj.rolling_ball.pos.x, object.obj.rolling_ball.pos.y, \
                                        object.obj.rolling_ball.vel.x, object.obj.rolling_ball.vel.y));
                ballID = max(cur.execute("""SELECT BALLID FROM Ball;""").fetchall())[0];
                #print("ballid ", ballID);
                cur.execute("""INSERT INTO BallTable
                                        VALUES (?, ?);""", (ballID, tableID));
        self.conn.commit();

        '''data = cur.execute("""SELECT * FROM BallTable""");
        dataText = cur.fetchall();
        for column in data.description: 
            print(column[0]);
        print ('\n'.join(str(e) for e in dataText));'''

        cur.close();
        return tableID;

    def close(self):
        self.conn.commit();
        self.conn.close();
    
    def getGame (self, id):
        cur = self.conn.cursor();
        data = cur.execute("""SELECT * FROM Game, Player
                                WHERE (Player.GAMEID = ?
                                AND Game.GAMEID = ?);""", (id, id));
        dataText = cur.fetchall();
        for column in data.description: 
            print(column[0]);
        self.conn.commit();
        cur.close();
        return dataText;
        
    def setGame (self, gN, p1N, p2N):
        cur = self.conn.cursor();
        cur.execute("""INSERT INTO Game
                                VALUES (?, ?);""", (None, gN));
        cur.execute("""SELECT GAMEID FROM Game;""");
        gameID = max(cur.fetchall())[0];
        print("max gameid is '%d'"%gameID);
        cur.execute("""INSERT INTO Player
                                VALUES (?, ?, ?);""", (None, gameID, p1N));
        cur.execute("""INSERT INTO Player
                                VALUES (?, ?, ?);""", (None, gameID, p2N));
                                
        self.conn.commit();
        cur.close();


class Game():
    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        db = Database();
        db.createDB();
        if (isinstance(gameID, int)):
            print("GAMEID IS INT");
            if not (gameName is None and player1Name is None and player2Name is None):
                print("GAMEID IS INT, OTHER INPUTS ARENT NONE")
                raise TypeError;
            else:
                tempID = gameID + 1;
                table = db.getGame(tempID);
                
                print(table);
                gameName = table[0][0];
                player1Name = table[0][4];
                player2Name = table[1][4];
                print("p1 is %s and p2 is %s" % (player1Name, player2Name));
        elif (gameID is None):
            if not (isinstance(gameName, str) and isinstance(player1Name, str) and isinstance(player2Name, str)):
                print ("GAMEID IS NONE, NO STRING INPUT")
                raise TypeError;
            else:
                print("setting");
                db.setGame(gN=gameName, p1N=player1Name, p2N=player2Name);
        else:
            print("WRONG INPUT FORMAT");
            raise TypeError;