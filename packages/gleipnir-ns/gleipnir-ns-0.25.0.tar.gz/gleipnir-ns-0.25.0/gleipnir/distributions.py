from abc import ABC, abstractmethod

class ContinuousDistBase(ABC):
    """Base abstract class for custom continuous distribution objects.
    """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def pdf(self, value):
        """Return the probability distribution function (pdf) at value.
        """
        pass

    @abstractmethod
    def logpdf(self, value):
        """Return the log of  the probability distribution function (pdf) at value.
        """

        pass

    @abstractmethod
    def cdf(self, value):
        """Return the cumulative distribution function (cdf) at value (integrated
        from the lower boundary of the distribution's support).
        """
        pass

    @abstractmethod
    def ppf(self, value):
        """Return the percent point function (ppf) (i.e., inverse of cdf) at value.
        Value is from [0:1].
        """
        pass

    @abstractmethod
    def rvs(self, shape):
        """Return a random variate sample (rvs) from the distribution with size
        given by shape.
        """
        pass

class DiscreteDistBase(ABC):
    """Base abstract class for custom discrete distribution objects.
    """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def pmf(self, value):
        """Return the probability distribution function (pdf) at value.
        """
        pass

    @abstractmethod
    def logpmf(self, value):
        """Return the log of  the probability distribution function (pdf) at value.
        """

        pass

    @abstractmethod
    def cdf(self, value):
        """Return the cumulative distribution function (cdf) at value (integrated
        from the lower boundary of the distribution's support).
        """
        pass

    @abstractmethod
    def ppf(self, value):
        """Return the percent point function (ppf) (i.e., inverse of cdf) at value.
        Value is from [0:1].
        """
        pass

    @abstractmethod
    def rvs(self, shape):
        """Return a random variate sample (rvs) from the distribution with size
        given by shape.
        """
        pass
