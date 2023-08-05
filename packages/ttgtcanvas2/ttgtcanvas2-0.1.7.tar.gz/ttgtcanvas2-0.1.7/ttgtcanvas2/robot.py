_directions = [(1,0), (0,1), (-1,0), (0,-1)]

dir_names = ["east", "north","west", "south"]

from .models.world_model import print_success, print_error
import time as _time

class Robot():
    def __init__(self, index, robot_model, world):
        self.model = robot_model
        self.world_model = world.model
        self.world = world
        self.index = index
        self.collections = {}
        self.speed  = 0.5
        self.last_picked = []
 
    @property
    def x(self):
        return self.model.x
    
    @property
    def y(self):
        return self.model.y
    
    @property
    def dir(self):
        return self.model.orientation
    
    @dir.setter
    def dir(self, value):
        self.model.orientation = value

    @x.setter
    def x(self,value):
        self.model.x = value
    
    @y.setter
    def y(self, value):
        self.model.y = value
    
    def move(self, step=1):
        """Move one step in direction where robot is facing.

        Parameters
        ---------
        step : int
        number of steps to move

        Examples
        --------
        For moving one step
        >>> bot.move()

        For moving 10 step
        >>> bot.move(10)
        """
        self.world_model.incr_instruction(step)
        for x in range(step):
            self._move()
        self.world.js_call('move_to',[self.index, self.x, self.y])
    
    def _move(self):
        if self.front_is_clear():
            xx, yy = _directions[self.dir]
            self.x += xx
            self.y += yy
        else:
            print_error("Opps You Hit the walls") 
            self.world.js_call('error', ['Opps You Hit the wall'])
    
    def front_is_clear(self):
        """Checks if no wall or border in front of robot.

        Returns
        -------
        bool
            Returns True if no wall or border in front of robot.

        Examples
        --------
        >>> bot.front_is_clear()
        True
        """
        return self.world_model.is_clear(self.x, self.y, self.dir)
    
    def done(self):
        """Checks if all the goals are completed.

        Returns
        -------
        bool
            Returns True if all the goals are completed.

        Examples
        --------
        >>> bot.done()
        True
        """
        self.world_model.incr_instruction()

        return self.world.model.done(self)
    
    def turn_left(self):
        """Rotate left by 90 degrees.

        Examples
        --------
        >>> bot.turn_left()
        """
        self.world_model.incr_instruction()
        self.dir = (self.dir + 1) % 4
        self.world.js_call('turn_left', [self.index])
    
    def is_front_clear(self):
        """Checks if no wall or border in front of robot.

        Returns
        -------
        bool
            Returns True if no wall or border in front of robot.

        Examples
        --------
        >>> bot.is_front_clear()
        True
        """

        return self.world_model.is_clear(self.x, self.y, self.dir)
    
    def right_is_clear(self):
        """Checks if no wall or border in right of robot.

        Returns
        -------
        bool
            Returns True if no wall or border in right of robot.

        Examples
        --------
        >>> bot.right_is_clear()
        True
        """

        return self.world.model.is_clear(self.x, self.y, (self.dir + 3) % 4)
    
    def wall_on_right(self):
        """Checks if there is  wall or border in right of robot.

        Returns
        -------
        bool
            Returns True if there is  wall or border in right of robot.

        Examples
        --------
        >>> bot.wall_on_right()
        True
        """

        return not self.right_is_clear()
    
    def wall_on_front(self):
        """Checks if there is  wall or border in front of robot.

        Returns
        -------
        bool
            Returns True if there is  wall or border in front of robot.

        Examples
        --------
        >>> bot.wall_on_front()
        True
        """

        return not self.is_front_clear()
    
    def report(self, msg):
        """ Reports the msg to Reporter goal

        Parameters
        ---------
        msg : str
        message to report

        Examples
        --------
        >>> bot.report("Counted 10 apples")

        """
        self.report = msg
    
    def cell(self):
        return self.world_model.cells[self.x - 1][self.y - 1 ]

    def build_wall(self):

        """Builds wall if there is No wall or border in front of robot 
            and its allowed.

        Examples
        --------
        >>> bot.build_wall()
        """
        self.world_model.incr_instruction()
        cell =  self.cell()
        if self.is_front_clear() and cell.has_goal_wall(self.dir) :
            cell.add_wall(self.dir, self.world.js_call)
        else:
            print_error("Wall Already exists")
            self.world.js_call("error", ["Wall already exists"])
    
    def remove_wall(self):
        """Removes wall if there is  wall in front of robot 

        Examples
        --------
        >>> bot.remove_wall()
        """

        self.world_model.incr_instruction()
        if not self.is_front_clear():
            self.cell().remove_wall(self.dir, self.world.js_call)
        else:
            print_error("No Wall exists")
            self.world.js_call("error", ["No Wall exists"])


    def set_trace(self, color='red'):
        """
            sets a new trace in that color.

        Examples
        --------
        >>> bot.set_trace('red')
        """

        self.world.js_call('set_trace', [self.index, color])
    
    def set_speed(self, speed=0.1):
        """
            sets the speed for the bot movement in seconds.

        Examples
        --------
        >>> bot.set_speed(1)
        """

        self.speed = speed
        self.world.js_call('set_speed', [self.index, speed])
    
    def has_object(self, obj_name = None):
        """Checks if there is  object on the current cell.
        Parameters
        ---------
        obj_name : str
        object name like carrot, beeper, star, apple

        Returns
        -------
        int
            Returns object count  if there is  object on the current cell.

        Examples
        --------
        >>> bot.has_object()
        1

        >>> bot.has_object('apple')
        3
        """

        self.world_model.incr_instruction()
        objs = self.collections.values()
        if len(objs) > 0:
            if obj_name is None:
                return 1
            else:
                fobjs = list(filter(lambda x, y: x == obj_name, objs))
                return sum(fobjs.values())
        else: 
            return 0
        

    def object_here(self):
        """Checks if there is  object on the current cell.

        Returns
        -------
        str
            Returns object name if there is  object on the current cell.

        Examples
        --------
        >>> bot.object_here()
        "apple"
        """
        self.world_model.incr_instruction()
        k = "{},{}".format(self.x,self.y)
        obj = self.world_model.objects.get(k, None)
        if obj is not None:
            obj_name = next(iter(obj))
            return obj_name
        else:
            return None
    
    def at_goal(self):
        """Checks if bot is at goal position.

        Returns
        -------
        bool
            Returns True if bot is at goal position.

        Examples
        --------
        >>> bot.at_goal()
        True
        """

        self.world_model.incr_instruction()
        goal = self.world_model.position_goal()

        if len(goal) > 0:
            goal = goal[0]
            return goal.is_completed(self)
        return False
    
    def put(self):
        """Places the last picked object on the current cell.

        Examples
        --------
        >>> bot.put()
        """
        
        self.world_model.incr_instruction()
        if len(self.last_picked) > 0:
            [o_name, ck] = self.last_picked.pop()
            collection = self.collections.get(ck, None)
            if collection is not None and o_name in collection:
                obj = collection.get(o_name, 0)
                if obj > 1:
                    collection[o_name] -= 1
                else:
                    del collection[o_name]
                self.collections[ck] = collection

                self.world_model.add_object(self.x, self.y, o_name, 1, self.world.js_call)
            

    def on_object(self, obj_type=None):
        """Checks if there is  object on the current cell.
        Parameters
        ---------
        obj_type : str
        object name like carrot, beeper, star, apple

        Returns
        -------
        int
            Returns True  if there is  object on the current cell.

        Examples
        --------
        >>> bot.on_object()
        True

        >>> bot.on_object('apple')
        False
        """
        self.world_model.incr_instruction()
        k = "{},{}".format(self.x,self.y)
        obj = self.world_model.objects.get(k, None)
        valid_type = True
        if obj is not None and obj_type is not None:
            obj_name = next(iter(obj))
            valid_type =  obj_name == obj_type

        return  obj is not None and valid_type and obj != self.collections.get(k, None) 
    
    def take(self, obj_type=None):
        """Collects the object of the current cell.

        Examples
        --------
        >>> bot.take()
        """
        self.world_model.incr_instruction()
        if self.on_object(obj_type):
            ck = "{},{}".format(self.x,self.y)
        
            obj = self.world_model.objects.get(ck, None)
            if obj is not None:
                for k, val in obj.items():
                    collection = self.collections.get(ck, {})
                    picked = collection.get(k, 0)
                    picked = picked + 1
                    collection[k] = picked
                    self.last_picked.append([k, ck])
                    self.collections[ck] = collection
                    if val == picked:
                        self.world.js_call('remove_object', [self.x,self.y])
                    if val > picked:
                        self.world.js_call('update_object', [self.x, self.y, val - 1])
        else:
            print_error("No Items to Pick.")
            self.world.js_call('error', ["No Items to Pick"])

