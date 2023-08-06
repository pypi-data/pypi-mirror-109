import os

import mlflow
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

from inxai import GlobalFeatureMetric, generate_per_instance_importances
from utils.scaling import minmax


class Consistency:
    def __init__(self, models, perturber=None, perturber_strategy='mean', dissimilarity='euclidean', confidence=None,
                 use_shap=True, use_lime=True):
        self.models = models
        self.global_feature_metric = GlobalFeatureMetric()
        self.perturber = perturber
        self.perturber_strategy = perturber_strategy
        self.dissimilarity = dissimilarity
        self.confidence = confidence
        self.use_shap = use_shap
        self.use_lime = use_lime

    def calculate(self, X, y):
        if self.use_shap:
            self.res_shap_con = generate_per_instance_importances(models=self.models, X=X, y=y, framework='kernel_shap')
            self.res_shap_con = [minmax(pd.DataFrame(rsc), scale=[-1, 1]) for rsc in self.res_shap_con]

            self.shap_cons = self.global_feature_metric.consistency(self.res_shap_con, perturber=self.perturber,
                                                                    perturber_strategy=self.perturber_strategy,
                                                                    dissimilarity=self.dissimilarity, confidence=self.confidence)

        if self.use_lime:
            self.res_lime_con = generate_per_instance_importances(models=self.models, X=X, y=y, framework='lime')
            self.res_lime_con = [minmax(pd.DataFrame(rlc), scale=[-1, 1]) for rlc in self.res_lime_con]
            self.lime_cons = self.global_feature_metric.consistency(self.res_lime_con, perturber=self.perturber,
                                                                    perturber_strategy=self.perturber_strategy,
                                                                    dissimilarity=self.dissimilarity, confidence=self.confidence)

        if self.use_shap and self.use_lime:
            self.cons_df = pd.DataFrame({'lime': self.lime_cons, 'shap': self.shap_cons})
        elif self.use_shap:
            self.cons_df = pd.DataFrame({'shap': self.shap_cons})
        else:
            self.cons_df = pd.DataFrame({'lime': self.lime_cons})

        self.fig, plot = plt.subplots()
        sns.boxplot(ax=plot, x="variable", y="value", data=pd.melt(self.cons_df))
        self.fig.tight_layout()

    def log(self, name='consistency'):
        with mlflow.start_run(run_name=name, nested=True):
            # mlflow.log_param("perturber", self.epsilon)
            mlflow.log_param("perturber_strategy", self.perturber_strategy)
            mlflow.log_param("dissimilarity", self.dissimilarity)
            # mlflow.log_param("confidence", self.epsilon)

            png_file_name = f"{name}.png"
            mlflow.log_figure(self.fig, png_file_name)

            csv_file_name = f'{name}.csv'
            self.cons_df.to_csv(csv_file_name, index=False)
            mlflow.log_artifact(csv_file_name)
            os.remove(csv_file_name)
