# ***************************************************************
# Copyright (c) 2021 Jittor. All Rights Reserved. 
# Maintainers:
#     Haoyang Peng <2247838039@qq.com>
#     Dun Liang <randonlang@gmail.com>.
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# ***************************************************************
import math
import numpy as np
import jittor as jt
from jittor.nn import binary_cross_entropy_with_logits

def simple_presum(x):
    src = '''
__inline_static__
@python.jittor.auto_parallel(1)
void kernel(int n0, int i0, in0_type* x, in0_type* out, int nl) {
    out[i0*(nl+1)] = 0;
    for (int i=0; i<nl; i++)
        out[i0*(nl+1)+i+1] = out[i0*(nl+1)+i] + x[i0*nl+i];
}
kernel(in0->num/in0->shape[in0->shape.size()-1], 0, in0_p, out0_p, in0->shape[in0->shape.size()-1]);
    '''
    return jt.code(x.shape[:-1]+(x.shape[-1]+1,), x.dtype, [x],
        cpu_src=src, cuda_src=src)


class OneHotCategorical:
    def __init__(self, probs=None, logits=None):
        assert not (probs is None and logits is None)
        if probs is None:
            # cannot align to pytorch
            probs = jt.sigmoid(logits)
        elif logits is None:
            logits = jt.log(probs)
        with jt.no_grad():
            self.probs = probs / probs.sum(-1, True)
            self.cum_probs = simple_presum(self.probs)
            self.cum_probs_l = self.cum_probs[..., :-1]
            self.cum_probs_r = self.cum_probs[..., 1:]
            self.logits = logits

    def sample(self, sample_shape=[]):
        shape = sample_shape + self.probs.shape[:-1] + (1,)
        rand = jt.rand(shape)
        one_hot = jt.logical_and(self.cum_probs_l < rand, rand <= self.cum_probs_r).float()
        return one_hot
    
    def log_prob(self,x):
        if len(x.shape) == 1:
            x = x.unsqueeze(0)
        logits = self.logits.broadcast(x.shape)
        indices = jt.argmax(x, dim=-1)[0]
        return logits.gather(1, indices.unsqueeze(-1)).reshape(-1)
    
    def entropy(self):
        min_real = -(math.pow(2,23)-1) / math.pow(2,22) * math.pow(2,127)
        logits = jt.clamp(self.logits,min_v=min_real)
        p_log_p = logits * self.probs
        return -p_log_p.sum(-1)
    
    
class Categorical:
    def __init__(self, probs=None, logits=None):
        assert not (probs is None and logits is None)
        if probs is None:
            # cannot align to pytorch
            probs = jt.sigmoid(logits)
        elif logits is None:
            logits = jt.log(probs)
        with jt.no_grad():
            self.probs = probs / probs.sum(-1, True)
            self.logits = logits
            self.cum_probs = simple_presum(probs)
            self.cum_probs_l = self.cum_probs[..., :-1]
            self.cum_probs_r = self.cum_probs[..., 1:]

    def sample(self, sample_shape=[]):
        shape = sample_shape + self.probs.shape[:-1] + (1,)
        rand = jt.rand(shape)
        one_hot = jt.logical_and(self.cum_probs_l < rand, rand <= self.cum_probs_r)
        index = one_hot.index(one_hot.ndim-1)
        return (one_hot * index).sum(-1)
    
    def log_prob(self, x):
        return jt.log(self.probs)[0,x]
    
    def entropy(self):
        min_real = -(math.pow(2,23)-1) / math.pow(2,22) * math.pow(2,127)
        logits = jt.clamp(self.logits,min_v=min_real)
        p_log_p = logits * self.probs
        return -p_log_p.sum(-1)


class Normal:
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma
    
    def sample(self, sample_shape=None):
        return jt.normal(jt.array(self.mu), jt.array(self.sigma),size=sample_shape)

    def log_prob(self, x):
        var = self.sigma**2
        log_scale = jt.log(self.sigma)
        return -((x-self.mu)**2) / (2*var) - log_scale-np.log(np.sqrt(2*np.pi))
    
    def entropy(self):
        return 0.5+0.5*np.log(2*np.pi)+jt.log(self.sigma)


class Uniform:
    def __init__(self,low,high):
        self.low = low
        self.high = high
        assert high > low
    
    def sample(self,sample_shape):
        return jt.uniform(self.low,self.high,sample_shape)
    
    def log_prob(self,x):
        if x < self.low or x >= self.high:
            return math.inf
        return -jt.log(self.high - self.low)
    
    def entropy(self):
        return jt.log(self.high - self.low)


class Geometric:
    def __init__(self,p=None,logits=None):
        assert (p is not None) or (logits is not None)
        assert 0 < p and p < 1
        if p is None:
            self.prob = jt.sigmoid(logits)
            self.logits = logits
        elif logits is None:
            self.prob = p
            self.logits = -jt.log(1. / p - 1)
        
    def sample(self, sample_shape):
        tiny = jt.info(self.probs.dtype).tiny
        u = jt.clamp(jt.rand(sample_shape),min_v=tiny)
        return (jt.log(u) / (jt.log(-self.probs+1))).floor()
    
    def log_prob(self, x):
        return x*jt.log(-self.prob+1)+jt.log(self.prob)
    
    def entropy(self):
        return binary_cross_entropy_with_logits(jt.array(self.logits),jt.array(self.prob)) / self.prob


def kl_divergence(cur_dist, old_dist):
    assert isinstance(cur_dist, type(old_dist))
    if isinstance(cur_dist, Normal):
        vr = (cur_dist.sigma / old_dist.sigma)**2
        t1 = ((cur_dist.mu - old_dist.mu) / old_dist.sigma)**2
        return 0.5*(vr+t1-1-jt.log(vr))
    if isinstance(cur_dist, Categorical) or isinstance(cur_dist,OneHotCategorical):
        t = cur_dist.probs * (cur_dist.logits-old_dist.logits)
        t[jt.array((old_dist.probs == 0))] = math.inf
        t[jt.array((cur_dist.probs == 0))] = 0
        return t.sum(-1)
    if isinstance(cur_dist, Uniform):
        res = jt.log((old_dist.high - old_dist.low) / (cur_dist.high - cur_dist.low))
        if old_dist.low > cur_dist.low or old_dist.high < cur_dist.high:
            res = math.inf
        return res
    if isinstance(cur_dist, Geometric):
        return -cur_dist.entropy() - jt.log(-old_dist.prob+1) / cur_dist.prob - old_dist.logits
