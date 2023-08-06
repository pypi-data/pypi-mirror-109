import os

import mlflow
from sklearn.compose import ColumnTransformer
from sklearn.metrics import auc

from inxai import *


class AcceleratedLoss:
    def __init__(self, model, shap_explainer, lime_explainer, count_per_step=10, resolution=50, use_shap=True, use_lime=True):
        self.model = model
        self.global_feature_metric = GlobalFeatureMetric()
        self.shap_explainer = shap_explainer
        self.lime_explainer = lime_explainer
        self.count_per_step = count_per_step
        self.resolution = resolution
        self.use_shap = use_shap
        self.use_lime = use_lime
        self.shap_res_global = None
        self.lime_res_global = None
        self.column_transformer = None
        self.acc_loss_shap = None
        self.acc_loss_lime = None
        self.auc_df = None
        self.fig = None

    def _explain_instance(self, row):
        e = self.lime_explainer.explain_instance(row, self.model.predict_proba, num_features=len(row)).as_list()
        return [i[1] for i in e]

    def calculate(self, X, y):
        self.column_transformer = ColumnTransformer(
            [('_INXAI_normal_noise_perturber', NormalNoisePerturber(scale=2), X.columns)])

        if self.use_shap:
            shap_res_instance = self.shap_explainer.shap_values(X)
            self.shap_res_global = pd.DataFrame(shap_res_instance[0]).apply(abs).mean()

            self.acc_loss_shap = self.global_feature_metric.gradual_perturbation(model=self.model, X=X, y=y,
                                                                                 column_transformer=self.column_transformer,
                                                                                 importances_orig=self.shap_res_global,
                                                                                 resolution=self.resolution,
                                                                                 count_per_step=self.count_per_step,
                                                                                 plot=False)

        if self.use_lime:
            self.lime_res_global = X.apply(lambda x: self._explain_instance(x), axis=1, result_type='expand').apply(
                abs).mean()

            self.acc_loss_lime = self.global_feature_metric.gradual_perturbation(model=self.model, X=X, y=y,
                                                                             column_transformer=self.column_transformer,
                                                                             importances_orig=self.lime_res_global,
                                                                             resolution=self.resolution,
                                                                             count_per_step=self.count_per_step,
                                                                             plot=False)

        self.fig, plot = plt.subplots()
        plot.set_xlabel('Percentile of perturbation range', fontsize=13)
        plot.set_ylabel('Loss of accuracy', fontsize=13)

        if self.use_shap and self.use_lime:
            self.auc_df = pd.DataFrame({'lime': [auc(np.linspace(0, 1, 50), self.acc_loss_lime)],
                                        'shap': [auc(np.linspace(0, 1, 50), self.acc_loss_shap)]})

            self.fig.legend(['Shap (AUCx = ' + str(auc(np.linspace(0, 1, 50), self.acc_loss_shap)) + ')',
                             'Lime (AUCx = ' + str(auc(np.linspace(0, 1, 50), self.acc_loss_lime)) + ')'])
        elif self.use_shap:
            self.auc_df = pd.DataFrame({'shap': [auc(np.linspace(0, 1, 50), self.acc_loss_shap)]})
            plot.plot(np.linspace(0, 100, 50), self.acc_loss_shap)

        else:
            self.auc_df = pd.DataFrame({'lime': [auc(np.linspace(0, 1, 50), self.acc_loss_lime)]})
            plot.plot(np.linspace(0, 100, 50), self.acc_loss_lime)

        self.fig.tight_layout()

    def log(self, name='acc_loss'):
        with mlflow.start_run(run_name=name, nested=True):
            png_file_name = f"{name}.png"
            mlflow.log_figure(self.fig, png_file_name)

            csv_file_name = f'{name}.csv'
            self.auc_df.to_csv(csv_file_name, index=False)
            mlflow.log_artifact(csv_file_name)
            os.remove(csv_file_name)
