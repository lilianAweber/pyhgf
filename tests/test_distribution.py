# Author: Nicolas Legrand <nicolas.legrand@cas.au.dk>

import unittest
from unittest import TestCase

import arviz as az
from pyhgf.binary import binary_surprise
import jax.numpy as jnp
import numpy as np
import pymc as pm
from jax import grad, jit
from jax.tree_util import Partial

from pyhgf import load_data
from pyhgf.distribution import HGFDistribution, HGFLogpGradOp, hgf_logp
from pyhgf.response import total_gaussian_surprise, total_binary_surprise


class TestDistribution(TestCase):

    def test_hgf_logp(self):

        ##################
        # Continuous HGF #
        ##################

        # Create the data (value and time vectors)
        timeserie = load_data("continuous")
        jax_logp = jit(
            Partial(
                hgf_logp,
                n_levels=2,
                input_data=[timeserie],
                response_function=total_gaussian_surprise,
                model_type="continuous",
                response_function_parameters=None,
                time=None
            )
        )

        logp = jax_logp(
            omega_1=-3.0,
            omega_2=-3.0,
            omega_3=jnp.nan,
            omega_input=np.log(1e-4),
            rho_1=0.0,
            rho_2=0.0,
            rho_3=jnp.nan,
            pi_1=1e4,
            pi_2=1e1,
            pi_3=jnp.nan,
            mu_1=timeserie[0],
            mu_2=0.0,
            mu_3=jnp.nan,
            kappa_1=1.0,
            kappa_2=jnp.nan,
        )
        assert jnp.isclose(logp, 1938.0101)

        ##############
        # Binary HGF #
        ##############

        # Create the data (value and time vectors)
        timeserie = load_data("binary")
        jax_logp = jit(
            Partial(
                hgf_logp,
                n_levels=2,
                input_data=[timeserie],
                response_function=total_binary_surprise,
                model_type="binary",
                response_function_parameters=None,
            )
        )

        logp = jax_logp(
            omega_1=jnp.inf,
            omega_2=jnp.array(-6.0),
            omega_3=jnp.nan,
            omega_input=jnp.inf,
            rho_1=jnp.array(0.0),
            rho_2=jnp.array(0.0),
            rho_3=jnp.nan,
            pi_1=jnp.array(0.0),
            pi_2=jnp.array(1e4),
            pi_3=jnp.nan,
            mu_1=jnp.inf,
            mu_2=jnp.array(0.5),
            mu_3=jnp.nan,
            kappa_1=jnp.array(1.0),
            kappa_2=jnp.nan,
        )
        assert jnp.isclose(logp, -215.11276)

    def test_grad_logp(self):

        ##################
        # Continuous HGF #
        ##################

        # Create the data (value and time vectors)
        timeserie = load_data("continuous")
        grad_logp = jit(
            grad(
                Partial(
                    hgf_logp,
                    n_levels=2,
                    input_data=[timeserie],
                    response_function=total_gaussian_surprise,
                    model_type="continuous",
                    response_function_parameters=None,
                ),
                argnums=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            ),
        )

        (
            omega_1,
            omega_2,
            omega_3,
            omega_input,
            rho_1,
            rho_2,
            rho_3,
            pi_1,
            pi_2,
            pi_3,
            mu_1,
            mu_2,
            mu_3,
            kappa_1,
            kappa_2,
        ) = grad_logp(
            np.array(-3.0),
            np.array(-3.0),
            np.array(0.0),
            np.log(1e-4),
            np.array(0.0),
            np.array(0.0),
            np.array(0.0),
            np.array(1e4),
            np.array(1e1),
            np.array(0.0),
            np.array(timeserie[0]),
            np.array(0.0),
            np.array(0.0),
            np.array(1.0),
            np.array(0.0),
        )

        assert jnp.isclose(omega_1, 0.47931308)

        ##############
        # Binary HGF #
        ##############

        # Create the data (value and time vectors)
        timeserie = load_data("binary")
        
        grad_logp = jit(
            grad(
                Partial(
                    hgf_logp,
                    n_levels=2,
                    input_data=[timeserie],
                    response_function=total_binary_surprise,
                    model_type="binary",
                    response_function_parameters=None,
                ),
                argnums=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            ),
        )

        (
            omega_1,
            omega_2,
            omega_3,
            omega_input,
            rho_1,
            rho_2,
            rho_3,
            pi_1,
            pi_2,
            pi_3,
            mu_1,
            mu_2,
            mu_3,
            kappa_1,
            kappa_2,
        ) = grad_logp(
                np.array(0.0),
                np.array(-2.0),
                np.array(0.0),
                np.array(0.0),
                np.array(0.0),
                np.array(0.0),
                np.array(0.0),
                np.array(0.0),
                np.array(1e4),
                np.array(0.0),
                np.array(0.0),
                np.array(0.5),
                np.array(0.0),
                np.array(1.0),
                np.array(1.0),
        )

        assert jnp.isclose(omega_2, -3.3864107)

    def test_aesara_logp(self):
        """Test the aesara hgf_logp op."""

        ##################
        # Continuous HGF #
        ##################

        # Create the data (value and time vectors)
        timeserie = load_data("continuous")

        hgf_logp_op = HGFDistribution(
            input_data=[timeserie],
            model_type="continuous",
            n_levels=2,
            response_function=total_gaussian_surprise,
            response_function_parameters=None,
        )

        logp = hgf_logp_op(
            omega_1=np.array(-3.0),
            omega_2=np.array(-3.0),
            omega_3=np.array(0.0),
            omega_input=np.log(1e-4),
            rho_1=np.array(0.0),
            rho_2=np.array(0.0),
            rho_3=np.array(0.0),
            pi_1=np.array(1e4),
            pi_2=np.array(1e1),
            pi_3=np.array(0.0),
            mu_1=np.array(timeserie[0]),
            mu_2=np.array(0.0),
            mu_3=np.array(0.0),
            kappa_1=np.array(1.0),
            kappa_2=np.array(0.0),
        ).eval()

        assert jnp.isclose(logp, 1938.01013184)

        ##############
        # Binary HGF #
        ##############

        # Create the data (value and time vectors)
        timeserie = load_data("binary")

        hgf_logp_op = HGFDistribution(
            input_data=[timeserie],
            model_type="binary",
            n_levels=2,
            response_function=total_binary_surprise,
            response_function_parameters=None,
        )

        logp = hgf_logp_op(
            omega_1=np.inf,
            omega_2=-6.0,
            omega_3=np.inf,
            omega_input=np.inf,
            rho_1=0.0,
            rho_2=0.0,
            rho_3=np.inf,
            pi_1=0.0,
            pi_2=1e4,
            pi_3=np.inf,
            mu_1=np.inf,
            mu_2=0.5,
            mu_3=np.inf,
            kappa_1=1.0,
            kappa_2=np.inf,
        ).eval()

        assert jnp.isclose(logp, -215.11276245)

    def test_aesara_grad_logp(self):
        """Test the aesara gradient hgf_logp op."""

        ##################
        # Continuous HGF #
        ##################

        # Create the data (value and time vectors)
        timeserie = load_data("continuous")

        hgf_logp_grad_op = HGFLogpGradOp(
            model_type="continuous",
            input_data=[timeserie],
            n_levels=2,
            response_function=total_gaussian_surprise,
            response_function_parameters=None,
        )

        omega_1 = hgf_logp_grad_op(
            omega_1=-3.0,
            omega_2=-3.0,
            omega_input=np.log(1e-4),
            rho_1=0.0,
            rho_2=0.0,
            pi_1=1e4,
            pi_2=1e1,
            mu_1=timeserie[0],
            mu_2=0.0,
            kappa_1=1.0,
        )[0].eval()

        assert jnp.isclose(omega_1, 0.47931308)
        
        
        ##############
        # Binary HGF #
        ##############

        # Create the data (value and time vectors)
        timeserie = load_data("binary")

        hgf_logp_grad_op = HGFLogpGradOp(
            model_type="binary",
            input_data=[timeserie],
            n_levels=2,
            response_function=total_binary_surprise,
            response_function_parameters=None,
        )

        omega_2 = hgf_logp_grad_op(
            omega_1=np.inf,
            omega_2=-6.0,
            omega_input=np.inf,
            rho_1=0.0,
            rho_2=0.0,
            pi_1=0.0,
            pi_2=1e4,
            mu_1=np.inf,
            mu_2=0.5,
            kappa_1=1.0,
        )[1].eval()

        assert jnp.isclose(omega_2, 2.6229846)

    def test_pymc_sampling(self):
        """Test the aesara hgf_logp op."""

        ##############
        # Continuous #
        ##############

        # Create the data (value and time vectors)
        timeserie = load_data("continuous")

        hgf_logp_op = HGFDistribution(
            n_levels=2,
            input_data=[timeserie],
            response_function=total_gaussian_surprise,
            response_function_parameters=(np.array(1), 1),
        )

        with pm.Model() as model:

            omega_2 = pm.Normal("omega_2", -11.0, 2)

            pm.Potential(
                "hhgf_loglike",
                hgf_logp_op(
                    omega_1=np.array(0.0),
                    omega_2=omega_2,
                    omega_input=np.log(1e-4),
                    rho_1=np.array(0.0),
                    rho_2=np.array(0.0),
                    pi_1=np.array(1e4),
                    pi_2=np.array(1e1),
                    mu_1=np.array(timeserie[0]),
                    mu_2=np.array(0.0),
                    kappa_1=np.array(1.0),
                    omega_3=np.nan,
                    rho_3=np.nan,
                    pi_3=np.nan,
                    mu_3=np.nan,
                    kappa_2=np.nan,
                ),
            )

        initial_point = model.initial_point()

        pointslogs = model.point_logps(initial_point)
        assert pointslogs["omega_2"] == -1.61
        assert pointslogs["hhgf_loglike"] == 2149.04

        with model:
            idata = pm.sample(chains=4, cores=4, tune=1000)

        assert -14 < round(az.summary(idata)["mean"].values[0]) < -10
        assert az.summary(idata)["r_hat"].values[0] == 1

        ##########
        # Binary #
        ##########

        # Create the data (value and time vectors)
        timeserie = load_data("binary")

        hgf_logp_op = HGFDistribution(
            n_levels=2,
            model_type="binary",
            input_data=[timeserie],
            response_function=total_binary_surprise,
            response_function_parameters=(np.array(1), 1),
        )

        with pm.Model() as model:

            omega_2 = pm.Normal("omega_2", -11.0, 2)

            pm.Potential(
                "hhgf_loglike",
                hgf_logp_op(
                    omega_1=np.inf,
                    omega_2=omega_2,
                    omega_input=np.inf,
                    rho_1=0.0,
                    rho_2=0.0,
                    pi_1=0.0,
                    pi_2=1e4,
                    mu_1=np.inf,
                    mu_2=0.5,
                    kappa_1=1.0,
                    omega_3=np.nan,
                    rho_3=np.nan,
                    pi_3=np.nan,
                    mu_3=np.nan,
                    kappa_2=np.nan,
                ),
            )

        initial_point = model.initial_point()

        pointslogs = model.point_logps(initial_point)
        assert pointslogs["omega_2"] == -1.61
        assert pointslogs["hhgf_loglike"] == -230.72

        with model:
            idata = pm.sample(chains=4, cores=4, tune=1000)

        assert -4 < round(az.summary(idata)["mean"].values[0]) < -2
        assert az.summary(idata)["r_hat"].values[0] <= 1.01

if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
