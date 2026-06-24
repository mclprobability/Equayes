import sympy as sp
import torch
from sympy.utilities.lambdify import lambdify

from equayes.utils import log
from tests.core.base_equayes_test import BaseEquayesTest

logger = log.getLogger("unittest_TestEquayesInferenceAlgosExecutable")

from parameterized import parameterized


class TestEquayesInferenceAlgosExecutable(BaseEquayesTest):

    @parameterized.expand(BaseEquayesTest.INF_METHOD_AND_KERNEL_NAMES)
    def test_inference_methods_executable(self, inference_method_name, kernel_name):
        x0, lat0 = sp.symbols("x0 lat0")
        output_dim = 1
        expr_sp_regression = 2.0 * lat0 * sp.sin(x0)
        expr_sp_modeling = 2.0 * lat0 * sp.sin(5.0, evaluate=False)
        expr_torch = lambdify([x0], expr_sp_regression, modules="torch")

        n_predictive_samples = 200
        n_train, n_test = 10, 100
        x_train = torch.linspace(1, 10, n_train).view(-1, 1)
        y_train = torch.randn((n_train, 1))
        x_test = torch.linspace(1, 10, n_test).view(-1, 1)
        y_test = torch.randn((n_test, 1))

        self.exec_regression_inference(
            expr_sp_regression,
            [x0],
            [lat0],
            output_dim,
            inference_method_name,
            kernel_name,
            x_train,
            y_train,
            x_test,
            n_predictive_samples,
            expected_number_of_latent_variables=2,
        )
        self.exec_modeling_inference(
            expr_sp_modeling,
            [lat0],
            output_dim,
            inference_method_name,
            kernel_name,
            y_train,
            n_predictive_samples,
            expected_number_of_latent_variables=3,
        )
