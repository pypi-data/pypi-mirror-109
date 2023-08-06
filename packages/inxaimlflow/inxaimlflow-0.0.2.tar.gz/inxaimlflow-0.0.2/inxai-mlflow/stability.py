import os

import mlflow
from matplotlib import pyplot as plt
from utils.scaling import minmax

from inxai import GlobalFeatureMetric, generate_per_instance_importances

import pandas as pd
import seaborn as sns


class Stability:
    def __init__(self, models, epsilon=.3, perturber=None, perturber_strategy='mean', dissimilarity='euclidean',
                 confidence=None, use_shap=True, use_lime=True):
        self.models = models
        self.global_feature_metric = GlobalFeatureMetric()
        self.epsilon = epsilon
        self.perturber = perturber
        self.perturber_strategy = perturber_strategy
        self.dissimilarity = dissimilarity
        self.confidence = confidence
        self.use_shap = use_shap
        self.use_lime = use_lime

    def calculate(self, X, y):
        if self.use_shap:
            self.res_shap_stab = generate_per_instance_importances(models=self.models, X=X, y=y, framework='kernel_shap')
            self.res_shap_stab = minmax(pd.DataFrame(self.res_shap_stab), scale=[-1, 1])
            self.shap_lips = self.global_feature_metric.stability(X, self.res_shap_stab,
                                                                  epsilon=self.epsilon, perturber=self.perturber,
                                                                  perturber_strategy=self.perturber_strategy,
                                                                  dissimilarity=self.dissimilarity,
                                                                  confidence=self.confidence)

        if self.use_lime:
            self.res_lime_stab = generate_per_instance_importances(models=self.models, X=X, y=y, framework='lime')
            self.res_lime_stab = minmax(pd.DataFrame(self.res_lime_stab), scale=[-1, 1])
            self.lime_lips = self.global_feature_metric.stability(X, self.res_lime_stab,
                                                                  epsilon=self.epsilon, perturber=self.perturber,
                                                                  perturber_strategy=self.perturber_strategy,
                                                                  dissimilarity=self.dissimilarity,
                                                                  confidence=self.confidence)

        if self.use_shap and self.use_lime:
            self.lip_df = pd.DataFrame({'lime': self.lime_lips, 'shap': self.shap_lips})
        elif self.use_shap:
            self.lip_df = pd.DataFrame({'shap': self.shap_lips})
        else:
            self.lip_df = pd.DataFrame({'lime': self.lime_lips})

        self.fig, plot = plt.subplots()
        sns.boxplot(ax=plot, x="variable", y="value", data=pd.melt(self.lip_df))
        self.fig.tight_layout()

    def log(self, name='stability'):
        with mlflow.start_run(run_name=name, nested=True):
            mlflow.log_param("epsilon", self.epsilon)
            # mlflow.log_param("perturber", self.epsilon)
            mlflow.log_param("perturber_strategy", self.perturber_strategy)
            mlflow.log_param("dissimilarity", self.dissimilarity)
            # mlflow.log_param("confidence", self.epsilon)

            png_file_name = f"{name}.png"
            mlflow.log_figure(self.fig, png_file_name)

            csv_file_name = f'{name}.csv'
            self.lip_df.to_csv(csv_file_name, index=False)
            mlflow.log_artifact(csv_file_name)
            os.remove(csv_file_name)
