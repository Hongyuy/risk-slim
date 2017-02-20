import numpy as np

def log_loss_value(Z, rho):
    #compute the slope of the logistic loss function in a way that is numerically stable
    #loss_value: (1 x 1) scalar = 1/n_rows * sum(log( 1 .+ exp(-Z*rho))
    #see also: http://stackoverflow.com/questions/20085768/
    #compute loss value
    scores = Z.dot(rho)
    pos_idx = scores > 0
    loss_value = np.empty_like(scores)
    loss_value[pos_idx] = np.log1p(np.exp(-scores[pos_idx]))
    loss_value[~pos_idx] = -scores[~pos_idx] + np.log1p(np.exp(scores[~pos_idx]))
    loss_value = loss_value.mean()
    return loss_value

def log_loss_value_and_slope(Z, rho):
    #compute the value and slope of the logistic loss function in a way that is numerically stable
    #loss_value: (1 x 1) scalar = 1/n_rows * sum(log( 1 .+ exp(-Z*rho))
    #loss_slope: (n_cols x 1) vector = 1/n_rows * sum(-Z*rho ./ (1+exp(-Z*rho))
    #see also: http://stackoverflow.com/questions/20085768/
    scores = Z.dot(rho)
    pos_idx = scores > 0
    exp_scores_pos = np.exp(-scores[pos_idx])
    exp_scores_neg = np.exp(scores[~pos_idx])

    #compute loss value
    loss_value = np.empty_like(scores)
    loss_value[pos_idx] = np.log1p(exp_scores_pos)
    loss_value[~pos_idx] = -scores[~pos_idx] + np.log1p(exp_scores_neg)
    loss_value = loss_value.mean()

    #compute loss slope
    log_probs = np.empty_like(scores)
    log_probs[pos_idx]  = 1.0 / (1.0 + exp_scores_pos)
    log_probs[~pos_idx] = exp_scores_neg / (1.0 + exp_scores_neg)
    loss_slope = Z.T.dot(log_probs - 1.0) / Z.shape[0]

    return loss_value, loss_slope

def log_loss_value_from_scores(scores):
    #compute the value and slope of the logistic loss function in a way that is numerically stable
    #loss_value: (1 x 1) scalar = 1/n_rows * sum(log( 1 .+ exp(-Z*rho))
    #loss_slope: (n_cols x 1) vector = 1/n_rows * sum(-Z*rho ./ (1+exp(-Z*rho))
    #see also: http://stackoverflow.com/questions/20085768/
    pos_idx = scores > 0
    loss_value = np.empty_like(scores)
    loss_value[pos_idx] = np.log1p(np.exp(-scores[pos_idx]))
    loss_value[~pos_idx] = -scores[~pos_idx] + np.log1p(np.exp(scores[~pos_idx]))
    loss_value = loss_value.mean()
    return loss_value

def log_probs(Z, rho):
    #compute the probabilities of the logistic loss function in a way that is numerically stable
    scores = Z.dot(rho)
    pos_idx = scores > 0
    log_probs = np.empty_like(scores)
    log_probs[pos_idx]  = 1.0 / (1.0 + np.exp(-scores[pos_idx]))
    log_probs[~pos_idx] = np.exp(scores[~pos_idx]) / (1.0 + np.exp(scores[~pos_idx]))
    return log_probs
