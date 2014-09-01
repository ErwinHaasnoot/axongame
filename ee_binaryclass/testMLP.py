# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    from utils import funcs
    from utils.MLP import MLP

    
        

    network = MLP(2,2,1)
    samples = np.zeros(4, dtype=[('input',  float, 2), ('output', float, 1)])

    # Example 1 : OR logical function
    # -------------------------------------------------------------------------
    print "Learning the OR logical function"
    network.reset()
    samples[0] = (0,0), 0
    samples[1] = (1,0), 1
    samples[2] = (0,1), 1
    samples[3] = (1,1), 1
    network.learn(samples)

    # Example 2 : AND logical function
    # -------------------------------------------------------------------------
    print "Learning the AND logical function"
    network.reset()
    samples[0] = (0,0), 0
    samples[1] = (1,0), 0
    samples[2] = (0,1), 0
    samples[3] = (1,1), 1
    network.learn(samples)

    # Example 3 : XOR logical function
    # -------------------------------------------------------------------------
    print "Learning the XOR logical function"
    network.reset()
    samples[0] = (0,0), 0
    samples[1] = (1,0), 1
    samples[2] = (0,1), 1
    samples[3] = (1,1), 0
    network.learn(samples)
    network.storeWeights('XORWeight.p')
    
    network.reset()
    network.loadWeights('XORWeight.p')
    
    network.test(samples)
    # Example 4 : Learning sin(x)
    # -------------------------------------------------------------------------
    print "Learning the sin function"
    network = MLP(1,10,1)
    samples = np.zeros(500, dtype=[('x',  float, 1), ('y', float, 1)])
    samples['x'] = np.linspace(0,1,500)
    samples['y'] = np.sin(samples['x']*np.pi)

    for i in range(10000):
        n = np.random.randint(samples.size)
        network.propagate_forward(samples['x'][n])
        network.propagate_backward(samples['y'][n])

    #plt.figure(figsize=(10,5))
    # Draw real function
    x,y = samples['x'],samples['y']
    #plt.plot(x,y,color='b',lw=1)
    # Draw network approximated function
    for i in range(samples.shape[0]):
        y[i] = network.propagate_forward(x[i])
    
    #plt.plot(x,y,color='r',lw=3)
    #plt.axis([0,1,0,1])
    #plt.show()
    
    
    # Example 5: Learning game 3 spike training data
    # -------------------------------------------------------------------------
    
    import scipy.stats as st
    
    network = MLP(10,1)
    l = 500000
    samples = np.zeros(l, dtype=[('input',  float, 10), ('output', float, 1)])
    samples = funcs.generateSamples(l, lambda x: 0 if x[2] < .28 else 1)
    
    out = network.learn(samples, epochs= 10000000)
    stepf= lambda x: 1 if x > .5 else 0
    test_data = [(t[0], t[1], stepf(t[2])) for t in out]
    percHits = np.mean([1 if t[2] == 1 else 0 for t in test_data if t[1] == 1]) # Percentage right hits
    falseAlarm = np.mean([1 if t[2] == 1 else 0 for t in test_data if t[1] == 0]) # Percentage false positives
    
    print 'Hit % = {}, but false alarm % = {}'.format(percHits,falseAlarm) 
    print network.weights  
    