#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 规则1：周围有两个或者三个活细胞，下一世代，该细胞仍然活着。  
# 规则2：周围少于两个活细胞，该细胞死于孤立。  
# 规则3：周围多于三个活细胞，该细胞死于拥挤。

# 先写一个对象，每个格子的元胞

class cell(object):
    def __init__(self) -> None:
        self.alive = False
        self.position = (0, 0)
        self.size = 10
    
    def _count(slef):
        pass
