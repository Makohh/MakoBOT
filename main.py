# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits


class Bot(BotCommandAgent):
    # This function runs every in-game tick (every time the game updates anything)
    def run(self):
        d1 = abs(self.ball.location.y - self.foe_goal.location.y - 150)
        d2 = abs(self.me.location.y - self.foe_goal.location.y)
        near_net = abs(self.ball.location.y - self.friend_goal.location.y)
        defending = abs(self.me.location.y - self.friend_goal.location.y)
        is_in_front_of_ball = d1 > d2
        targets = {
            'at_opponent_goal': (self.foe_goal.left_post, self.foe_goal.right_post),
            'away_from_my_goal': (self.friend_goal.right_post, self.friend_goal.left_post)
        }
        hits = find_hits(self,targets)

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
        if near_net <= abs(1500):
            self.set_intent(goto(self.friend_goal.location))
            print('ball near net')
            if defending < abs(100):
                if len(hits['away_from_my_goal']) > 0:
                    self.set_intent(hits['away_from_my_goal'][0])
                    print('defending')
                    return
                return
            return
        if len(hits['at_opponent_goal']) > 0:
            self.set_intent(hits['at_opponent_goal'][0])
            print('shooting at goal')
            return

        # Boost Logic
        available_boosts = [boost for boost in self.boosts if boost.active]

        closest_boost = None
        closest_distance = 10000

        for boost in available_boosts:
            distance = (self.me.location - boost.location).magnitude()
            if closest_boost is None or distance < closest_distance:
                closest_boost = boost
                closest_distance = distance

        if closest_boost is not None:
            self.set_intent(goto(closest_boost.location))
            print('Grabbing Boost')
            return
