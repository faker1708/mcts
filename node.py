

class node():
    def __init___(self,sub_conscious,parent,root,action):

        self.sub_conscious = sub_conscious
        self.parent = parent
        self.root = root
        self.child = list()
        self.action = action    # 从上级状态经历什么动作来到这里？

        # bp
        self.virgin = 1 # not rollout yet
        self.value = 0
        self.explore_count = 0

