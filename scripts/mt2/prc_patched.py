from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

for query in [f'q{i}' for i in range(1,5)]:
    curves = pd.read_csv(f'prc/{query}_prc.csv')
    for system in ['sys1', 'sys2', 'sys1_syn', 'sys2_syn']:
        disp = PrecisionRecallDisplay(curves[system], np.arange(0.0, 1.1, 0.1))
        ax = plt.gca()
        plt.ylim((0.0,1.0))
        disp.plot(ax=ax)
        plt.savefig(f'prc/{query}/{system}.pdf')
        ax.clear()