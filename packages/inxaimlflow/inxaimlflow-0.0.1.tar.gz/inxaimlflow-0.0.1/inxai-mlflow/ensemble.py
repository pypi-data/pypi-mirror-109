import os

import mlflow
from matplotlib import pyplot as plt
from utils.scaling import minmax

from inxai import GlobalFeatureMetric
from stability import Stability
from consistency import Consistency
from accelerated_loss import AcceleratedLoss
from ensemble_exception import EnsembleException

import pandas as pd
import numpy as np
import seaborn as sns


class Ensemble:
    def __init__(self, stability: Stability, consistency: Consistency, acc_loss: AcceleratedLoss, cons_alpha=0.2,
                 lip_alpha=20, auc_alpha=0.1, perturber=None, perturber_strategy='mean', dissimilarity='euclidean',
                 confidence=None):
        self.stability = stability
        self.consistency = consistency
        self.acc_loss = acc_loss

        self.perturber = perturber
        self.perturber_strategy = perturber_strategy
        self.dissimilarity = dissimilarity
        self.confidence = confidence

        self.global_feature_metric = GlobalFeatureMetric()

        self.weights_df = cons_alpha * self.consistency.cons_df + lip_alpha * self.stability.lip_df + auc_alpha / self.acc_loss.auc_df

        self.r1 = self.weights_df['lime'] * pd.DataFrame(self.stability.res_lime_stab).T
        self.r2 = self.weights_df['shap'] * pd.DataFrame(self.stability.res_shap_stab).T

        self.ens_res = (self.r1 + self.r2) / self.weights_df.sum(axis=1)
        self.ens_res = minmax(pd.DataFrame(self.ens_res.T.values))

    def calculate_stability(self, X):
        if not self.stability.use_shap or not self.stability.use_lime:
            raise EnsembleException()

        ens_lips = self.global_feature_metric.stability(X, self.ens_res, epsilon=self.stability.epsilon,
                                                        perturber=self.perturber, perturber_strategy=self.perturber_strategy,
                                                        dissimilarity=self.dissimilarity, confidence=self.confidence)

        self.lip_df_fin = pd.DataFrame(
            {'lime': self.stability.lime_lips, 'shap': self.stability.shap_lips, 'ens': ens_lips})

        self.fig_stab, plot = plt.subplots()
        sns.boxplot(ax=plot, x="variable", y="value", data=pd.melt(self.lip_df_fin))
        self.fig_stab.tight_layout()

    def log_stability(self, name='ensemble_stability'):
        with mlflow.start_run(run_name=name, nested=True):
            png_file_name = f"{name}.png"
            mlflow.log_figure(self.fig_stab, png_file_name)

            csv_file_name = f'{name}.csv'
            self.lip_df_fin.to_csv(csv_file_name)
            mlflow.log_artifact(csv_file_name)
            os.remove(csv_file_name)

    def calculate_consistency(self):
        if not self.consistency.use_shap or not self.consistency.use_lime:
            raise EnsembleException()

        # Spytać co te dwie linijki robia
        src1 = pd.DataFrame(minmax(
            pd.DataFrame(self.consistency.res_shap_con[0]).apply(lambda x: x * self.weights_df['shap'], axis=0)))
        src2 = pd.DataFrame(minmax(
            pd.DataFrame(self.consistency.res_shap_con[1]).apply(lambda x: x * self.weights_df['shap'], axis=0)))

        lime_cons = self.global_feature_metric.consistency(self.consistency.res_lime_con, perturber=self.perturber,
                                                           perturber_strategy=self.perturber_strategy,
                                                           dissimilarity=self.dissimilarity, confidence=self.confidence)
        shap_cons = self.global_feature_metric.consistency(self.consistency.res_shap_con, perturber=self.perturber,
                                                           perturber_strategy=self.perturber_strategy,
                                                           dissimilarity=self.dissimilarity, confidence=self.confidence)
        shap_cons_ensemble = self.global_feature_metric.consistency([src1.values, src2.values], perturber=self.perturber,
                                                                    perturber_strategy=self.perturber_strategy,
                                                                    dissimilarity=self.dissimilarity, confidence=self.confidence)

        self.cons_df_ens = pd.DataFrame({'lime': lime_cons, 'shap': shap_cons, 'ensemble': shap_cons_ensemble})

        self.fig_cons, plot = plt.subplots()
        sns.boxplot(ax=plot, x="variable", y="value", data=pd.melt(self.cons_df_ens))
        self.fig_cons.tight_layout()

    def log_consistency(self, name='ensemble_consistency'):
        with mlflow.start_run(run_name=name, nested=True):
            png_file_name = f"{name}.png"
            mlflow.log_figure(self.fig_cons, png_file_name)

            csv_file_name = f'{name}.csv'
            self.cons_df_ens.to_csv(csv_file_name)
            mlflow.log_artifact(csv_file_name)
            os.remove(csv_file_name)

    def calculate_acc_loss(self, X, y):
        if not self.acc_loss.use_shap or not self.acc_loss.use_lime:
            raise EnsembleException()

        ens_res_global = pd.DataFrame(self.ens_res).mean()

        ens_loss_lime = self.global_feature_metric.gradual_perturbation(model=self.acc_loss.model, X=X, y=y,
                                                                        column_transformer=self.acc_loss.column_transformer,
                                                                        importances_orig=ens_res_global,
                                                                        resolution=self.acc_loss.resolution,
                                                                        count_per_step=self.acc_loss.count_per_step,
                                                                        plot=False)

        self.fig_acc_loss, plot = plt.subplots()
        plot.plot(np.linspace(0, 100, 50), ens_loss_lime)
        plot.plot(np.linspace(0, 100, 50), self.acc_loss.acc_loss_shap)
        plot.plot(np.linspace(0, 100, 50), self.acc_loss.acc_loss_lime)
        plot.set_xlabel('Percentile of perturbation range', fontsize=13)
        plot.set_ylabel('Loss of accuracy', fontsize=13)
        plot.legend(['Ensemble', 'Shap', 'Lime'])
        self.fig_acc_loss.tight_layout()

        self.accloss_ens_df = pd.DataFrame({'ensemble': [np.linspace(0, 100, 50), ens_loss_lime],
                                            'shap': [np.linspace(0, 100, 50), self.acc_loss.acc_loss_shap],
                                            'lime': [np.linspace(0, 100, 50), self.acc_loss.acc_loss_lime]})

    def log_acc_loss(self, name='ensemble_acc_loss'):
        with mlflow.start_run(run_name=name, nested=True):
            # mlflow.log_param("perturber", self.epsilon)
            mlflow.log_param("perturber_strategy", self.perturber_strategy)
            mlflow.log_param("dissimilarity", self.dissimilarity)
            # mlflow.log_param("confidence", self.epsilon)

            png_file_name = f"{name}.png"
            mlflow.log_figure(self.fig_acc_loss, png_file_name)

            csv_file_name = f'{name}.csv'
            self.accloss_ens_df.to_csv(csv_file_name)
            mlflow.log_artifact(csv_file_name)
            os.remove(csv_file_name)
