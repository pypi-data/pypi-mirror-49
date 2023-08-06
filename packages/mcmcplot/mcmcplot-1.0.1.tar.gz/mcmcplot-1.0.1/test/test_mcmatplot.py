#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 12:21:24 2018

@author: prmiles
"""

from mcmcplot import mcmatplot as MP
import matplotlib.pyplot as plt
import numpy as np
import math
import unittest


# --------------------------
class PlotDensityPanel(unittest.TestCase):
    def test_basic_plot_features(self):
        npar = 3
        chains = np.random.random_sample(size=(100, npar))
        f = MP.plot_density_panel(chains=chains)
        for ii in range(npar):
            name = str('$p_{{{}}}$'.format(ii))
            self.assertEqual(f.axes[ii].get_xlabel(), name,
                             msg=str('Should be {}'.format(name)))
            self.assertEqual(f.axes[ii].get_ylabel(),
                             str('$\\pi$({}$|M^{}$)'.format(name, '{data}')),
                             msg='Should be posterior')
        self.assertEqual(f.get_figwidth(), 5.0, msg='Width is 5in')
        self.assertEqual(f.get_figheight(), 4.0, msg='Height is 4in')
        plt.close()
        f, settings = MP.plot_density_panel(chains=chains, return_settings=True)
        self.assertTrue(isinstance(settings, dict),
                        msg='Expect dict return')
        plt.close()

    def test_basic_plot_features_with_hist_on(self):
        npar = 3
        chains = np.random.random_sample(size=(100, npar))
        settings = {'hist_on': True}
        f = MP.plot_density_panel(chains=chains, settings=settings)
        for ii in range(npar):
            name = str('$p_{{{}}}$'.format(ii))
            self.assertEqual(f.axes[ii].get_xlabel(), name,
                             msg=str('Should be {}'.format(name)))
            self.assertEqual(f.axes[ii].get_ylabel(),
                             str('$\\pi$({}$|M^{}$)'.format(name, '{data}')),
                             msg='Should be posterior')
        self.assertEqual(f.get_figwidth(), 5.0, msg='Width is 5in')
        self.assertEqual(f.get_figheight(), 4.0, msg='Height is 4in')
        plt.close()
        f, kde = MP.plot_density_panel(
                chains=chains, settings=settings,
                return_kde=True)
        for ii in range(npar):
            name = str('$p_{{{}}}$'.format(ii))
            self.assertEqual(f.axes[ii].get_xlabel(), name,
                             msg=str('Should be {}'.format(name)))
            self.assertEqual(f.axes[ii].get_ylabel(),
                             str('$\\pi$({}$|M^{}$)'.format(name, '{data}')),
                             msg='Should be posterior')
        self.assertEqual(f.get_figwidth(), 5.0, msg='Width is 5in')
        self.assertEqual(f.get_figheight(), 4.0, msg='Height is 4in')
        plt.close()
        self.assertEqual(len(kde), 3,
                        msg='Expect 3 kde functions')


# --------------------------
class PlotChainPanel(unittest.TestCase):
    def test_basic_plot_features_nsimu_lt_maxpoints(self):
        chains = np.random.random_sample(size=(100, 2))
        f = MP.plot_chain_panel(chains=chains)
        x1, y1 = f.axes[0].lines[0].get_xydata().T
        x2, y2 = f.axes[1].lines[0].get_xydata().T
        self.assertTrue(np.array_equal(y1, chains[:, 0]),
                        msg='Expect y1 to match column 1')
        self.assertTrue(np.array_equal(y2, chains[:, 1]),
                        msg='Expect y2 to match column 2')
        self.assertEqual(f.axes[0].get_xlabel(), '', msg='Should be blank')
        self.assertEqual(f.axes[1].get_xlabel(), 'Iteration',
                         msg='Should be Iteration')
        plt.close()

    def test_basic_plot_features_nsimu_gt_maxpoints(self):
        nsimu = 1000
        chains = np.random.random_sample(size=(nsimu, 2))
        f = MP.plot_chain_panel(chains=chains)
        x1, y1 = f.axes[0].lines[0].get_xydata().T
        x2, y2 = f.axes[1].lines[0].get_xydata().T
        skip = int(math.floor(nsimu/500))
        self.assertTrue(np.array_equal(y1, chains[range(0, nsimu, skip), 0]),
                        msg='Expect y1 to match column 1')
        self.assertTrue(np.array_equal(y2, chains[range(0, nsimu, skip), 1]),
                        msg='Expect y2 to match column 2')
        self.assertEqual(f.axes[0].get_xlabel(), '', msg='Should be blank')
        self.assertEqual(f.axes[1].get_xlabel(), 'Iteration',
                         msg='Should be Iteration')
        plt.close()

    def test_basic_plot_features_nsimu_gt_maxpoints_with_pm2std(self):
        nsimu = 1000
        chains = np.random.random_sample(size=(nsimu, 2))
        f = MP.plot_chain_panel(chains=chains,
                                   settings=dict(add_pm2std=True))
        x1, y1 = f.axes[0].lines[0].get_xydata().T
        x2, y2 = f.axes[1].lines[0].get_xydata().T
        skip = int(math.floor(nsimu/500))
        self.assertTrue(np.array_equal(y1, chains[range(0, nsimu, skip), 0]),
                        msg='Expect y1 to match column 1')
        self.assertTrue(np.array_equal(y2, chains[range(0, nsimu, skip), 1]),
                        msg='Expect y2 to match column 2')
        self.assertEqual(f.axes[0].get_xlabel(), '',
                         msg='Should be blank')
        self.assertEqual(f.axes[1].get_xlabel(), 'Iteration',
                         msg='Should be Iteration')
        self.assertEqual(len(f.axes[0].lines), 4,
                         msg='Expect 4 lines')
        self.assertEqual(len(f.axes[1].lines), 4,
                         msg='Expect 4 lines')
        plt.close()
        f, settings = MP.plot_chain_panel(
                chains=chains, return_settings=True,
                settings=dict(add_pm2std=True))
        self.assertTrue(isinstance(settings, dict),
                        msg='Expect dict return')
        plt.close()


# --------------------------
class PlotHistogramPanel(unittest.TestCase):
    def test_basic_plot_features_nsimu_lt_maxpoints(self):
        npar = 3
        chains = np.random.random_sample(size=(100, npar))
        f = MP.plot_histogram_panel(chains=chains)
        for ii in range(npar):
            self.assertEqual(f.axes[ii].get_xlabel(),
                             str('$p_{{{}}}$'.format(ii)),
                             msg=str('Should be $p_{{{}}}$'.format(ii)))
            self.assertEqual(f.axes[ii].get_ylabel(), '',
                             msg='Should be blank')
        plt.close()
        f, settings = MP.plot_histogram_panel(chains=chains, return_settings=True)
        self.assertTrue(isinstance(settings, dict),
                        msg='Expect dict return')
        plt.close()


# --------------------------
class PlotPairwiseCorrelationPanel(unittest.TestCase):

    def test_basic_plot_features_nsimu_lt_maxpoints(self):
        chains = np.random.random_sample(size=(100, 3))
        f = MP.plot_pairwise_correlation_panel(chains=chains)
        x1, y1 = f.axes[0].lines[0].get_xydata().T
        x2, y2 = f.axes[1].lines[0].get_xydata().T
        x3, y3 = f.axes[1].lines[0].get_xydata().T
        self.assertTrue(np.array_equal(x1, chains[:, 0]),
                        msg='Expect x1 to match column 0')
        self.assertTrue(np.array_equal(y1, chains[:, 1]),
                        msg='Expect y1 to match column 1')
        self.assertTrue(np.array_equal(x2, chains[:, 0]),
                        msg='Expect x2 to match column 0')
        self.assertTrue(np.array_equal(y2, chains[:, 2]),
                        msg='Expect y2 to match column 2')
        self.assertTrue(np.array_equal(x3, chains[:, 0]),
                        msg='Expect x3 to match column 1')
        self.assertTrue(np.array_equal(y3, chains[:, 2]),
                        msg='Expect y3 to match column 2')
        for ai in f.axes:
            self.assertEqual(ai.get_xlabel(), '', msg='Should be blank')
        self.assertEqual(f.axes[0].get_title(), '$p_{0}$',
                         msg='Expect $p_{0}$')
        self.assertEqual(f.axes[2].get_title(), '$p_{1}$',
                         msg='Expect $p_{1}$')
        self.assertEqual(f.axes[0].get_ylabel(), '$p_{1}$',
                         msg='Expect $p_{1}$')
        self.assertEqual(f.axes[1].get_ylabel(), '$p_{2}$',
                         msg='Expect $p_{2}$')
        plt.close()

    def test_basic_plot_features_nsimu_lt_maxpoints_and_2_chains(self):
        chains = np.random.random_sample(size=(100, 2))
        f = MP.plot_pairwise_correlation_panel(chains=chains)
        x1, y1 = f.axes[0].lines[0].get_xydata().T
        self.assertTrue(np.array_equal(x1, chains[:, 0]),
                        msg='Expect x1 to match column 0')
        self.assertTrue(np.array_equal(y1, chains[:, 1]),
                        msg='Expect y1 to match column 1')
        for ai in f.axes:
            self.assertEqual(ai.get_title(), '', msg='Should be blank')
        self.assertEqual(f.axes[0].get_xlabel(), '$p_{0}$',
                         msg='Expect $p_{0}$')
        self.assertEqual(f.axes[0].get_ylabel(), '$p_{1}$',
                         msg='Expect $p_{1}$')
        plt.close()

    def test_basic_plot_features_2c_w_contours(self):
        chains = np.random.random_sample(size=(100, 2))
        f = MP.plot_pairwise_correlation_panel(
                chains=chains, settings=dict(add_5095_contours=True))
        x1, y1 = f.axes[0].lines[0].get_xydata().T
        self.assertTrue(np.array_equal(x1, chains[:, 0]),
                        msg='Expect x1 to match column 0')
        self.assertTrue(np.array_equal(y1, chains[:, 1]),
                        msg='Expect y1 to match column 1')
        self.assertEqual(len(f.axes[0].lines), 3, msg='Expect 3 lines')
        for ai in f.axes:
            self.assertEqual(ai.get_title(), '', msg='Should be blank')
        self.assertEqual(f.axes[0].get_xlabel(), '$p_{0}$',
                         msg='Expect $p_{0}$')
        self.assertEqual(f.axes[0].get_ylabel(), '$p_{1}$',
                         msg='Expect $p_{1}$')
        plt.close()

    def test_basic_plot_features_2c_w_contours_and_legend(self):
        chains = np.random.random_sample(size=(100, 2))
        f = MP.plot_pairwise_correlation_panel(
                chains=chains,
                settings=dict(add_5095_contours=True, add_legend=True))
        x1, y1 = f.axes[0].lines[0].get_xydata().T
        self.assertTrue(np.array_equal(x1, chains[:, 0]),
                        msg='Expect x1 to match column 0')
        self.assertTrue(np.array_equal(y1, chains[:, 1]),
                        msg='Expect y1 to match column 1')
        self.assertEqual(len(f.axes[0].lines), 3, msg='Expect 3 lines')
        self.assertEqual(len(f.legends), 1, msg='Expect legend')
        plt.close()


# --------------------------
class PlotChainMetrics(unittest.TestCase):

    def test_basic_plot_features(self):
        chains = np.random.random_sample(size=(100, 1))
        f = MP.plot_chain_metrics(chain=chains, name=['a1'])
        x1, y1 = f.axes[0].lines[0].get_xydata().T
        self.assertTrue(np.array_equal(y1, chains[:, 0]),
                        msg='Expect y1 to match column 1')
        self.assertEqual(f.axes[0].get_xlabel(), 'Iterations',
                         msg='Should be Iterations')
        self.assertEqual(f.axes[0].get_ylabel(), 'a1-chain',
                         msg='Should be a1-chain')
        self.assertEqual(f.axes[1].get_xlabel(), 'a1',
                         msg='Strings should match')
        self.assertEqual(f.axes[1].get_ylabel(),
                         'Histogram of a1-chain',
                         msg='Strings should match')
        self.assertEqual(f.get_figwidth(), 7.0, msg='Width is 7in')
        self.assertEqual(f.get_figheight(), 5.0, msg='Height is 5in')
        plt.close()

    def test_figsize_plot_features(self):
        chains = np.random.random_sample(size=(100, 1))
        f = MP.plot_chain_metrics(chain=chains, name=['a1'],
                                     settings={'fig': dict(figsize=(10, 2))})
        x1, y1 = f.axes[0].lines[0].get_xydata().T
        self.assertTrue(np.array_equal(y1, chains[:, 0]),
                        msg='Expect y1 to match column 1')
        self.assertEqual(f.axes[0].get_xlabel(), 'Iterations',
                         msg='Should be Iterations')
        self.assertEqual(f.axes[0].get_ylabel(), 'a1-chain',
                         msg='Should be a1-chain')
        self.assertEqual(f.axes[1].get_xlabel(), 'a1',
                         msg='Strings should match')
        self.assertEqual(f.axes[1].get_ylabel(),
                         'Histogram of a1-chain',
                         msg='Strings should match')
        self.assertEqual(f.get_figwidth(), 10.0, msg='Width is 10in')
        self.assertEqual(f.get_figheight(), 2.0, msg='Height is 2in')
        plt.close()
        f, settings = MP.plot_chain_metrics(
                chain=chains, name=['a1'],
                settings={'fig': dict(figsize=(10, 2))},
                return_settings=True)
        self.assertTrue(isinstance(settings, dict),
                        msg='Expect dict return')
        plt.close()
