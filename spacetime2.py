import numpy as np
import matplotlib.pyplot as plt

def prime_axis(ax, upper_limit, slope):
    """Return an axis in the prime frame."""
    prime_axis_weight = 2.0

    return ax.plot([0,upper_limit],
                   [0,slope*upper_limit],
                   'k-', linewidth=prime_axis_weight)

def label_stat_axes(ax,tick_label=r'$D_0$'):
    """Label horiztontal and vertical ticks with multiples of a
    label."""
    new_ticks = [0, tick_label]
    nx = len(ax.get_xticklabels())
    for tick in range(2,nx):
        new_ticks.append(('%i' % tick)+tick_label)
    ax.set_xticklabels(new_ticks)

    ny = len(ax.get_yticklabels())
    if nx > ny:
        new_ticks = new_ticks[0:ny]
    elif nx < ny:
        for tick in range(nx, ny):
            new_ticks.append(('%i' % tick)+tick_label)
    ax.set_yticklabels(new_ticks)


def spacetime_diagram(fig, frame, upper_limit=10.0,
                      stationary_only=False, **kwd):
    """Draw a spacetime diagram in fig."""

    limits = (0,upper_limit)
    ax = fig.add_subplot(111, aspect=1, xlim=limits,
                         ylim=limits, **kwd)

    label_stat_axes(ax)

    if stationary_only:
        return
        
    const_pos_slope = 1/frame.beta
    line_of_simul_slope = frame.beta


    t_prime_axis = prime_axis(ax, upper_limit, const_pos_slope)
    x_prime_axis = prime_axis(ax, upper_limit, line_of_simul_slope)

    line_of_simul_locs = ax.get_yticks()/frame.gamma
    line_of_simul_locs=np.arange(1,np.int32(frame.gamma*len(ax.get_yticks())))*ax.get_yticks()[1]/frame.gamma
    negs_locs = -line_of_simul_locs
    
    for intercept in line_of_simul_locs.tolist() + negs_locs.tolist():
        line_of_simul = ax.plot([0,upper_limit],
                                [intercept,line_of_simul_slope*upper_limit+intercept],
                                'k:')
        b = -const_pos_slope*intercept
        line_of_pos = ax.plot([intercept,upper_limit],
                [0, const_pos_slope*upper_limit+b],
                'k--')

    ax.set_title('v/c=%f'% frame.beta)
    fig.legend((line_of_pos[0], line_of_simul[0]),(r'$x^\prime=$constant',r'$ct^\prime=$constant'))
    return ax
    
def make_spacetime(betas,save_format='png'):
    """"Make and save spacetime diagram for a list of beta values"""
    from frame import Frame

    fig = plt.figure(1)
    for beta in betas:
        frame = Frame(beta)
        fig.clf()
        ax = spacetime_diagram(fig, frame)
        ax.set_xlabel(r'$x$')
        ax.set_ylabel(r'$ct$')
        fig.savefig('spacetime_0-%i.%s' % (np.int32(1000*beta),save_format))
