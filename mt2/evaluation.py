# SETUP
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import pandas as pd

metrics = {}
def metric(f): return metrics.setdefault(f.__name__, f)


@metric
def ap(results, relevant):
    """Average Precision"""
    precision_values = [
        len([
            val
            for val in results[:idx]
            if val in relevant
        ]) / idx
        for idx in range(1, len(results))
    ]
    return sum(precision_values)/len(precision_values) if precision_values else 0


@metric
def p10(results, relevant, n=10):
    """Precision at N"""
    return len([val for val in results[:n] if val in relevant])/n


# Define metrics to be calculated
evaluation_metrics = {
    'ap': 'Average Precision',
    'p10': 'Precision at 10 (P@10)'
}


class EvaluateQuery:

    def __init__(self, results, relevant):
        self.results = results
        self.relevant = relevant
        print(results, relevant)

    def calculate_metric(self, key):
        return metrics[key](self.results, self.relevant)

    def export_metrics(self, filepath):
        # Calculate all metrics and export results as LaTeX table
        df = pd.DataFrame([['Metric', 'Value']] +
                          [
            [evaluation_metrics[m], self.calculate_metric(m)]
            for m in evaluation_metrics
        ]
        )

        with open(f'{filepath}/results.tex', 'w+') as tf:
            tf.write(df.to_latex())

    def export_ap(self, filepath):
        ap = self.calculate_metric('ap')
        with open(f'{filepath}/ap.txt', 'w+') as tf:
            tf.write(str(ap))

    def plot_precision_recall(self, name, ax):
        # PRECISION-RECALL CURVE
        # Calculate precision and recall values as we move down the ranked list

        if not self.results:
            return

        precision_values = [
            len([
                val
                for val in self.results[:idx]
                if val in self.relevant
            ]) / idx
            for idx, _ in enumerate(self.results, start=1)
        ]

        recall_values = [
            len([
                val for val in self.results[:idx]
                if val in self.relevant
            ]) / len(self.relevant)
            for idx, _ in enumerate(self.results, start=1)
        ]

        precision_recall_match = {k: v for k,
                                  v in zip(recall_values, precision_values)}

        # Extend recall_values to include traditional steps for a better curve (0.1, 0.2 ...)
        recall_values.extend([step for step in np.arange(
            0.1, 1.1, 0.1) if step not in recall_values])
        recall_values = sorted(set(recall_values))

        # Extend matching dict to include these new intermediate steps
        for idx, step in enumerate(recall_values):
            if step not in precision_recall_match:
                if recall_values[idx-1] in precision_recall_match:
                    precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
                else:
                    precision_recall_match[step] = precision_recall_match[recall_values[idx+1]]

        disp = PrecisionRecallDisplay(
            [precision_recall_match.get(r) for r in recall_values], recall_values)
        disp.plot(ax=ax, name="Micro-average precision-recall", color="red", linewidth=1, linestyle=":",)
        #plt.savefig(f'{filepath}/precision_recall.pdf')
