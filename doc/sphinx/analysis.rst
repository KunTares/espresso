.. _Analysis:

Analysis
========

has two fundamentally different classes of observables for analyzing the
systems. On the one hand, some observables are computed from the Tcl
level. In that case, the observable is measured in the moment that the
corresponding Tcl function is called, and the results are returned to
the Tcl script. In general, observables in this class should only be
computed after a large number of timesteps, as switching forth and back
between the C- and the Tcl-level is costly. This chapter describes all
observables in this class.

On the other hand, some observables are computed and stored in the
C-core of during a call to the function , while they are set up and
their results are collected from the Tcl level. These observables are
more complex to implement and offer less flexibility, while the are
significantly faster and more memory efficient, and they can be set up
to be computed every few timesteps. The observables in this class are
described in chapter [chap:analysis-core].

The class of Tcl-level analysis functions is mainly controlled via the
command. It has two main uses: Calculation of observables () and
definition and analysis of topologies in the system (). In addition,
offers the command (see section [sec:uwerr] for computing statistical
errors in time series.


.. _Available observables:

Available observables
---------------------

The command provides online-calculation of local and global observables.


.. _Minimal distances between particles:

Minimal distances between particles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[analyze:distto]

analyze mindist analyze distto analyze distto

Variant returns the minimal distance between two particles in the
system. If the type-lists are given, then the minimal distance between
particles of only those types is determined.

returns the minimal distance of all particles to particle (variant ), or
to the coordinates (, , ) (Variant ).


.. _Particles in the neighbourhood:

Particles in the neighbourhood
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

analyze nbhood analyze nbhood

Returns a Tcl-list of the particle ids of all particles within a given
radius around the position of the particle with number in variant or
around the spatial coordinate (, , ) in variant .

.. _Particle distribution:

Particle distribution
~~~~~~~~~~~~~~~~~~~~~

analyze distribution

Returns its parameters and the distance distribution of particles
(probability of finding a particle of type at a certain distance around
a particle of type , disregarding the fact that a spherical shell of a
larger radius covers a larger volume) with types specified in around
particles with types specified in with distances between and , binned
into bins. The bins are either equidistant (if
:math:`\var{log\_flag} = 0`) or logarithmically equidistant (if
:math:`\var{log\_flag} \geq 1`). If an integrated distribution is
required, use :math:`\var{int\_flag}=1`. The distance is defined as the
*minimal* distance between a particle of one group to any of the other
group.

The output corresponds to the blockfile format (see section ):

{ } { { } }


.. _Radial density map:

Radial density map
~~~~~~~~~~~~~~~~~~

analyze radial\_density\_map

Returns the radial density of particles around a given axis. Parameters
are:

-  histogram bins in x direction.

-  histogram bins in y direction.

-  range for analysis in x direction.

-  range for analysis in y direction.

-  rotate around given axis. (x, y, or z)

-  rotate around given point.

-  only analyze beads of given types.

-  histogram bins in angle theta.

This command does not do what you might expect. Here is an overview of
the currently identified properties.

#. is the number of bins along the axis of rotation.

#. is the number of bins in the radial direction.

#. The centre point () of the cylinder is located in the lower cap,
   i.e., is the height of the cylinder with respect to this centre
   point.

#. The bins are distributed along starting from 0 ().

#. The seem to average with respect to the centre of mass of the
   particles in the individual bins rather than with respect to the
   central axis, which one would think is natural.


.. _Cylndrical average:

Cylindrical Average
~~~~~~~~~~~~~~~~~~~

analyze cylindrical\_average

The command returns a list of lists. The outer list contains all data
combined whereas each inner list contains one line. Each lines stores a
different combination of the radial and axial index. The output might
look something like this

::

    { { 0 0 0.05 -0.25 0.0314159 0 0 0 0 0 0 }
      { 0 1 0.05 0.25 0.0314159 31.831 1.41421 1 0 0 0 }
      ... }

In this case two different particle types were present. The columns of
the respective lines are coded like this

output index\_radial index\_axial pos\_radial pos\_axial binvolume
density v\_radial v\_axial density v\_radial v\_axial 0 0 0.05 -0.25
0.0314159 0 0 0 0 0 0 0 1 0.05 0.25 0.0314159 31.831 1.41421 1 0 0 0

As one can see the columns , , and appear twice. The order of appearance
corresponds two the order of the types in the argument . For example if
was set to ``{0 1}`` then the first triple is associated to type 0 and
the second triple to type 1.

After knowing what the output looks like we might want to have more
information on how to input data.

-  is a double list containing the coordinates of the centre point of
   the cylinder.

-  is a double list containing a (not necessarily normalised) vector.

-  is the total length of the cylinder.

-  is the radius of the cylinder.

-  is the number of bins along the vector.

-  is the number of bins in radial direction.

-  is an int list of the type IDs.

Because all of this text is super abstract we additionally drew a
picture of what these variables actually mean, see
figure [fig:cylindricalaverage].

[dot/.style=draw,fill,circle,inner sep=1pt,rotate=-100] in .5, 1, 1.5, 2
in -, 0, (0,) ellipse ( and .5\*); (-,-) – (-,); (+,-) – (+,); (0,0)
node[dot,label=above:center] – (0,1.5) node[above] direction; in 0, (2,)
– (2,-); (2,-) – node[blue,below,rotate=-8] bins\_axial (2,); in .5, 1,
1.5, 2 (,-) – (-.5,-); (2,-) – node[red,above,rotate=80] bins\_radial
(0,-);

(0,) – node[right] radius (2,); (-2,-) – node[above] length (-2,);


.. _Modes:

Modes
~~~~~

analyze modes2d

Analyzes the modes of a configuration. Requires that a grid is set and
that the system contains more than two particles. Output are four
numbers in the order:

.. math:: ht_{RE}\qquad ht_{IM}\qquad \theta_{RE}\qquad \theta_{IM}


.. _Lipid orientation:

Lipid orientation
~~~~~~~~~~~~~~~~~

analyze get\_lipid\_orients analyze lipid\_orient\_order


.. _Bilayers:

Bilayers
~~~~~~~~

analyze bilayer\_set analyze bilayer\_density\_profile


.. _GPB:

GPB
~~~

analyze cell\_gpb


.. _Get folded positions:

Get folded positions
~~~~~~~~~~~~~~~~~~~~

analyze get\_folded\_positions

Outputs the folded positions of particles. Without any parameters, the
positions of all particles are given, folded to the box length. The
optional parameter ensures that molecules (particle groups) are kept
intact. The optional shift parameters can be used to shift the not
separated molecules if needed.


.. _Vkappa:

Vkappa
~~~~~~

analyze Vkappa

Calculates the compressibility :math:`V \times \kappa_T` through the
Volume fluctuations
:math:`V \times \kappa_T = \beta \left(\langle V^2\rangle - \langle V \rangle^2\right)`
:cite:`kolb99a`. Given no arguments this function calculates
and returns the current value of the running average for the volume
fluctuations. The argument clears the currently stored values. With the
cumulative mean volume, cumulative mean squared volume and how many
samples were used can be retrieved. Likewise the option enables you to
set those.


.. _Radial distribution function:

Radial distribution function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[analyze:<rdf>]

analyze

Returns its parameters and the radial distribution function (rdf) of
particles with types specified in around particles with types specified
in . The range is given by and and is divided into equidistant bins.

The output corresponds to the blockfile format (see section ):

{ } { { } }

.. _Structure factor:

Structure factor
~~~~~~~~~~~~~~~~

analyze structurefactor

Returns the spherically averaged structure factor :math:`S(q)` of
particles specified in . :math:`S(q)` is calculated for all possible
wave vectors, :math:`\frac{2\pi}{L} <= q <= \frac{2\pi}{L}\var{order}`.
Do not choose parameter too large, because the number of calculations
grows as :math:`\var{order}^3`.

The output corresponds to the blockfile format (see section ):

{ }


.. _Van-Hove autocorrelation function:

Van-Hove autocorrelation function :math:`G(r,t)`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

analyze vanhove

Returns the van Hove auto correlation function :math:`G(r,t)` and the
mean square displacement :math:`msd(t)` for particles of type for the
configurations stored in the array configs. This tool assumes that the
configurations stored with (see section ) are stored at equidistant time
intervals. :math:`G(r,t)` is calculated for each multiple of this time
intervals. For each time t the distribution of particle displacements is
calculated according to the specification given by , and . Optional
argument defines the maximum value of :math:`t` for which :math:`G(r,t)`
is calculated. If it is omitted or set to zero, maximum possible value
is used. If the particles perform a random walk (a normal diffusion
process) :math:`G(r,t)/r^2` is a Gaussian distribution for all times.
Deviations of this behavior hint on another diffusion process or on the
fact that your system has not reached the diffusive regime. In this case
it is also very questionable to calculate a diffusion constant from the
mean square displacement via the Stokes-Einstein relation.

The output corresponds to the blockfile format (see section ):

{ msd { …} } { vanhove { { …} { …} } }

The :math:`G(r,t)` are normalized such that the integral over space
always yields :math:`1`.


.. _Center of mass:

Center of mass
~~~~~~~~~~~~~~

analyze centermass

Returns the center of mass of particles of the given type.


.. _Moment of inertia matrix:

Moment of inertia matrix
~~~~~~~~~~~~~~~~~~~~~~~~

[analyze:find-principal-axis]

analyze momentofinertiamatrix analyze find\_principal\_axis

Variant returns the moment of inertia matrix for particles of given type
. The output is a list of all the elements of the 3x3 matrix. Variant
returns the eigenvalues and eigenvectors of the matrix.


.. _Gyration tensor:

Gyration tensor
~~~~~~~~~~~~~~~

analyze gyration\_tensor

Analyze the gyration tensor of particles of a given type , or of all
particles in the system if no type is given. Returns a Tcl-list
containing the squared radius of gyration, three shape descriptors
(asphericity, acylindricity, and relative shape anisotropy), eigenvalues
of the gyration tensor and their corresponding eigenvectors. The
eigenvalues are sorted in descending order.


.. _Aggregation:

Aggregation
~~~~~~~~~~~

analyze aggregation

Returns the aggregate size distribution for the molecules in the
molecule id range to . If any monomers in two different molecules are
closer than they are considered to be in the same aggregate. One can use
the optional parameter to specify a minimum number of contacts such that
only molecules having at least contacts will be considered to be in the
same aggregate. The second optional parameter enables one to consider
aggregation state of only oppositely charged particles.


.. _Identifying pearl necklace structures:

Identifying pearl-necklace structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

analyze necklace

Algorithm for identifying pearl necklace structures for polyelectrolytes
in poor solvent :cite:`limbach03a`. The first three
parameters are tuning parameters for the algorithm: is the minimal
number of monomers in a pearl. is the number of monomers along the chain
backbone which are excluded from the space distance criterion to form
clusters. is the distance between two monomers up to which they are
considered to belong to the same clusters. The three parameters may be
connected by scaling arguments. Make sure that your results are only
weakly dependent on the exact choice of your parameters. For the
algorithm the coordinates stored in partCfg are used. The chain itself
is defined by the identity first of its first monomer and the chain
length length. Attention: This function is very specific to the problem
and might not give useful results for other cases with similar
structures.


.. _Finding holes:

Finding holes
~~~~~~~~~~~~~

analyze holes

Function for the calculation of the unoccupied volume (often also called
free volume) in a system. Details can be found in
:cite:`schmitz00a`. It identifies free space in the
simulation box via a mesh based cluster algorithm. Free space is defined
via a probe particle and its interactions with other particles which
have to be defined through LJ interactions with the other existing
particle types via the inter command before calling this routine. A
point of the mesh is counted as free space if the distance of the point
is larger than LJ\_cut+LJ\_offset to any particle as defined by the LJ
interaction parameters between the probe particle type and other
particle types.How to use this function: Define interactions between all
(or the ones you are interested in) particle types in your system and a
fictitious particle type. Practically one uses the van der Waals radius
of the particles plus the size of the probe you want to use as the
Lennard Jones cutoff. The mesh spacing is the box length divided by the
.

{ { } { } { } }

A hole is defined as a continuous cluster of mesh elements that belong
to the unoccupied volume. Since the function is quite rudimentary it
gives back the whole information suitable for further processing on the
script level. and are given in number of mesh points, which means you
have to calculate the actual size via the corresponding volume or
surface elements yourself. The complete information is given in the
element\_lists for each hole. The element numbers give the position of a
mesh point in the linear representation of the 3D grid (coordinates are
in the order x, y, z). Attention: the algorithm assumes a cubic box.
Surface results have not been tested. .


.. _Temperature of the lb fluid:

Temperature of the LB fluid
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This command returns the temperature of the lattice-Boltzmann (LB)
fluid, see Chapter [sec:lb], by averaging over the fluid nodes. In case
or are compiled in and boundaries are defined, only the available fluid
volume is taken into account.


.. _Momentum of the system:

Momentum of the System
~~~~~~~~~~~~~~~~~~~~~~

analyze momentum

This command returns the total linear momentum of the particles and the
lattice-Boltzmann (LB) fluid, if one exists. Giving the optional
parameters either causes the command to ignore the contribution of LB or
of the particles.


.. _Energies:

Energies
~~~~~~~~

analyze energy analyze energy analyze energy bonded analyze energy
nonbonded

Returns the energies of the system. Variant returns all the
contributions to the total energy. Variant returns the numerical value
of the total energy or its kinetic or Coulomb or magnetic contributions
only. Variants and return the energy contributions of the bonded resp.
non-bonded interactions.

{ energy } { kinetic } { interaction } …


.. _Pressure:

Pressure
~~~~~~~~

analyze pressure analyze pressure total analyze pressure analyze
pressure bonded analyze pressure nonbonded analyze pressure
nonbonded\_intra analyze pressure nonbonded\_inter

Computes the pressure and its contributions in the system. Variant
returns all the contributions to the total pressure. Variant will return
the total pressure only. Variants , and return the corresponding
contributions to the total pressure.

The pressure is calculated (if there are no electrostatic interactions)
by

.. math::

   \label{eq:ptens}
     p = \frac{2E_{kinetic}}{Vf} + \frac{\sum_{j>i} {F_{ij}r_{ij}}}{3V}

where :math:`f=3` is the number of translational degrees of freedom of
each particle, :math:`V` is the volume of the system,
:math:`E_{kinetic}` is the kinetic energy, :math:`F_{ij}` the force
between particles i and j, and :math:`r_{ij}` is the distance between
them. The kinetic energy divided by the degrees of freedom is

.. math:: \frac{2E_{kinetic}}{f} = \frac{1}{3}\sum_{i} {m_{i}v_{i}^{2}}.

Note that Equation [eq:ptens] can only be applied to pair potentials and
central forces. Description of how contributions from other interactions
are calculated is beyond the scope of this manual. Three body potentials
are implemented following the procedure in
Ref. :cite:`thompson09a`. A different formula is used to
calculate contribution from electrostatic interactions in P3M. For
electrostatic interactions, the :math:`k`-space contribution is not well
tested, so use with caution! Anything outside that is currently not
implemented. Four-body dihedral potentials are not included. In case of
rigid body rotation, virial contribution from torques is not included.
The pressure contribution for rigid bodies constructed by means of the
VIRTUAL\_SITES\_RELATIVE mechanism is included. On the other hand, the
pressure contribution for rigid bonds is not included. All other
constraints of any kind are not currently accounted for in the pressure
calculations. The pressure is no longer correct, e.g., when particles
are confined to a plane.

The command is implemented in parallel.

{ { pressure } { ideal } { { } } { { } } { coulomb } }

specifying the pressure, the ideal gas pressure, the contributions from
bonded interactions, the contributions from non-bonded interactions and
the electrostatic contributions.


.. _Stress Tensor:

Stress Tensor
~~~~~~~~~~~~~

analyze stress\_tensor analyze stress\_tensor total analyze
stress\_tensor analyze stress\_tensor bonded analyze stress\_tensor
nonbonded analyze stress\_tensor nonbonded\_intra analyze stress\_tensor
nonbonded\_inter

Computes the stress tensor of the system. The various options are
equivalent to those described by in . It is called a stress tensor but
the sign convention follows that of a pressure tensor.

The stress tensor is calculated by

.. math:: p^{(kl)} = \frac{\sum_{i} {m_{i}v_{i}^{(k)}v_{i}^{(l)}}}{V} + \frac{\sum_{j>i}{F_{ij}^{(k)}r_{ij}^{(l)}}}{V}

where the notation is the same as for in and the superscripts :math:`k`
and :math:`l` correspond to the components in the tensors and vectors.

Note that the angular velocities of the particles are not included in
the calculation of the stress tensor.

The command is implemented in parallel.

{ { pressure } { ideal } { { } } { { } } { coulomb } }

specifying the pressure tensor, the ideal gas pressure tensor, the
contributions from bonded interactions, the contributions from
non-bonded interactions and the electrostatic contributions.


.. _Local Stress Tensor:

Local Stress Tensor
~~~~~~~~~~~~~~~~~~~

analyze local\_stress\_tensor

Computes local stress tensors in the system. A cuboid is defined
starting at the coordinate (,,) and going to the coordinate (+, +, +).
This cuboid in divided into bins in the x direction, bins in the y
direction and bins in the z direction such that the total number of bins
is \*\*. For each of these bins a stress tensor is calculated using the
Irving Kirkwood method. That is, a given interaction contributes towards
the stress tensor in a bin proportional to the fraction of the line
connecting the two particles that is within the bin.

If the P3M and MMM1D electrostatic methods are used, these interactions
are not included in the local stress tensor. The DH and RF methods, in
contrast, are included. Concerning bonded interactions only two body
interactions (FENE, Harmonic) are included (angular and dihedral are
not). For all electrostatic interactions only the real space part is
included.

Care should be taken when using constraints of any kind, since these are
not accounted for in the local stress tensor calculations.

The command is implemented in parallel.

{ { LocalStressTensor } { { } { } } }

specifying the local pressure tensor in each bin.


.. _Configurational temperature:

Configurational temperature
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Estimates the temperature using the potential energy, instead of the
kinetic energy (i.e., “kinetic temperature”). The configurational
temperature has been shown a more stringent criterion to reproduce a
canonical ensemble in certain cases
:cite:`allen06,bereau15`. The configurational temperature,
:math:`T_\textrm{conf}`, is estimated using first and second derivatives
of the potential energy of the system

.. math::

   \label{eq:configtemp}
     \frac{1}{k_\textrm{B}T_\textrm{conf}} = - \frac{\langle \sum_i \nabla_i \cdot
       \mathbf{F}_i \rangle}{\langle \sum_j F_j^2 \rangle},

where :math:`F_i` is the force exerted on particle :math:`i`, and
angular brackets denote canonical averages. Just like the conventional
kinetic temperature, the configurational temperature can be estimated
from a subsystem, e.g., a subset of particles in the box. To activate
the calculation of the configurational temperature for particle
:math:`i`, use

part i configtemp 1

The command will return a list of two terms: the instantaneous values of
the (:math:`i`) denominator and (:math:`ii`) numerator of the expression
in Equation [eq:configtemp]. Due to the reliance on second derivatives
of the potential energy (i.e., first derivative of the force), a limited
set of interaction potentials have so far been implemented.


.. _Analyzing groups of particles:

Analyzing groups of particles (molecules)
-----------------------------------------

[analyze:set]

analyze set chains analyze set topo\_part\_sync analyze set

The above set of functions is designed to facilitate analysis of
molecules. Molecules are expected to be a group of particles comprising
a contiguous range of particle IDs. Each molecule is a set of
consecutively numbered particles and all molecules are supposed to
consist of the same number of particles. Some functions in this group
require that the particles constituting a molecule are connected into
linear chains (particle :math:`n` is connected to :math:`n+1` and so on)
while others are applicable to molecules of whatever topology.

The command defines the structure of the current system to be used with
some of the analysis functions.

Variant defines a set of chains of equal length which start with the
particle with particle number and are consecutively numbered (the last
particle in that topology has number :math:`\var{chain\_start} +
\var{n\_chains}*\var{chain\_length} - 1`).

Variant synchronizes topology and particle data, assigning values to
particles.

Variant will return the chains currently stored.


.. _Chains:

Chains
~~~~~~

All analysis functions in this section require the topology of the
chains to be set correctly. The topology can be provided upon calling.
This (re-)sets the structure info permanently, it is only required once.


.. _End to end distance:

End-to-end distance
^^^^^^^^^^^^^^^^^^^

analyze

Returns the quadratic end-to-end-distance and its root averaged over all
chains. If is used, the distance is averaged over all stored
configurations (see section ).

{ }


.. _Radius of gyration:

Radius of gyration
^^^^^^^^^^^^^^^^^^

analyze

Returns the radius of gyration averaged over all chains. It is a radius
of a sphere, which would have the same moment of inertia as the
molecule, defined as

.. math::

   \label{eq:Rg}
   R_{\mathrm G}^2 = \frac{1}{N} \sum\limits_{i=1}^{N} \left(\vec r_i - \vec r_{\mathrm{cm}}\right)^2\,,

where :math:`\vec r_i` are position vectors of individual particles
constituting a molecule and :math:`\vec r_{\mathrm{cm}}` is the position
vector of its centre of mass. The sum runs over all :math:`N` particles
comprising the molecule. For more information see any polymer science
book, e.g. :cite:`rubinstein03a`. If is used, the radius of
gyration is averaged over all stored configurations (see section ).

{ }


.. _Hydrodynamic radius:

Hydrodynamic radius
^^^^^^^^^^^^^^^^^^^

analyze

Returns the hydrodynamic radius averaged over all chains. If is used,
the hydrodynamic radius is averaged over all stored configurations (see
section ). The following formula is used for the computation:

.. math::

   \label{eq:Rh}
   \frac{1}{R_{\mathrm H}} = \frac{2}{N^2} \sum\limits_{i=1}^{N} \sum\limits_{j=i}^{N} \frac{1}{|\vec r_i - \vec r_j|}\,,

The above-mentioned formula is only valid under certain assumptions. For
more information, see Chapter 4 and equation 4.102
in :cite:`doi86a`.

{ }


.. _Internal distances:

Internal distances
^^^^^^^^^^^^^^^^^^

analyze

Returns the averaged internal distances within the chains (over all
pairs of particles). If is used, the values are averaged over all stored
configurations (see section ).

{ … }

The index corresponds to the number of beads between the two monomers
considered (0 = next neighbours, 1 = one monomer in between, …).


.. _Internal distances II (specific monomer):

Internal distances II (specific monomer)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

analyze

In contrast to , it does not average over the whole chain, but rather
takes the chain monomer at position (default: :math:`0`, the first
monomer on the chain) to be the reference point to which all internal
distances are calculated. If is used, the values will be averaged over
all stored configurations (see section ).

{ … }


.. _Bond lengths:

Bond lengths
^^^^^^^^^^^^

analyze

Analyzes the bond lengths of the chains in the system. Returns its
average, the standard deviation, the maximum and the minimum. If you
want to look only at specific chains, use the optional arguments,
:math:`\var{chain\_start} =
2*\var{MPC}` and :math:`\var{n\_chains} = 1` to only include the third
chain’s monomers. If is used, the value will be averaged over all stored
configurations (see section ). This function assumes linear chain
topology and does not check if the bonds really exist!

{ }


.. _Form factor:

Form factor
^^^^^^^^^^^

| analyze

Computes the spherically averaged form factor of a single chain, which
is defined by

.. math::

   S(q) = \frac{1}{\var{chain\_length}} \sum_{i,j=1}^{\var{chain\_length}}
     \frac{\sin(q r_{ij})}{q r_{ij}}

of a single chain, averaged over all chains for :math:`\var{qbin}+1`
logarithmically spaced q-vectors :math:`\var{qmin}, \dots ,\var{qmax}`
where :math:`\var{qmin}>0` and :math:`\var{qmax}>\var{qmin}`. If is
used, the form factor will be averaged over all stored configurations
(see section ).

{ { } }

with :math:`q \in \{\var{qmin},\dots,\var{qmax}\}`.


.. _Chain radial distribution function:

Chain radial distribution function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

analyze rdfchain

Returns three radial distribution functions (rdf) for the chains. The
first rdf is calculated for monomers belonging to different chains, the
second rdf is for the centers of mass of the chains and the third one is
the distribution of the closest distances between the chains (the
shortest monomer-monomer distances). The distance range is given by and
and it is divided into equidistant bins.

{ { } }


.. _Mean square displacement of chains:

Mean square displacement of chains
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

[analyze:<g2>] [analyze:<g3>] [analyze:g123]

analyze analyze g123

Variant returns

-  the mean-square displacement of the beads in the chain ()

-  the mean-square displacement of the beads relative to the center of
   mass of the chain ()

-  or the motion of the center of mass ()

averaged over all stored configurations (see section ). At short time
scales, and coincide, since the motion of the center of mass is much
slower. At large timescales and coincide and correspond to the center of
mass motion, while levels off. and together correspond to . For details,
see :cite:`grest86a`.

Variant returns all of these observables for the current configuration,
as compared to the reference configuration. The reference configuration
is set, when the option is used.

{ …}

{ }



.. _Storing configurations:

Storing configurations
----------------------

Some observables (non-static ones) require knowledge of the particles’
positions at more than one or two times. Therefore, it is possible to
store configurations for later analysis. Using this mechanism, the
program is also able to work quasi-offline by successively reading in
previously saved configurations and storing them to perform any analysis
desired afterwards.

Note that the time at which configurations were taken is not stored. The
most observables that work with the set of stored configurations do
expect that the configurations are taken at equidistant timesteps.

Note also, that the stored configurations can be written to a file and
read from it via the command (see section ).


.. _Storing and removing configurations:

Storing and removing configurations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[analyze:push] [analyze:replace] [analyze:remove]

analyze append analyze remove analyze replace analyze push analyze
configs

Variant appends the current configuration to the set of stored
configurations. Variant removes the th stored configuration, or all, if
is not specified. Variant will replace the th configuration with the
current configuration.

Variant will append the current configuration to the set of stored
configuration and remove configurations from the beginning of the set
until the number of stored configurations is equal to . If is not
specified, only the first configuration in the set is removed.

Variants to return the number of currently stored configurations.

Variant will append the configuration to the set of stored
configurations. has to define coordinates for all configurations in the
format:

{ …}


.. _Getting the stored configurations:

Getting the stored configurations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[analyze:stored]

analyze configs analyze stored

Variant returns all stored configurations, while variant returns only
the number of stored configurations.

{ { …} }



.. _Computing statistical errors in time series:

Computing statistical errors in time series
---------------------------------------------

uwerr

uwerr

Calculates the mean value, the error and the error of the error for an
arbitrary numerical time series according to :cite:`wolff04a`.

is a matrix filled with the primary estimates :math:`a_\alpha^{i,r}`
from :math:`R\/` replica with :math:`N_1,N_2,\ldots,N_R` measurements
each.

.. math::

   \var{data}=\left(
         \begin{array}
           {{4}{c}} a_1^{1,1}&a_2^{1,1}&a_3^{1,1}&\cdots\\ 
           a_1^{2,1}&a_2^{2,1}&a_3^{2,1}&\cdots\\
           \vdots&\vdots&\vdots&\vdots\\
           a_1^{{N_1},1}&a_2^{{N_1},1}&a_3^{{N_1},1}&\cdots\\
           a_1^{1,2}&a_2^{1,2}&a_3^{1,2}&\cdots\\
           \vdots&\vdots&\vdots&\vdots\\
           a_1^{{N_R},R}&a_2^{{N_R},R}&a_3^{{N_R},R}&\cdots\\
         \end{array}
       \right)

is a vector whose elements specify the length of the individual replica.

.. math:: nrep=\left(N_1,N_2,\ldots,N_R\right)

is a user defined Tcl function returning a double with first argument a
vector which has as many entries as data has columns. If is given
instead of the column, the corresponding derived quantity is analyzed.

are further arguments to .

is the estimate :math:`S=\tau/\tau_{\textrm{int}}` as explained in
section (3.3) of :cite:`wolff04a`. The default is 1.5 and it
is never taken larger than :math:`\min_{r=1}^R{N_r}/2`.

If plot is specified, you will get the plots of :math:`\Gamma/\Gamma(0)`
and :math:`\tau_{int}` vs. :math:`W`. The data and gnuplot script is
written to the current directory.

where denotes the integrated autocorrelation time, and denotes a
*quality measure*, the probability to find a :math:`\chi^2` fit of the
replica estimates.

The function returns an error message if the windowing failed or if the
error in one of the replica is to large.
