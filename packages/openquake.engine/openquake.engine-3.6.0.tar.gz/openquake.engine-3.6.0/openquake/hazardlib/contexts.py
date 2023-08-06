# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2018-2019 GEM Foundation
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.
import abc
import numpy

from openquake.baselib import config
from openquake.baselib.hdf5 import vfloat64
from openquake.baselib.performance import Monitor
from openquake.hazardlib import imt as imt_module, const
from openquake.hazardlib.calc.filters import IntegrationDistance
from openquake.hazardlib.probability_map import ProbabilityMap
from openquake.hazardlib.geo.surface import PlanarSurface

# if there are few sites store the rupdata
FEWSITES = config.general.max_sites_disagg

KNOWN_DISTANCES = frozenset(
    'rrup rx ry0 rjb rhypo repi rcdpp azimuth rvolc'.split())


def get_distances(rupture, mesh, param):
    """
    :param rupture: a rupture
    :param mesh: a mesh of points or a site collection
    :param param: the kind of distance to compute (default rjb)
    :returns: an array of distances from the given mesh
    """
    if param == 'rrup':
        dist = rupture.surface.get_min_distance(mesh)
    elif param == 'rx':
        dist = rupture.surface.get_rx_distance(mesh)
    elif param == 'ry0':
        dist = rupture.surface.get_ry0_distance(mesh)
    elif param == 'rjb':
        dist = rupture.surface.get_joyner_boore_distance(mesh)
    elif param == 'rhypo':
        dist = rupture.hypocenter.distance_to_mesh(mesh)
    elif param == 'repi':
        dist = rupture.hypocenter.distance_to_mesh(mesh, with_depths=False)
    elif param == 'rcdpp':
        dist = rupture.get_cdppvalue(mesh)
    elif param == 'azimuth':
        dist = rupture.surface.get_azimuth(mesh)
    elif param == "rvolc":
        # Volcanic distance not yet supported, defaulting to zero
        dist = numpy.zeros_like(mesh.lons)
    else:
        raise ValueError('Unknown distance measure %r' % param)
    dist.flags.writeable = False
    return dist


class FarAwayRupture(Exception):
    """Raised if the rupture is outside the maximum distance for all sites"""


def get_num_distances(gsims):
    """
    :returns: the number of distances required for the given GSIMs
    """
    dists = set()
    for gsim in gsims:
        dists.update(gsim.REQUIRES_DISTANCES)
    return len(dists)


class RupData(object):
    """
    A class to collect rupture information into an array
    """
    def __init__(self, cmaker, sitecol):
        self.cmaker = cmaker
        self.sitecol = sitecol.complete
        self.N = len(sitecol.complete)
        self.data = []

    def from_srcs(self, srcs):
        """
        :returns: the underlying rupdata array
        """
        for src in srcs:
            for rup in src.iter_ruptures():
                self.cmaker.add_rup_params(rup)
                self.add(rup, src.id)
        return self.to_array()

    def add(self, rup, src_id):
        try:
            rate = rup.occurrence_rate
            probs_occur = numpy.zeros(0, numpy.float64)
        except AttributeError:  # for nonparametric ruptures
            rate = numpy.nan
            probs_occur = rup.probs_occur
        row = [src_id or 0, rate]
        for rup_param in self.cmaker.REQUIRES_RUPTURE_PARAMETERS:
            row.append(getattr(rup, rup_param))
        for dist_param in self.cmaker.REQUIRES_DISTANCES:
            row.append(get_distances(rup, self.sitecol, dist_param))
        closest = rup.surface.get_closest_points(self.sitecol)
        row.append(closest.lons)
        row.append(closest.lats)
        row.append(rup.weight)
        row.append(probs_occur)
        self.data.append(tuple(row))

    def to_array(self):
        dtlist = [('srcidx', numpy.uint32), ('occurrence_rate', float)]
        for rup_param in self.cmaker.REQUIRES_RUPTURE_PARAMETERS:
            dtlist.append((rup_param, float))
        for dist_param in self.cmaker.REQUIRES_DISTANCES:
            dtlist.append((dist_param, (float, (self.N,))))
        dtlist.append(('lon', (float, (self.N,))))  # closest lons
        dtlist.append(('lat', (float, (self.N,))))  # closest lats
        dtlist.append(('mutex_weight', float))
        dtlist.append(('probs_occur', vfloat64))
        return numpy.array(self.data, dtlist)


class ContextMaker(object):
    """
    A class to manage the creation of contexts for distances, sites, rupture.
    """
    REQUIRES = ['DISTANCES', 'SITES_PARAMETERS', 'RUPTURE_PARAMETERS']

    def __init__(self, trt, gsims, maximum_distance=None, param=None,
                 monitor=Monitor()):
        param = param or {}
        self.trt = trt
        self.gsims = gsims
        self.maximum_distance = maximum_distance or IntegrationDistance({})
        self.pointsource_distance = param.get('pointsource_distance', {})
        for req in self.REQUIRES:
            reqset = set()
            for gsim in gsims:
                reqset.update(getattr(gsim, 'REQUIRES_' + req))
            setattr(self, 'REQUIRES_' + req, reqset)
        filter_distance = param.get('filter_distance')
        if filter_distance is None:
            if 'rrup' in self.REQUIRES_DISTANCES:
                filter_distance = 'rrup'
            elif 'rjb' in self.REQUIRES_DISTANCES:
                filter_distance = 'rjb'
            else:
                filter_distance = 'rrup'
        self.filter_distance = filter_distance
        self.reqv = param.get('reqv')
        self.REQUIRES_DISTANCES.add(self.filter_distance)
        if self.reqv is not None:
            self.REQUIRES_DISTANCES.add('repi')
        if hasattr(gsims, 'items'):
            # gsims is actually a dict rlzs_by_gsim
            # since the ContextMaker must be used on ruptures with the
            # same TRT, given a realization there is a single gsim
            self.gsim_by_rlzi = {}
            for gsim, rlzis in gsims.items():
                for rlzi in rlzis:
                    self.gsim_by_rlzi[rlzi] = gsim
        self.ctx_mon = monitor('make_contexts', measuremem=False)
        self.poe_mon = monitor('get_poes', measuremem=False)

    def filter(self, sites, rupture):
        """
        Filter the site collection with respect to the rupture.

        :param sites:
            Instance of :class:`openquake.hazardlib.site.SiteCollection`.
        :param rupture:
            Instance of
            :class:`openquake.hazardlib.source.rupture.BaseRupture`
        :returns:
            (filtered sites, distance context)
        """
        distances = get_distances(rupture, sites, self.filter_distance)
        if self.maximum_distance:
            mask = distances <= self.maximum_distance(
                rupture.tectonic_region_type, rupture.mag)
            if mask.any():
                sites, distances = sites.filter(mask), distances[mask]
            else:
                raise FarAwayRupture(
                    '%d: %d km' % (rupture.serial, distances.min()))
        return sites, DistancesContext([(self.filter_distance, distances)])

    def add_rup_params(self, rupture):
        """
        Add .REQUIRES_RUPTURE_PARAMETERS to the rupture
        """
        for param in self.REQUIRES_RUPTURE_PARAMETERS:
            if param == 'mag':
                value = rupture.mag
            elif param == 'strike':
                value = rupture.surface.get_strike()
            elif param == 'dip':
                value = rupture.surface.get_dip()
            elif param == 'rake':
                value = rupture.rake
            elif param == 'ztor':
                value = rupture.surface.get_top_edge_depth()
            elif param == 'hypo_lon':
                value = rupture.hypocenter.longitude
            elif param == 'hypo_lat':
                value = rupture.hypocenter.latitude
            elif param == 'hypo_depth':
                value = rupture.hypocenter.depth
            elif param == 'width':
                value = rupture.surface.get_width()
            else:
                raise ValueError('%s requires unknown rupture parameter %r' %
                                 (type(self).__name__, param))
            setattr(rupture, param, value)

    def make_contexts(self, sites, rupture):
        """
        Filter the site collection with respect to the rupture and
        create context objects.

        :param sites:
            Instance of :class:`openquake.hazardlib.site.SiteCollection`.

        :param rupture:
            Instance of
            :class:`openquake.hazardlib.source.rupture.BaseRupture`

        :returns:
            Tuple of two items: sites and distances context.

        :raises ValueError:
            If any of declared required parameters (site, rupture and
            distance parameters) is unknown.
        """
        sites, dctx = self.filter(sites, rupture)
        for param in self.REQUIRES_DISTANCES - set([self.filter_distance]):
            distances = get_distances(rupture, sites, param)
            setattr(dctx, param, distances)
        reqv_obj = (self.reqv.get(rupture.tectonic_region_type)
                    if self.reqv else None)
        if reqv_obj and isinstance(rupture.surface, PlanarSurface):
            reqv = reqv_obj.get(dctx.repi, rupture.mag)
            if 'rjb' in self.REQUIRES_DISTANCES:
                dctx.rjb = reqv
            if 'rrup' in self.REQUIRES_DISTANCES:
                reqv_rup = numpy.sqrt(reqv**2 + rupture.hypocenter.depth**2)
                dctx.rrup = reqv_rup
        self.add_rup_params(rupture)
        # NB: returning a SitesContext make sures that the GSIM cannot
        # access site parameters different from the ones declared
        sctx = SitesContext(self.REQUIRES_SITES_PARAMETERS, sites)
        return sctx, dctx

    def gen_rup_contexts(self, src, sites):
        """
        :param src: a hazardlib source
        :param sites: the sites affected by it
        :yields: (rup, sctx, dctx)
        """
        sitecol = sites.complete
        N = len(sitecol)
        fewsites = N <= FEWSITES
        rupdata = RupData(self, sites)
        for rup, sites in self._gen_rup_sites(src, sites):
            try:
                with self.ctx_mon:
                    sctx, dctx = self.make_contexts(sites, rup)
            except FarAwayRupture:
                continue
            yield rup, sctx, dctx
            if fewsites:  # store rupdata
                rupdata.add(rup, src.id)
        self.rupdata = rupdata.to_array()

    def _gen_rup_sites(self, src, sites):
        # implements the pointsource_distance feature
        pdist = self.pointsource_distance.get(src.tectonic_region_type)
        if hasattr(src, 'location') and pdist:
            close_sites, far_sites = sites.split(src.location, pdist)
            if close_sites is None:  # all is far
                for rup in src.iter_ruptures(False, False):
                    yield rup, far_sites
            elif far_sites is None:  # all is close
                for rup in src.iter_ruptures(True, True):
                    yield rup, close_sites
            else:
                for rup in src.iter_ruptures(True, True):
                    yield rup, close_sites
                for rup in src.iter_ruptures(False, False):
                    yield rup, far_sites
        else:
            for rup in src.iter_ruptures():
                yield rup, sites

    def poe_map(self, src, s_sites, imtls, trunclevel, rup_indep=True):
        """
        :param src: a source object
        :param s_sites: a filtered SiteCollection of sites around the source
        :param imtls: intensity measure and levels
        :param trunclevel: truncation level
        :param rup_indep: True if the ruptures are independent
        :returns: a ProbabilityMap instance
        """
        pmap = ProbabilityMap.build(
            len(imtls.array), len(self.gsims), s_sites.sids,
            initvalue=rup_indep)
        eff_ruptures = 0
        for rup, sctx, dctx in self.gen_rup_contexts(src, s_sites):
            eff_ruptures += 1
            with self.poe_mon:
                pnes = self._make_pnes(rup, sctx, dctx, imtls, trunclevel)
                for sid, pne in zip(sctx.sids, pnes):
                    if rup_indep:
                        pmap[sid].array *= pne
                    else:
                        pmap[sid].array += (1.-pne) * rup.weight
        if rup_indep:
            pmap = ~pmap
        pmap.eff_ruptures = eff_ruptures
        return pmap

    # NB: it is important for this to be fast since it is inside an inner loop
    def _make_pnes(self, rupture, sctx, dctx, imtls, trunclevel):
        nsites = len(sctx.sids)
        pne_array = numpy.zeros((nsites, len(imtls.array), len(self.gsims)))
        for i, gsim in enumerate(self.gsims):
            dctx_ = dctx.roundup(gsim.minimum_distance)
            for imt in imtls:
                slc = imtls(imt)
                if hasattr(gsim, 'weight') and gsim.weight[imt] == 0:
                    # set by the engine when parsing the gsim logictree;
                    # when 0 ignore the gsim: see _build_trts_branches
                    pno = numpy.ones((nsites, slc.stop - slc.start))
                else:
                    poes = gsim.get_poes(
                        sctx, rupture, dctx_,
                        imt_module.from_string(imt), imtls[imt], trunclevel)
                    pno = rupture.get_probability_no_exceedance(poes)
                pne_array[:, slc, i] = pno
        return pne_array

    # tested in scenario/case_11
    def get_limit_distance(self, sites, rup, imts, minimum_intensity):
        """
        Calculate the distance over which the GMVs are lower than the
        minimum_intensity for all IMTs and GSIMs.

        :param sites: a SiteCollection
        :param rup: a rupture
        :param imts: a sequence on intensity measure strings
        :param minimum_intensity: a dictionary TRT -> minimum_intensity
        :returns: the limit distance
        """
        if not minimum_intensity:
            return self.maximum_distance[rup.tectonic_region_type]
        sctx, dctx = self.make_contexts(sites, rup)
        fdist = getattr(dctx, self.filter_distance)
        limit_dist = 0
        for im in imts:
            try:
                minint = minimum_intensity[im]
            except KeyError:
                minint = minimum_intensity['default']
            imt = imt_module.from_string(im)
            for gsim in self.gsims:
                mean, _ = gsim.get_mean_and_stddevs(
                    sctx, rup, dctx, imt, [const.StdDev.TOTAL])
                for i, gmv in enumerate(numpy.exp(mean)):
                    if gmv <= minint:
                        limit_dist = max(limit_dist, fdist[i])
                        break
        return limit_dist or self.maximum_distance[rup.tectonic_region_type]


class BaseContext(metaclass=abc.ABCMeta):
    """
    Base class for context object.
    """
    def __eq__(self, other):
        """
        Return True if ``other`` has same attributes with same values.
        """
        if isinstance(other, self.__class__):
            if self._slots_ == other._slots_:
                oks = []
                for s in self._slots_:
                    a, b = getattr(self, s, None), getattr(other, s, None)
                    if a is None and b is None:
                        ok = True
                    elif a is None and b is not None:
                        ok = False
                    elif a is not None and b is None:
                        ok = False
                    elif hasattr(a, 'shape') and hasattr(b, 'shape'):
                        if a.shape == b.shape:
                            ok = numpy.allclose(a, b)
                        else:
                            ok = False
                    else:
                        ok = a == b
                    oks.append(ok)
                return numpy.all(oks)
        return False


# mock of a site collection used in the tests and in the SMTK
class SitesContext(BaseContext):
    """
    Sites calculation context for ground shaking intensity models.

    Instances of this class are passed into
    :meth:`GroundShakingIntensityModel.get_mean_and_stddevs`. They are
    intended to represent relevant features of the sites collection.
    Every GSIM class is required to declare what :attr:`sites parameters
    <GroundShakingIntensityModel.REQUIRES_SITES_PARAMETERS>` does it need.
    Only those required parameters are made available in a result context
    object.
    """
    # _slots_ is used in hazardlib check_gsim and in the SMTK
    def __init__(self, slots='vs30 vs30measured z1pt0 z2pt5'.split(),
                 sitecol=None):
        self._slots_ = slots
        if sitecol is not None:
            self.sids = sitecol.sids
            for slot in slots:
                setattr(self, slot, getattr(sitecol, slot))


class DistancesContext(BaseContext):
    """
    Distances context for ground shaking intensity models.

    Instances of this class are passed into
    :meth:`GroundShakingIntensityModel.get_mean_and_stddevs`. They are
    intended to represent relevant distances between sites from the collection
    and the rupture. Every GSIM class is required to declare what
    :attr:`distance measures <GroundShakingIntensityModel.REQUIRES_DISTANCES>`
    does it need. Only those required values are calculated and made available
    in a result context object.
    """
    _slots_ = ('rrup', 'rx', 'rjb', 'rhypo', 'repi', 'ry0', 'rcdpp',
               'azimuth', 'hanging_wall', 'rvolc')

    def __init__(self, param_dist_pairs=()):
        for param, dist in param_dist_pairs:
            setattr(self, param, dist)

    def roundup(self, minimum_distance):
        """
        If the minimum_distance is nonzero, returns a copy of the
        DistancesContext with updated distances, i.e. the ones below
        minimum_distance are rounded up to the minimum_distance. Otherwise,
        returns the original DistancesContext unchanged.
        """
        if not minimum_distance:
            return self
        ctx = DistancesContext()
        for dist, array in vars(self).items():
            small_distances = array < minimum_distance
            if small_distances.any():
                array = numpy.array(array)  # make a copy first
                array[small_distances] = minimum_distance
                array.flags.writeable = False
            setattr(ctx, dist, array)
        return ctx


# mock of a rupture used in the tests and in the SMTK
class RuptureContext(BaseContext):
    """
    Rupture calculation context for ground shaking intensity models.

    Instances of this class are passed into
    :meth:`GroundShakingIntensityModel.get_mean_and_stddevs`. They are
    intended to represent relevant features of a single rupture. Every
    GSIM class is required to declare what :attr:`rupture parameters
    <GroundShakingIntensityModel.REQUIRES_RUPTURE_PARAMETERS>` does it need.
    Only those required parameters are made available in a result context
    object.
    """
    _slots_ = (
        'mag', 'strike', 'dip', 'rake', 'ztor', 'hypo_lon', 'hypo_lat',
        'hypo_depth', 'width', 'hypo_loc')
    temporal_occurrence_model = None  # to be set

    def __init__(self, rec=None):
        if rec is not None:
            for name in rec.dtype.names:
                setattr(self, name, rec[name])

    def get_probability_no_exceedance(self, poes):
        """
        Compute and return the probability that in the time span for which the
        rupture is defined, the rupture itself never generates a ground motion
        value higher than a given level at a given site.

        Such calculation is performed starting from the conditional probability
        that an occurrence of the current rupture is producing a ground motion
        value higher than the level of interest at the site of interest.
        The actual formula used for such calculation depends on the temporal
        occurrence model the rupture is associated with.
        The calculation can be performed for multiple intensity measure levels
        and multiple sites in a vectorized fashion.

        :param poes:
            2D numpy array containing conditional probabilities the the a
            rupture occurrence causes a ground shaking value exceeding a
            ground motion level at a site. First dimension represent sites,
            second dimension intensity measure levels. ``poes`` can be obtained
            calling the :meth:`method
            <openquake.hazardlib.gsim.base.GroundShakingIntensityModel.get_poes>
        """
        if numpy.isnan(self.occurrence_rate):  # nonparametric rupture
            # Uses the formula
            #
            #    ∑ p(k|T) * p(X<x|rup)^k
            #
            # where `p(k|T)` is the probability that the rupture occurs k times
            # in the time span `T`, `p(X<x|rup)` is the probability that a
            # rupture occurrence does not cause a ground motion exceedance, and
            # thesummation `∑` is done over the number of occurrences `k`.
            #
            # `p(k|T)` is given by the attribute probs_occur and
            # `p(X<x|rup)` is computed as ``1 - poes``.
            # Converting from 1d to 2d
            if len(poes.shape) == 1:
                poes = numpy.reshape(poes, (-1, len(poes)))
            p_kT = self.probs_occur
            prob_no_exceed = numpy.array(
                [v * ((1 - poes) ** i) for i, v in enumerate(p_kT)])
            prob_no_exceed = numpy.sum(prob_no_exceed, axis=0)
            if isinstance(prob_no_exceed, numpy.ndarray):
                prob_no_exceed[prob_no_exceed > 1.] = 1.  # sanity check
                prob_no_exceed[poes == 0.] = 1.  # avoid numeric issues
            return prob_no_exceed
        # parametric rupture
        tom = self.temporal_occurrence_model
        return tom.get_probability_no_exceedance(self.occurrence_rate, poes)
