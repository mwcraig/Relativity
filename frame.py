from numpy import sqrt
from numpy import asarray 

class Frame(object):
    """Defines a Lorentz transform between reference frames."""
    def __init__(self, beta=0.0):
        """`beta` is velocity of moving frame as a fraction of c."""
        self.beta = beta
        
    @property
    def gamma(self):
        """The usual \gamma factor."""
        return 1/sqrt(1-self.beta**2)

    def _lorentz_transform(self, x, ct, to_moving=True):
        """Lorentz transform, with option to specify direction of
        transform.

        If `to_moving` is true `self.beta` is used as the velcoity for
        the transform. If `to_moving` is false `-self.beta` is used,
        which inverts the transform.
        """
        if to_moving:
            beta = self.beta
        else:
            beta = -self.beta

        x, ct = asarray(x), asarray(ct)
        x_prime = self.gamma*(x-beta*ct)
        ct_prime = self.gamma*(-beta*x + ct)
        return x_prime, ct_prime          
        
    def toMoving(self,x,ct):
        """Transform from stationary frame to moving.
        """
        return self._lorentz_transform(x, ct, to_moving=True)
        
    def fromMoving(self, x_prime, ct_prime):
        """Transform from moving frame to stationary."""
        return self._lorentz_transform(x_prime, ct_prime, to_moving=False)

    def spacetime_from(self, x_prime, ct_prime):
        x, ct = self.fromMoving(x_prime, ct_prime)
        return self.spacetime_scale*x, self.spacetime_scale*ct
        
    def spacetime_to(self, x, ct):
        x_prime, ct_prime = self.toMoving(x, ct)
        return self.spacetime_scale*x_prime, self.spacetime_scale*ct_prime