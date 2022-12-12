from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

for query in [f'q{i}' for i in range(1,5)]:
    curves = pd.read_csv(f'prc/{query}_prc.csv')
    fig, axs = plt.subplots(1, 4, sharey=True)
    for i, system in enumerate(['sys1', 'sys2', 'sys1_syn', 'sys2_syn']):
        disp = PrecisionRecallDisplay(curves[system], np.arange(0.0, 1.1, 0.1))
        ax = axs[i]
        ax.set_ylim(0.0, 1.0)
        disp.plot(ax=ax)
    fig = plt.gcf()
    fig.set_size_inches(18.5, 4.0)
    plt.savefig(f'prc/{query}.pdf')