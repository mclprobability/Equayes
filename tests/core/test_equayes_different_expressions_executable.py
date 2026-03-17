import inspect
import unittest
from datetime import date

import numpy as np
import sympy as sp
import torch
from sympy.utilities.lambdify import lambdify

from equayes import Equayes
from equayes.utils import log
from tests.core.base_equayes_test import BaseEquayesTest

logger = log.getLogger("unittest_TestEquayesInferenceMethodsExecutable")


class TestEquayesDifferentExpressionsExecutable(BaseEquayesTest):

    def test_1d_single_input_no_param(self, inference_method_name="mcmc", kernel_name="nuts"):
        x0 = sp.Symbol("x0")
        output_dim = 1
        expr_sp = sp.sin(x0)
        expr_torch = lambdify([x0], expr_sp, modules="torch")

        n_predictive_samples = 200
        n_train, n_test = 10, 100
        x_train = torch.linspace(1, 10, n_train).view(-1, 1)
        y_train = expr_torch(x_train)
        x_test = torch.linspace(1, 10, n_test).view(-1, 1)
        y_test = expr_torch(x_test)

        self.exec_regression_inference(
            expr_sp,
            [x0],
            output_dim,
            inference_method_name,
            kernel_name,
            x_train,
            y_train,
            x_test,
            n_predictive_samples,
            expected_number_of_latent_variables=0,
        )

    def test_1d_no_input_single_param(self, inference_method_name="mcmc", kernel_name="nuts"):
        output_dim = 1
        # todo: evaluate=False is important, as the sinus is lost otherwise. Does SR return such constructs that we need to keep?
        expr_sp = sp.sin(2.0, evaluate=False)
        expr_torch = lambdify([], expr_sp, modules="torch")

        n_predictive_samples = 200
        n_train, n_test = 10, 100
        x_train = torch.linspace(1, 10, n_train).view(-1, 1)
        y_train = torch.tensor(np.sin(2.0)).expand((n_train, 1))
        x_test = torch.linspace(1, 10, n_test).view(-1, 1)
        y_test = torch.tensor(np.sin(2.0)).expand((n_test, 1))

        self.exec_modeling_inference(
            expr_sp,
            output_dim,
            inference_method_name,
            kernel_name,
            y_train,
            n_predictive_samples,
            expected_number_of_latent_variables=1,
        )

    def test_1d_single_input_single_param(self, inference_method_name="mcmc", kernel_name="nuts"):
        x0 = sp.Symbol("x0")
        output_dim = 1
        expr_sp = 2.0 * sp.sin(x0) + 1  # integers are not transformed to random variables
        expr_torch = lambdify([x0], expr_sp, modules="torch")

        n_predictive_samples = 200
        n_train, n_test = 10, 100
        x_train = torch.linspace(1, 10, n_train).view(-1, 1)
        y_train = expr_torch(x_train)
        x_test = torch.linspace(1, 10, n_test).view(-1, 1)
        y_test = expr_torch(x_test)

        self.exec_regression_inference(
            expr_sp,
            [x0],
            output_dim,
            inference_method_name,
            kernel_name,
            x_train,
            y_train,
            x_test,
            n_predictive_samples,
            expected_number_of_latent_variables=1,
        )

    def test_1d_multiple_inputs_multiple_params(self, inference_method_name="mcmc", kernel_name="nuts"):
        x0, x1 = sp.symbols("x0 x1")
        output_dim = 1
        expr_sp = 2.0 * sp.sin(x0) + 5.0 * sp.cos(x1**2)
        expr_torch = lambdify([x0, x1], expr_sp, modules="torch")

        n_predictive_samples = 200
        n_train, n_test = 10, 100
        x_train = torch.linspace(1, 10, n_train).view(-1, 1).expand((-1, 2))
        y_train = expr_torch(x_train[:, 0], x_train[:, 1]).view(-1, 1)
        x_test = torch.linspace(1, 10, n_test).view(-1, 1).expand((-1, 2))
        y_test = expr_torch(x_test[:, 0], x_test[:, 1])

        self.exec_regression_inference(
            expr_sp,
            [x0, x1],
            output_dim,
            inference_method_name,
            kernel_name,
            x_train,
            y_train,
            x_test,
            n_predictive_samples,
            expected_number_of_latent_variables=2,
        )
