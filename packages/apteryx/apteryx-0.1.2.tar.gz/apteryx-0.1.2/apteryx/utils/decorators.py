import numpy as np

def fail_with_prob(prob, log=False):
    def decorator_wrapper(function):
        def wrapper(*args, **kwargs):
            try:
                p = np.random.choice(np.linspace(0,1,1001))
                assert p > prob
                return function(*args, **kwargs)
            except:
                if log:
                    print(f'Failed (p = {round(p,3)}, thresh = {prob})')
                raise ValueError()
        return wrapper
    return decorator_wrapper