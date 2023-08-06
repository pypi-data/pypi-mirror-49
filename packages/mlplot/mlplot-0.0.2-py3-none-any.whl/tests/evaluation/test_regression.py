"""Test for mlplot model evaluation classification class"""
import pytest

from .. import np, output_ax
from mlplot.evaluation import RegressionEvaluation
from mlplot.errors import InvalidArgument

@pytest.fixture
def reg_eval():
    """Setup an example RegressionEvaluation"""
    y_true = np.random.normal(size=10000)
    y_pred = np.random.normal(0.25, 0.3, size=y_true.shape) + y_true

    model_eval = RegressionEvaluation(
        y_true=y_true,
        y_pred=y_pred,
        value_name='variable',
        model_name='foo',
    )
    return model_eval

def test_repr(reg_eval):
    """Check the string representation"""
    assert str(reg_eval) == 'RegressionEvaluation(model_name=foo)'
    assert repr(reg_eval) == 'RegressionEvaluation(model_name=foo)'

def test_mse_score(reg_eval):
    assert round(reg_eval.mse_score(), 2) == 0.15

def test_mae_score(reg_eval):
    assert round(reg_eval.mae_score(), 2) == 0.32

def test_r2_score(reg_eval):
    assert round(reg_eval.r2_score(), 2) == 0.85

def test_explained_variance_score(reg_eval):
    assert round(reg_eval.explained_variance_score(), 2) == 0.91

def test_scatter(reg_eval, output_ax):
    reg_eval.scatter(ax=output_ax)

def test_residuals(reg_eval, output_ax):
    reg_eval.residuals(ax=output_ax)

def test_residuals_histogram(reg_eval, output_ax):
    reg_eval.residuals_histogram(ax=output_ax)

def test_report_table(reg_eval, output_ax):
    reg_eval.report_table(ax=output_ax)
