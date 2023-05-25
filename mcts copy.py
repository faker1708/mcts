import node


class mcts():
    def __init__(self,r,d,p,assess,action_space):
        self.sensory=r
        self.inference = d
        self.strategy = p   # dqn
        self.time_limit = 2**10
        self.action_space = action_space    # 动作空间容积
        self.assess = assess    # 评估局势的函数

    def choose_child(self,node_a,think):
        return

    def rollout(self,node_a):
        # random policy
        # muzero 的mcts没有结局，可以无限仿真下去，所以要设置极限。
        # alphago的仿真是有结局的,可以用极限来停止，也可以一直下到终局。

        rollout_limit = 2**10
        rt= rollout_limit
        s = node_a.sub_conscious
        while(1):
            action = self.random_action(s)
            next_s = self.inference(s,action)
            s = next_s
            rt -= 1
            if(rt<=0):
                break
        value = self.assess(s)
        return value


    def get_virgin(self,root):
        a = root
        while(1):
            if(a.virgin):
                break
            else:
                self.expand(a)
                a = self.choose_child(a,think = 1)
        return a

    def think(self,root):
        time_left = self.time_limit
        while(1):
            virgin = self.get_virgin(root)
            value = self.rollout(virgin)
            self.back_propagate(virgin,value)


            # self.time_left-=1
            time_left-=1
            if(time_left<=0):
                break
        return

    def decide(self,root):
        child = self.choose_child(root,think = 0)
        action = child.action
        return action

    def take_actioin(self,peception):
        sub_conscious = self.sensory(peception)
        root = node(sub_conscious,parent = 0,action = -1)


        # self.time_left = self.time_limit
        self.think(root)
        action = self.decide(root)
        return action




action  = mcts.take_action(perception)