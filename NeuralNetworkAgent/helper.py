import matplotlib.pyplot as plt
from IPython import display
import numpy as np

plt.ion()


generationn = 0

def plot(scores, mean_scores):
    display.clear_output(wait=True)
    global generationn
    generationn += 1
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number Of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    
    plt.xlim([generationn-100, generationn])

    plt.plot(mean_scores)
    #plt.ylim(ymin = 0) # i want to see how low it goes
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.pause(0.00000001)
    
    