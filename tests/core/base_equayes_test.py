import unittest

from equayes import Equayes


class BaseEquayesTest(unittest.TestCase):

    INFERENCE_METHOD_NAMES = ("mcmc", "vi")
    KERNEL_NAMES = ("nuts", "random_walk")

    INF_METHOD_AND_KERNEL_NAMES = [("mcmc", kernel_name) for kernel_name in KERNEL_NAMES] + [("vi", "")]

    def exec_regression_inference(
        self,
        expr_sp,
        input_symbols,
        output_dim,
        inference_method_name,
        kernel_name,
        x_train,
        y_train,
        x_test,
        n_predictive_samples,
        expected_number_of_latent_variables,
    ):
        equayes = Equayes(
            expr_sp,
            input_symbols,
            output_dim=output_dim,
            inference_method_name=inference_method_name,
            kernel_name=kernel_name,
            mcmc_samples=10,
            mcmc_warmup_samples=10,
            vi_iter=10,
            jit_compile=False,
        )
        self.assertEqual(
            len(equayes._exp_param_values),
            expected_number_of_latent_variables,
            f"Equayes transformed {len(equayes._exp_param_values)} parameters to latent variables but expected {expected_number_of_latent_variables}"
            + f"\n latent vars: "
            + str([f"{k}, {v}" for (k, v) in equayes._exp_param_values.items()]),
        )

        equayes.fit(x_train, y_train)
        equayes.inference_diagnostics()
        y_pred = equayes.predict(x_test, n_predictive_samples=n_predictive_samples)

        self.assertEqual(
            (y_pred["mu"].shape[0], *y_pred["mu"].shape[-2:]),
            (n_predictive_samples, x_test.shape[0], output_dim),
            "Shape of prediction must match",
        )
        self.assertEqual(
            (y_pred["obs"].shape[0], *y_pred["obs"].shape[-2:]),
            (n_predictive_samples, x_test.shape[0], output_dim),
            "Shape of prediction must match",
        )

    def exec_modeling_inference(
        self,
        expr_sp,
        output_dim,
        inference_method_name,
        kernel_name,
        y_train,
        n_predictive_samples,
        expected_number_of_latent_variables,
    ):
        equayes = Equayes(
            expr_sp,
            [],
            output_dim=output_dim,
            inference_method_name=inference_method_name,
            kernel_name=kernel_name,
            mcmc_samples=10,
            mcmc_warmup_samples=10,
            vi_iter=10,
            jit_compile=False,
        )
        self.assertEqual(
            len(equayes._exp_param_values),
            expected_number_of_latent_variables,
            f"Equayes transformed {len(equayes._exp_param_values)} parameters to latent variables but expected {expected_number_of_latent_variables}"
            + f"\n latent vars: "
            + str([f"{k}, {v}" for (k, v) in equayes._exp_param_values.items()]),
        )
        equayes.fit(None, y_train)
        equayes.inference_diagnostics()
        y_pred = equayes.predict(None, n_predictive_samples=n_predictive_samples)

        self.assertEqual(
            (y_pred["mu"].shape[0], *y_pred["mu"].shape[-2:]),
            (n_predictive_samples, 1, output_dim),
            "Shape of prediction must match",
        )
        self.assertEqual(
            (y_pred["obs"].shape[0], *y_pred["obs"].shape[-2:]),
            (n_predictive_samples, 1, output_dim),
            "Shape of prediction must match",
        )
