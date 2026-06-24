import tempfile
import unittest

import sympy as sp
import torch
import xarray

from equayes import Equayes


class TestEquayesPersistence(unittest.TestCase):
    def test_persist_load_equayes_mcmc(self):
        test_dir = self.enterContext(tempfile.TemporaryDirectory("test"))
        test_file_name = test_dir + "inference_res.netcdf"
        x, y = torch.randn((10, 1)), torch.randn((10, 1))
        x_test = torch.randn((20, 1))
        x0 = sp.Symbol("x0")
        expr_sp = 2.0 * sp.sin(x0)

        equayes = Equayes(
            expr_sp,
            input_symbols=[x0],
            mcmc_warmup_samples=10,
            mcmc_samples=10,
        )
        equayes.fit(x, y)
        inference_dt = equayes.get_posterior()
        self.assertEqual(type(inference_dt), xarray.DataTree, "MCMC inference must return xarray.DataTree")
        # save and reload inference data
        inference_dt.to_netcdf(test_file_name)
        inference_dt_loaded = xarray.load_datatree(test_file_name)
        # initialize new equayes instance
        equayes_reloaded = Equayes(
            expr_sp,
            input_symbols=[x0],
            mcmc_warmup_samples=10,
            mcmc_samples=10,
        )
        equayes_reloaded.load_posterior_arviz(inference_dt_loaded)
        # verify that posterior samples are equal
        posterior_original = equayes.mcmc_.get_samples(group_by_chain=True)
        posterior_reloaded = equayes_reloaded.mcmc_.get_samples(group_by_chain=True)
        for k, v in posterior_original.items():
            self.assertTrue(torch.all(torch.abs(v - posterior_reloaded[k]) < 1e-6))

        # verify that predict() is working - no exception ==> everything is okay
        equayes_reloaded.predict(x_test, sample_prior=False)
        equayes_reloaded.predict(x_test, sample_prior=True)
