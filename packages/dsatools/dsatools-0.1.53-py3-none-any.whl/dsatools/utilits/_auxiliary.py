import numpy as np
from . _awgn import wgn_with_snr, signal_like_noise

_all__ = ['pad_to_power_of_2','pad_noises']

def pad_to_power_of_2(signal,
                      method = None, param = 0):
    '''
    Padding to length as power of 2.
    
    Paramteres
    -----------------
    * signal: 1d ndarray,
        input signal.
    * method, string,
        method of padding:
        * 'zeroing' - with 0;
        * None or 'constant'
            - with param value;
        * 'reflect', with the the mirrored 
                        samples, without last.
        * 'symmetric', with the the mirrored 
                        samples, with last.
        * 'cyclic', with repeat from first sample.
        * 'linear_ramp' with samples from 
                last value to 0
        * 'noise','wgn': with
            noise of power param;
        * 'awgn': noise of SNR param; 
        * 'signal_noise': with noise as
           random signal samples 
           with SNR param;
    * param: float,
        auxiliary parameter.
        
    Returns
    ------------
    * padded signal.    
    '''       
    N = len(signal)
    
    N_new = np.power(2,int(np.log2(N))+1)
    
    if method is None or method is 'constant':
        return np.pad(signal,(0,N_new-N),
                      'constant', 
                      constant_values = param)

    elif method is 'zeroing':
        return np.pad(signal,(0,N_new-N),'constant', 
                                          constant_values = 0)
    
    elif method in ['noise','wgn']:
        return np.concatenate((signal, 
                               param*np.random.randn(N_new-N) ))
    
    elif method is 'awgn':
        return np.concatenate((signal, 
                               wgn_with_snr(signal, 
                                            param, 
                                            length=N_new-N) )) 
    
    elif method is 'signal_noise':
        return np.concatenate((signal, 
                               signal_like_noise(signal,
                                                 param)[:N_new-N]))    
    
    elif method in ['reflect','symmetric','linear_ramp']:
        return np.pad(signal,(0,N_new-N),method)
    
    elif method is 'cyclic':
        #TODO: what if N_new-N>N - it is not the case for pow2
        return np.concatenate((signal, 
                               signal[:N_new-N] ))    
    
    else:
        return ValueError('uncorrect value')

#-----------------------------------------------
def pad_noises(signal, 
               pad_width = [0,0], 
               snr = 30, 
               method = 'wng_db', 
               random_state = None):
    '''
    Padding with pad_width.
    
    Paramteres
    -----------------
    * signal: 1d ndarray,
        input signal.
    * pad_width int list, [before, after],
        number of values add before and after,
        if only one value - then only after.
    * snr_db, float, or None,
        Signal-to-Noise ratio in dB by default,
        could have different meaning depends 
        on the method.
        If None, than zeros will be padded.    
    * method, string:
        * 'wng_db': padding with 
            White Gaussian Noises, SNR in dB.
        * 'wng': padding with 
            Noise Power, in abs value. 
        * 'signal_like': padding with 
            Noises taken as random signal samples,
            with SNR in dB.             
    * random_state: float,
        random state.
     
    Returns
    ------------
    * padded signal.
    
    ''' 
    signal = np.asarray(signal)
    pad_width = np.asarray(pad_width,dtype=int)
    if pad_width.size <2:
        pad_width = np.array([0, 
                              np.squeeze(pad_width)])
    if snr is None:
        return np.pad(signal,pad_width)
    
    if method is 'wng_db':
        return np.concatenate((
                       wgn_with_snr(signal,snr = snr, 
                                    length=pad_width[0],
                                    random_state = random_state),
                       signal, 
                       wgn_with_snr(signal,snr = snr, 
                                    length=pad_width[1],
                                    random_state = random_state),
                              ))
    elif method is 'wng':
        return np.concatenate((
                       wgn(snr, 
                              length=pad_width[0],
                              is_complex = (
                                  signal.dtype == complex),
                               random_state = random_state),
                       signal, 
                       wgn(snr, 
                              length=pad_width[1],
                              is_complex = (
                                  signal.dtype == complex),
                              random_state = random_state),
                              ))    
    
    elif method is 'signal_like':
        return np.concatenate((
                    signal_like_noise(signal, 
                                      snr=snr,
                                      length = pad_width[0],
                                      random_state = random_state),
                    signal,
                    signal_like_noise(signal, 
                                      snr=snr,
                                      length = pad_width[1],
                                      random_state = random_state)
                              ))    
    
    else:
        return ValueError('uncorrect value')
