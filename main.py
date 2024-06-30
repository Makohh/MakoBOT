# This file is for strategy

from util.objects import *
from util.routines import *


class Bot(BotCommandAgent):
    # This function runs every in-game tick (every time the game updates anything)
    def run(self):
        d1 = abs(self.ball.location.y - self.foe_goal.location.y - 150)
        d2 = abs(self.me.location.y - self.foe_goal.location.y)
        near_net = abs(self.ball.location.y - self.friend_goal.location.y)
        defending = abs(self.me.location.y - self.friend_goal.location.y)
        is_in_front_of_ball = d1 > d2
        if (self.intent is not None):
            return
        if self.kickoff_flag:
            self.set_intent(kickoff())
            return
        # if we're in front of the ball, retreat
        if is_in_front_of_ball:
            self.set_intent(goto(self.friend_goal.location))
            print('retreating')
            return
        # if the ball is near our net, return to net and clear
        if near_net <= abs(1200):
            self.set_intent(goto(self.friend_goal.location))
            print('ball near net')
            if defending < abs(100):
                self.set_intent(short_shot(self.foe_goal.location))
                print('defending')
                return
            return
        self.set_intent(short_shot(self.foe_goal.location))