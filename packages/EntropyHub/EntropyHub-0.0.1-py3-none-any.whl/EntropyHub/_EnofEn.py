"""Base Entropy of Entropy Function"""    
import numpy as np

def EnofEn(Sig, tau=10, S=(10,5), Logx=np.exp(1)):
    """EnofEn  estimates the entropy of entropy of a univariate data sequence.
    
    .. code-block:: python

        EoE, AvEn = EnofEn(Sig) 

    Returns the entropy of entropy (``EoE``) and the average Shannon entropy 
    across all windows (``AvEn``) estimated from the data sequence (``Sig``) using
    the default parameters: 
    window length (samples) = 10, slices (s1,s2) = [10 5], logarithm = natural

    .. code-block:: python
        
        EoE, AvEn = EnofEn(Sig, keyword = value, ...)
        
    Returns the entropy of entropy (``EoE``) estimated from the data sequence (``Sig``)  
    using the specified 'keyword' arguments:
        :tau:   - Window length, an integer > 1
        :S:     - Number of slices (s1,s2), a two-element tuple of integers > 2
        :Logx:  - Logarithm base, a positive scalar  
 
    :See also::
        ``SampEn``, ``MSEn``
    
    :References:
        [1] Chang Francis Hsu, et al.,
            "Entropy of entropy: Measurement of dynamical complexity for biological systems." 
            Entropy 
            19.10 (2017): 550.
    
    """
        
    Sig = np.squeeze(Sig)

    assert Sig.shape[0]>10 and Sig.ndim == 1,  "Sig:   must be a numpy vector"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
    assert isinstance(tau,int) and (tau > 1), "tau:   must be an integer > 1"
    assert isinstance(S,tuple) and len(S)==2 and isinstance(S[0] and S[1],int) \
    and min(S)>2, "S:     must be a two-element tuple of integers with values > 2"
        
    Wn = int(np.floor(Sig.shape[0]/tau))
    Wj = np.reshape(Sig[:Wn*tau],(Wn,tau))
    Edges = np.linspace(min(Sig),max(Sig),S[0]+1)
    Yj = np.zeros(Wn)
    for n in range(Wn):
        Temp,_ = np.histogram(Wj[n,:],Edges)        
        Temp = Temp[Temp!=0]/tau
        Yj[n] = -sum(Temp*(np.log(Temp)/np.log(Logx)))
        
    AvEn = sum(Yj)/Wn
    Edges = np.linspace(min(Yj),max(Yj),S[1]+1)
    Pjl,_ = np.histogram(Yj,Edges)
    Pjl = Pjl/Wn
    Pjl = Pjl[Pjl!=0]
    if round(sum(Pjl),5) != 1:
        print('Warning: Possible error estimating probabilities')
    EoE = -sum(Pjl*(np.log(Pjl)/np.log(Logx)))            
    return EoE, AvEn
"""
    Copyright 2021 Matthew W. Flood, EntropyHub
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
     http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    
    For Terms of Use see https://github.com/MattWillFlood/EntropyHub
"""