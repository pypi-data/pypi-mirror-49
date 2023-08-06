import numpy as np

def sse(model, param_mask, observable_data, timespan):
    """Fitness function decorator for computing the negative sum of squared errors (sse)
    from model output.

    Args:
        position (numpy.array): The parameter vector the compute loglikelihood
            of.

    Returns:
        float: The natural logarithm of the likelihood estimate.

    """
    data = dict()
    data_mask = dict()
    for observable_key in observable_data.keys():
        data[observable_key] = observable_data[observable_key][0]
        data_mask[observable_key] = observable_data[observable_key][2]
        # print(observable_data[observable_key][2])
        if observable_data[observable_key][2] is None:
            data_mask[observable_key] = range(len(timespan))
    param_values = np.array([parm.value for parm in model.parameters])
    def wrap(run_model):
        def wrapped_f(theta):
            params = param_values.copy()
            params[param_mask] = 10**theta
            sim = run_model(model, params, timespan)
            sserr= 0.0
            for observable in observable_data.keys():
                sim_vals = sim[observable][data_mask[observable]]
                sserr -= np.sum((data[observable]-sim_vals)**2)
            if np.isnan(sserr):
                return -np.inf
            return sserr
        return wrapped_f
    return wrap

def sse_loglikelihood(self, position):
    """Compute the loglikelihood using the negative sum of squared errors estimator.

    Args:
        position (numpy.array): The parameter vector the compute loglikelihood
            of.

    Returns:
        float: The natural logarithm of the likelihood estimate.

    """
    Y = np.copy(position)
    params = self._param_values.copy()
    params[self._rate_mask] = 10**Y
    sim = self._model_solver.run(param_values=[params]).all
    logl = 0.0
    for observable in self._like_data.keys():
        sim_vals = sim[observable][self._data_mask[observable]]
        logl -= np.sum((self._data[observable]-sim_vals)**2)
    if np.isnan(logl):
        return -np.inf
    return logl
