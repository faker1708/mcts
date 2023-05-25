

mcts()



sub_conscious = sensory(perception)

action_q_list = mcts.take_action(sub_conscious)


take_action{
    think
    decide

}


think{
    get_virgin
    rollout
    back_propagate
}


decide{

    return root.q_list
}



get_virgin{
    expand
    choose_child
}
rollout{
    rollout_policy(一般用随机动作)
    inference
}

back_propagate{

}




expand{
    is_all_expand   (改成,向神经网络询问是否需要新增节点,而不是不满就新增 .)
    add_child
    inference
}
choose_child{
    
    u = left+right
    return 最大u的child
}