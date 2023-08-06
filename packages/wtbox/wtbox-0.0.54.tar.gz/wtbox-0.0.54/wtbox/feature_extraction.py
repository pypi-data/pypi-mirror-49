# -*- coding: utf-8 -*-
"""
Created on Wed Aug 05 10:00:59 2015

@author: pkiefer
"""
import emzed
import utils as _utils
import checks_and_settings as _checks
from peakmap_operations import determine_spectral_baseline_and_noise
from table_operations import update_rt_by_integration as _update_rt_by_integration
from _fix_inspector_bug import fix_ms2_inspect_integration_bug as _inspect_
from emzed.core.data_types import PeakMap
from copy import deepcopy
from integrate_smoothed_emg import emg_smoothed
from _shift_rt_windows import shift_rt_windows
import table_operations as _top
import _ff_metabo_config as ff
import numpy as np
import hires
import _local_feature_finder as lff

#################################################################################################
# MS_level 1
#################################################################################################
# Untargeted extraction
def enhanced_ff_metabo(peakmap, config=None, adapt=True, advanced_gui=False, c13=False, 
                       max_c_gap=0, elements=('C',), min_abundance=0.01, 
                        determine_intensity_threshold=False):
    """ Function untargeted_peaks(pm=None, config=None, adapt=True, advanced=False)
    uses open MS featureFinderMetabo for peak detection and feature grouping if adapt=True (default), 
    ff_metabo configuration can be adapted by the user via a GUI in a simplified mode with selected
    parameters and an adcanced mode (advanced=True) to access all parameters. To analyze single
    peakmap use argument pm. Function returns a table. To  analyze an iterable  
    
    """
    
    if not config:
        config=ff.get_default_ff_metabo()
    if adapt:
        config=ff.adapt_ff_metabo_config(config, advanced=advanced_gui)
    assert isinstance(peakmap, PeakMap), 'pm must be of Type PeakMap'
    if determine_intensity_threshold:
        threshold=determine_ff_config_intensity_threshold(peakmap)
        print 
        config['common_noise_threshold_int']=threshold
    t= emzed.ff.runMetaboFeatureFinder(peakmap, **config)
    # bug fixing: wrong formats 
    t.setColFormat('mzmin', '%.5f')
    t.setColFormat('mzmax', '%.5f')
    # hires feature_regrouper and local_ff algorithms require peak area or intensity, 
    # we therefore reintegrate the table using  `max` integrator 
    t=emzed.utils.integrate(t, 'max', n_cpus=_utils.get_n_cpus(t, 4))
    # we add the feature_finder config to tale meta data
    t.meta['ff_config']=config
    if c13:
        rttol=float(np.percentile(t.fwhm.values, 60))/2
        t=hires.feature_regrouper(t, min_abundance=min_abundance, elements=elements, 
                                max_c_gap=max_c_gap, rt_tolerance=rttol)
        t.replaceColumn('feature_id', t.isotope_cluster_id, type_=int, format_='%d')
        t.dropColumns('isotope_cluster_id', 'carbon_isotope_shift', 'unlabeled_isotope_shift',
                          'mass_corr')
    return lff.local_ff_metabo(t, c13=c13, ff_config=config, max_c_gap=max_c_gap, 
                        min_abundance=min_abundance, elements=elements)
                             
                             
    
def determine_ff_config_intensity_threshold(pm, sn=3):
    """
        Determines what is the minimal peak_intensity below a spectral peak is ignored. 
        The function determines baseline and noise level assuming that the baseline should contain
        the highest point denity (J Ams Soc Mass Spectrom 2000, 11, 320-3332).
        To this end we build a histogramm of all intensities over all spectra, the bin width of
        the histogramm is deteremined by the rule of Freedman und Diaconis. the mean intensity
        of the bin with highest abundance is said to be the baseline value and the fwhm of the
        histogramm is said to be the noise (more precisely : fwhm/2.5438 = sigma, sigma * 3=noise).
        
    """
    baseline, noise=determine_spectral_baseline_and_noise(pm)
    return baseline+ sn*noise/2.3548 # fwhm/sigma = 2.3548   

##########################################
# Targeted extraction




def targeted_peaks_ms(peakmap, peaks_table, enhanced_integrate=True, integrator='trapez', 
                      fwhm=None, max_dev_percent=20, min_area=-1.0, n_cpus=None, step=1):
    """ Function targeted_peaks_ms(peakmap, peaks_table, enhanced_integrate=True, 
        integrator='trapez', fwhm=None, max_dev_percent=20, min_area=-1.0, n_cpus=None, step=1) 
        extracts MS level 1 peaks LC-MS level 1peaks of peakmap defined in table peaks_table by integration
        using function -> wtbox.utils.enhanced_integrate if enhanced_integrate == True. 
        Optional parameters are related to enhanced_integrate. If attribute enhanced_integrate
        is False peaks will be integrated applying emzed.utils.integrate function with integration
        algorithm set by attribute integrator.
        If min_area < 0 all rows of peaks_table are kept, else rows with area <= min_area 
        will be removed !
        Peaks_table requires columns 'mzmin', 'mzmax', 'rtmin', 'rtmax'. 
        
        
    """
    _checks.is_ms_peaks_table(peaks_table)
    assert 1 in peakmap.getMsLevels(), 'MS_level 1 data are missing!'
    peaks_table=_add_peakmap_to_table( peakmap, peaks_table)
    if enhanced_integrate:
        t=_utils.enhanced_integrate(peaks_table,  fwhm=fwhm, max_dev_percent=max_dev_percent, 
                              min_area=min_area, mslevel=1, n_cpus=n_cpus, step=step)
    else:                              
        t=integrate_and_filter(peaks_table, integrator=integrator, min_area=min_area, mslevel=1)
    return _update_rt_by_integration(t, mslevel=1)
    


def _add_peakmap_to_table(pm, table):
    t=table.copy()
    colnames=['rtmin', 'rtmax', 'mzmin', 'mzmax']
    postfixes=t.supportedPostfixes(colnames)
    for pstfx in postfixes:
        t.addColumn('peakmap'+pstfx, pm, type_=PeakMap)
        t.addColumn('source'+pstfx, pm.meta['source'], type_=str)
    return t


################################################################################################
# MS_level 2
################################################################################################

# Untargeted extraction

def metaboff_ms2(peakmap, ff_metabo_config=None, min_area=1e2, integrator='trapez'):
    """ metaboff_ms2(peakmap, ff_metabo_config=None) detects all peaks of ms_level_2 using 
    feature_finder_ms from peakmap. If ff_metabo_config is not provided a dialog window will open. 
    If min_area < 0 all rows of peaks_table are kept, else rows with area <= min_area will 
    be removed !
    """
    _checks.is_peakmap(peakmap)
    if not ff_metabo_config:
        ff_metabo_config=_checks.default_ffmetabo_config()
        
        ff_metabo_config['ms_level']=2
    tuples=peakmap.splitLevelN(2)
#    print tuples
    results=[]
    failed=[]
    for precursor, pm in tuples:
        peaks=find_ms2_peaks(pm, ff_metabo_config)        
        if len(peaks):
            peaks.addColumn('precursor_ion', precursor, type_=float, insertBefore='mz')
            results.append(peaks)
        else:
          failed.append(precursor)  
    overall=emzed.utils.stackTables(results)
    return overall

        
def find_ms2_peaks(pm, params):
    try:
        return emzed.ff.runMetaboFeatureFinder(pm, **params)
    except:
        # not enough spectra
        return []

def _show_problem_cases(cases):
    if len(cases):
        precursors=', '.join([str(case) for case in cases])
        print
        print
        print 'WARNING: NO EIC PEAKS FOUND FOR PRECURSOR IONS %s !!!!' %precursors


###########################################################################################

# Targeted extraction


def targeted_peaks_ms2(peakmap, peaks_table, min_area=-1, enhanced_integrate=True, fwhm=None, 
                       max_dev_percent=20, n_cpus=None, step=1, integrator='trapez'):
    """
    Function targeted_peaks_ms2 extracts MS level 2 peaks defined in table peaks_table by integration
        using function -> wtbox.utils.enhanced_integrate if enhanced_integrate == True. 
        Optional parameters are related to enhanced_integrate. If attribute enhanced_integrate
        is False peaks will be integrated applying emzed.utils.integrate function with integration
        algorithm set by attribute integrator.
        If min_area < 0 all rows of peaks_table are kept, else rows with area <= min_area 
        will be removed !
        Peaks_table requires columns 'mzmin', 'mzmax', 'rtmin', 'rtmax'. 
    """
    _checks.is_prm_peaks_table(peaks_table)
    assert 2 in peakmap.getMsLevels(), 'MS_level 2 data are missing'
    tuples=peakmap.splitLevelN(2)
    for precursor, pm in tuples:
        add_peakmap_to_precursor(precursor, pm, peaks_table)
    if enhanced_integrate:    
        return _utils.enhanced_integrate(peaks_table, mslevel=2, fwhm=fwhm, 
                    max_dev_percent=max_dev_percent,min_area=min_area, n_cpus=n_cpus, step=step)
    t=integrate_and_filter(peaks_table, integrator=integrator, min_area=min_area, mslevel=2)
    return _update_rt_by_integration(t)
    



    
def add_peakmap_to_precursor(precursor, pm, table):
    t=table
    colnames=['rtmin', 'rtmax', 'mzmin', 'mzmax']
    postfixes=table.supportedPostfixes(colnames)
    for pstfx in postfixes:
        _update_empty_column(table, 'peakmap'+pstfx, PeakMap)
        _update_empty_column(table, 'source'+pstfx, str)
        table.addColumn('delta', (t.getColumn('precursor_ion'+pstfx)-precursor).apply(abs), 
                        type_=float)
        if check_precursor_consistency(table, pm, pstfx):
            print t.delta.values, t.delta.min()
            t.replaceColumn('peakmap'+pstfx, (t.delta==t.delta.min()).thenElse\
            (pm, t.getColumn('peakmap'+pstfx)), type_=PeakMap)
            t.replaceColumn('source'+pstfx, t.getColumn('peakmap'+pstfx).isNotNone().thenElse\
            (t.getColumn('peakmap'+pstfx).apply(lambda v: v.meta['source']), 
             t.getColumn('source'+pstfx)))
        t.dropColumns('delta')
    
    
def check_precursor_consistency(table, pm, pstfx):
    selected=table.filter(table.delta==table.delta.min())
    delta_value=selected.delta.uniqueValue()
    if delta_value>0.1:
        print 'precursor not detected'
        return False
    else:    
        rtmin, rtmax=pm.rtRange()
        mzmin, mzmax=pm.mzRange(2)
        rtmin1_crit = all([rtmin<=rtmax_ for rtmax_ in selected.getColumn('rtmax'+pstfx).values])
        rtmin2_crit = all([rtmax>=rtmin_ for rtmin_ in selected.getColumn('rtmin'+pstfx).values])
        mzmin_crit=selected.getColumn('mzmin'+pstfx).min()>=mzmin
        mzmax_crit=selected.getColumn('mzmax'+pstfx).max()<=mzmax
        if all([rtmin1_crit, rtmin2_crit, mzmin_crit, mzmax_crit]):
            return True
        else:
            print [rtmin1_crit, rtmin2_crit, mzmin_crit, mzmax_crit]
            print mzmin, table.getColumn('mzmin'+pstfx).min() 
            print mzmax, table.getColumn('mzmax'+pstfx).max()
            emzed.gui.showWarning('Inconsistency for precursor %f.' \
            'peakmap does not comprise of table fragment ion peaks' \
                                %selected.getColumn('precursor_ion'+pstfx).uniqueValue())
            return False
    
def _mz_range(pm):
    mzmin= min([spec.mzMin() for spec in pm.spectra])
    mzmax= max([spec.mzMax() for spec in pm.spectra])
    return mzmin, mzmax
    
def _update_empty_column(table, _colname='peakmap', type_=None):
    if not table.hasColumn(_colname):
        table.addColumn(_colname, None, type_=type_)
    
##################################################################################################
# MS level 1 + 2
def smart_peak_extraction(peakmap, ref_table, max_delta_rt=20.0, id_col='feature_id', 
                    max_diff_percent=None, mslevel=1, n_cpus=None):
    """ 
    Function smart_integrate(peakmap, ref, kwargs) an integratable reference table is 
    used to perform a local alignment in mass trace section 
        [ref.rtmin - max_delta_rtmin; ref.rtmax + max_delta_rt] prior to integration. 
    If the peak window of isobaric peaks do overlap, the pattern of the 
    merged peaks is used to shift rt_windows.
    
    IMPORTANT: ALL ISOBARIC PEAKS occuring within the enlarged rt windows should be defined 
    in the ref table. If not this might lead to missmatching. Therefore: carefully check the 
    neighboring environment of each peak when building the reference table
    Reference table ref, required columns: mzmin, mzmax, rtmin, rtmax, peakmap, id_col
    key word arguments:
        - max_delta_rt: maximum retentions shift added to rtmin and rt_max. 
        - mztol: the m/z tolerance 
        - id_col: if identifyers of grouped peaks are used (e.g. feature_id groups all 
        isotopologues) the peak of the group with bigest area is used for local alignment.
         - max_diff_percent: parameter for smoothed_emg: It defines maximal allowed area difference
         between trapez integration and emg_model
        - mslevel: the ms level of the peaks (1,2)
        n_cpus: number of cpus: default = None if none optimal number of cpus is determined
            automatically
    """
    ref=ref_table
    n_cpus = _utils.get_n_cpus(ref) if n_cpus==None else n_cpus
    _checks.is_integratable_table(ref)
    try:
        _checks.is_integrated_table(ref)
        assert len(set(ref.method.values)-set(['trapez, max, std']))>0
    except:
        ref=emzed.utils.integrate(ref, 'trapez')
    multiprocess= False if n_cpus==1 else True
    t=shift_rt_windows(peakmap, ref, id_col, max_delta_rt, multiprocess=multiprocess)
    return emg_smoothed(t, max_diff_percent=max_diff_percent, mslevel=mslevel)
################################################################################################
# Top N experimet
################################################################################################

def top_n_to_table(peakmap, rttol=20, mztol=0.003):
    """top_n_to_table(pm_, rttol=5, mztol=0.3) extracts all precursor_ion peaks on mslevel 1
    with corresponding ms_level 2 spectra. Attributes: 
        - Peakmap: PeakMap with mslevels [1, 2]; 
        - rttol: retention time tolerance in second, 
        - mztol: m/z tolerance in units.

    """
    pm=deepcopy(peakmap)
    pairs=_ms_dd_ms2(pm)
    print len(pairs)
    pm1=pm.extract(mslevelmax=1)
    tables=[]
    for rt, ms2 in pairs:
        t=emzed.utils.toTable('precursor_ion', [v[0] for v in ms2], type_=float,
                              format_='%.5f')
        t.addColumn('rt', rt, type_=float, format_='"%.2fm" %(o/60)')
        t.addColumn('rtmin', t.rt-rttol,type_=float, format_='"%.2fm" %(o/60)')
        t.addColumn('rtmax', t.rt+rttol,type_=float, format_='"%.2fm" %(o/60)')    
        t.addColumn('mzmin', t.precursor_ion-mztol, type_=float, format_='%.5f')
        t.addColumn('mzmax', t.precursor_ion+mztol, type_=float, format_='%.5f')
        t.addColumn('peakmap', pm1)
        subtables=[_top.single_spec_to_table(prec, spec) for prec, spec in ms2]
        t.addColumn('ms2_specs', subtables)
        tables.append(t)
    t=emzed.utils.stackTables(tables)
    return _update_rt_by_integration(t)
    

  
def _ms_dd_ms2(pm):
    # helper function of top_n_to_table
    ms1_specs=pm.levelNSpecs(1)
    ms_2_data=pm.splitLevelN(2, significant_digits_precursor=4)
    def unpack(precursor, pm):
        return [[s.rt, (precursor, s)] for s in pm.spectra]
    ms_2=[]
    for precursor, pm2 in ms_2_data:
        ms_2.extend(unpack(precursor, pm2))
    ms_1=[[spec.rt, spec] for spec in ms1_specs]
    
    spec_rt=[spec.rt for spec in ms1_specs]
    d_rt=zip(spec_rt, spec_rt[1:])
    d_rt.append((spec_rt[-1], spec_rt[-1]+10)) #all ms2 spectra are linked to final ms_1 spectrum 
    pairs=[]
    for i in range(len(ms_1)):
        ms2_specs=[p for rt, p in ms_2 if (rt > d_rt[i][0]) and (rt < d_rt[i][1])]
        pair=(ms_1[i][:1]*len(ms2_specs), ms2_specs)
        if len(ms2_specs):
            pairs.append(pair)
    return pairs



def _det_rt(params):
    rts, ints=params
    idx=np.where(max(ints)== ints)[0][0]
    return rts[idx]
    
#################################################################################################
# 

def adapt_rt_windows(peaks_table, pm, split_by='feature_id', mslevel=None, keep_peakmap=False):
    """
    adapt_rt_windows(peaks_table, pm, split_by='feature_id', mslevel=None) allows manualy adapting
    retention time windows to peaks by integration for mslevels 1 and 2. peaks_table required 
    columns: mzmin, mzmax, rtmin, rtmax, and column defined by split_by. mslevel will be ignored
    if table provides column mslevel.By default mslevel is 1. If mslevel ==2 column precursor_ion 
    is required. If more than one peak per group is integrated, the one with largest area will 
    be selected to modify retention time.
    """
    colnames=[n for n in peaks_table.getColNames()]
    if keep_peakmap:
        pstfx=_get_postfix(peaks_table)
        name=''.join(['peakmap', pstfx])
        colnames.append(name)
    tables=_prepare_table_for_inspection(peaks_table, pm, split_by, ms_level=mslevel)
    _inspect(tables)
    _adapt_rt(tables)    
    return extract_peaks_table(tables, colnames)


def _prepare_table_for_inspection(t, pm, split_by, ms_level=None):
    pstfx=_get_postfix(t)
    print pstfx
    if t.hasColumn('mslevel'+pstfx):
        levels=[]
        for level in t.splitBy('mslevel'+pstfx):
            mslevel=level.getColumn('mslevel'+pstfx).uniqueValue()
            _add_peakmap(level, pm, mslevel, pstfx)
            levels.append(emzed.utils.integrate(level, 'no_integration', msLevel=mslevel, n_cpus=1))
        t=emzed.utils.mergeTables(levels, force_merge=True)
    else:
#        import pdb; pdb.set_trace()
        _add_peakmap(t, pm, ms_level, pstfx)
        t=emzed.utils.integrate(t, 'no_integration', msLevel=ms_level, n_cpus=1)
    
    tables=t.splitBy(split_by)
    [_set_title(sub, split_by) for sub in tables]
    return tables

def _get_postfix(t):
    return _top.find_common_postfix(t)


def _add_peakmap(t, pm, mslevel, pstfx):
    if mslevel<=1:
        t.addColumn('peakmap'+pstfx, pm, type_=PeakMap)
    else:
        assert t.hasColumn('precursor_ion'+pstfx), 'column precursor_ion is required if mslevel>1'
        targeted_peaks_ms2(pm, t)
            

def _set_title(t, id_col):
    t.title=str(t.getColumn(id_col).uniqueValue())

    

def _inspect(tables):
    emzed.gui.showInformation('you can adapt rt windows of a feature by moving integration '\
            'bounderies and reintegrate the peak using any integration algorithm except' \
            '`no_integration`. It is sufficient to integrate one peak per group to change '\
            'rtmin and rtmax of all grouped peaks.')
    #emzed.gui.inspect(tables)
    _inspect_(tables)

def _adapt_rt(tables, test=False):
    for t in tables:
        pstfx=_top.find_common_postfix(t)
        area_='area'+pstfx
        area=t.getColumn(area_).max()
        print ' max area', area
        while area:
            sub=t.filter(t.getColumn(area_)==area)
            try:
                rtmin=sub.getColumn('rtmin'+pstfx).uniqueValue()
                rtmax=sub.getColumn('rtmax'+pstfx).uniqueValue()
                t.replaceColumn('rtmin'+pstfx, rtmin, type_=float)
                t.replaceColumn('rtmax'+pstfx, rtmax, type_=float)
                area=0
            except:
                # to make function testable
                if test:
                    assert False, ''
                else:
                    emzed.gui.showWarning('Provided feature_id has to be reintegrated!')
                    _inspect(t)
                    area=area=t.getColumn(area_).max()


def extract_peaks_table(tables, colnames):
    t=emzed.utils.mergeTables(tables, force_merge=True)
    return t.extractColumns(*colnames)
######################################################

def integrate_and_filter(t, integrator='trapez', min_area=1e2, mslevel=1):
    t=emzed.utils.integrate(t, integrator, msLevel=mslevel, n_cpus=1)
    integrated=t.filter(t.area>=min_area)
    not_int=t.filter(t.area<min_area)
    not_int=emzed.utils.integrate(not_int, 'no_integration', n_cpus=1)
    return emzed.utils.stackTables([integrated, not_int])



# temporary
def help_():
    t=emzed.utils.toTable('Number_of_Glu', [10,11], type_=int)
    t.addColumn('Isotopologue', [1,0], type_=int)
    t.addColumn('z', [1,1], type_=int)
    t.addColumn('mzmin', [918.30, 611.86], type_=float)
    t.addColumn('mzmax', [919.31, 612.87], type_=float)
    t.addColumn('rtmin', [1800.0, 1800.0], type_=float)
    t.addColumn('rtmax', [2040.0, 2040.0], type_=float)
    return t

def help_1():
    t=emzed.utils.toTable('fid', [10], type_=int)
    t.addColumn('Isotopologue', [1], type_=int)
    t.addColumn('z', [1], type_=int)
    t.addColumn('mzmin', [918.30], type_=float)
    t.addColumn('mzmax', [919.31], type_=float)
    t.addColumn('rtmin', [1800.0], type_=float)
    t.addColumn('rtmax', [2040.0], type_=float)
    return t