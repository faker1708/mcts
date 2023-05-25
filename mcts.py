import node
import math # ucb log

class mcts():
    def __init__(self,d,p,assess,action_space):
        # self.sensory=r
        self.inference = d
        self.strategy = p   # dqn mc 依概率抽样
        self.time_limit = 2**10
        self.action_space = action_space    # 动作空间容积
        self.assess = assess    # 评估局势的函数

    def choose_child(self,node_a,think):
        #默认返回u最大的子节点
        
        for i,child in enumerate(node_a.child):
            if(child.explore_count==0):
                if(think ==0):
                    raise(BaseException('logic error.决定阶段,不应该有未探索过的子节点'))    # 抛出一个逻辑错误。
                return child    # 这是刚刚新增 的，直接返回即可
        
        child_u_list = list()
        
        root = node_a.root
        for i,child in enumerate(node_a.child):
            right = 0
            if(think):
                up = math.log(root.explore_count)
                down = child.explore_count
                rx = up/down
                right = 2*rx**0.5
                pass
            
            left = child.value/child.explore_count

            u = left + right
            child_u_list.append(u)
        # 也可以根据计算好的u表，自行设计选择策略

        # 以下是选择最大u的子节点的策略
        init = 1
        u_max = 0
        max_u_child = 0
        for i,u in enumerate(child_u_list):
            change = 0
            if(init==1):
                change= 1
            else:
                if(u>u_max):
                    change = 1
            init = 0

            if(change==1):
                u_max = u
                max_u_child = child

        return max_u_child

    def expand(self,node_a):
        # 询问神经网络，是否要新增节点
        # 根据神经网络的输出，建立概率分布，抽样，得到一个动作
        # 如果这个动作已有对应的子结点，就不再新增节点
        # 这样，就完成了依概率新增节点的方法

        # if need a new child
        action = self.strategy(node_a.sub_conscious)    # 用p网络，依概率抽样一个动作出来
        ok = 0
        for i,child in enumerate(node_a.child):
            if(child.action == action):
                ok = 1
                break
        if(ok==0):
            ns = self.inference(node_a.sub_conscious,action)
            new_child = node(ns,node_a,node_a.root,action)
            node_a.child.append(new_child)
        return



    def get_virgin(self,root):
        a = root
        while(1):
            if(a.virgin):
                break
            else:
                self.expand(a)
                a = self.choose_child(a,think = 1)
        return a
    

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

    def back_propagate(self,virgin,value):
        p = virgin
        while(1):
            if(p==0):   # 判断为根节点的指标
                break
            else:
                p.value += value
                p.explore_count +=1
                p.virgin = 0

                p = p.parent
        return

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

    # def decide(self,root):
    #     child = self.choose_child(root,think = 0)
    #     action = child.action
    #     return action

    # def take_actioin(self,sub_conscious):
    #     #咱也别输出动作了，就输出动作价值表吧，让外部自己去选。

    #     # sub_conscious = self.sensory(peception)
    #     root = node(sub_conscious,parent = 0,root = 0,action = -1)
        root.root = root

    #     # self.time_left = self.time_limit
    #     self.think(root)
    #     action = self.decide(root)
    #     return action




# action  = mcts.take_action(sub_conscious)