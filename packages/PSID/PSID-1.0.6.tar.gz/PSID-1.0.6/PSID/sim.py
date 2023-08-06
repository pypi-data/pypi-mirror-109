""" Omid Sani, Shanechi Lab, University of Southern California, 2020 """
"Tools for simulating models"
import os, copy, pickle, re
from datetime import datetime
from difflib import SequenceMatcher
import hashlib

import numpy as np
from numpy.lib.arraysetops import isin
from sympy import symbols, Poly

from PSID import MatHelper as mh
from .LSSM import LSSM, genRandomGaussianNoise

def extractRangeParamFromSysCode(sysCode, prefix=''):
    regex = re.compile(prefix+"R([\\d\\.e+-]*)_([\\d\\.e+-]*)") #NxR1_10
    matches = re.finditer(regex, sysCode)
    paramVals = None
    pos = None
    for matchNum, match in enumerate(matches, start=1):
        p = match.groups()
        if len(p) == 2 and np.all([pt!='' for pt in p]):
            paramVals = [float(p[0]), float(p[1])] # np.arange(int(p[0]), 1+int(p[1]))
            pos = match.regs
    if paramVals is None:
        regex = re.compile(prefix+"([\\d\\.e+-]*)") #Nx4
        matches = re.finditer(regex, sysCode)
        for matchNum, match in enumerate(matches, start=1):
            p = match.groups()
            paramVals = [float(p[0])] #np.arange(int(p[0]), 1+int(p[0]))
            pos = match.regs
    return paramVals, pos

def getSysSettingsFromSysCode(sysCode):
    sysSettings = {}
    prefixFieldPairs = [
        ('Nx', 'nxVals'), ('N1', 'n1Vals'), ('nu', 'nuVals'),
        ('nxu', 'nxuVals'), ('ny', 'nyVals'), ('nz', 'nzVals')
    ]
    for prefix, settingsField in prefixFieldPairs:
        rng = extractRangeParamFromSysCode(sysCode, prefix=prefix)[0]
        if rng is not None:
            if len(rng)==2 and rng[1] == rng[0]: rng.pop(-1)
            if len(rng)==1: rng.append(1 + rng[0])
            sysSettings[settingsField] = np.arange(int(rng[0]), int(rng[1]))
        else:
            sysSettings[settingsField] = None
    if sysSettings['nuVals'] is None or len(sysSettings['nuVals']) == 0:
        sysSettings['nuVals'] = np.arange(0,1)
    if sysSettings['nxuVals'] is None or len(sysSettings['nxuVals']) == 0:
        sysSettings['nxuVals'] = np.arange(0,1)

    sysSettings['xNScLR'] = extractRangeParamFromSysCode(sysCode, prefix='xNScL')[0]
    sysSettings['yNScLR'] = extractRangeParamFromSysCode(sysCode, prefix='yNScL')[0]

    for p in ['A', 'K', 'Cy', 'Cz']:
        sysSettings[p+'_args'] = {}

    polOrds, pos = extractRangeParamFromSysCode(sysCode, prefix='polO')
    if polOrds is not None:
        regex = r"([A|K|Cy|Cz|]*)" #A
        matches = re.finditer(regex, sysCode[pos[-1][-1]:].split('_')[0])
        for matchNum, match in enumerate(matches):
            if match.groups()[0] != '':
                var_names = match.groups()[0]
        for p in ['A', 'K', 'Cy', 'Cz']:
            if p in var_names:
                sysSettings[p+'_args']['polOrd'] = int(polOrds[0])

    if 'sin' in sysCode:
        regex = r"sin([A|K|Cy|Cz|]*)" #A
        matches = re.finditer(regex, sysCode)
        for matchNum, match in enumerate(matches):
            if match.groups()[0] != '':
                var_names = match.groups()[0]
        for p in ['A', 'K', 'Cy', 'Cz']:
            if p in var_names:
                sysSettings[p+'_args']['sin'] = True
    
    return sysSettings

def generateRandomLinearModel(sysSettings):
    nx = np.random.choice(sysSettings['nxVals'])
    n1 = np.random.choice(sysSettings['n1Vals'][sysSettings['n1Vals']<=nx])
    nu = np.random.choice(sysSettings['nuVals'])
    nxu = np.random.choice(sysSettings['nxuVals'])
    ny = np.random.choice(sysSettings['nyVals'])
    nz = np.random.choice(sysSettings['nzVals'])

    if 'S0' not in sysSettings:
        sysSettings['S0'] = False

    if nu > 0:
        sysU = LSSM(state_dim=nxu, output_dim=nu, input_dim=0)   # Input model
    else:
        sysU = None
    s = LSSM(state_dim=nx, output_dim=ny, input_dim=nu, randomizationSettings={'n1': n1, 'S0': sysSettings['S0']})

    zDims = np.array([])
    if n1 > 0: # Determine dimensions used for z
        BLKS = extractDiagonalBlocks(s.A, emptySide='lower', absThr=1e-14)
        groupInds = getBlockIndsFromBLKSArray(BLKS)
        twoBLocks = np.nonzero(BLKS  > 1)[0]
        oneBlocks = np.nonzero(BLKS == 1)[0]
        
        tbCnt = np.min([twoBLocks.size, int(np.floor(n1/2))])
        if oneBlocks.size == 0 and 2*tbCnt < n1: # Odd n1 but no 1x1 blocks
            tbCnt += 1
        for si in range(0, tbCnt):
            groupInd = groupInds[twoBLocks[si]]
            blockZDims = [*range(groupInd[0], groupInd[1])]  
            zDims = np.concatenate((zDims, blockZDims))
        if len(zDims) > n1:
            zDims = zDims[:-1]
        si = -1
        while len(zDims) < n1:
            si += 1
            groupInd = groupInds[oneBlocks[si]]
            blockZDims = [*range(groupInd[0], groupInd[1])]  
            zDims = np.concatenate((zDims, blockZDims))
        zDims = np.array(zDims, dtype=int)

        # Move z-dims to the top
        I = np.eye(nx)
        E = np.concatenate( (I[zDims, :], I[~np.isin(np.arange(nx), zDims), :]), axis=0 )
        s.applySimTransform(E)
        zDims = np.array(np.arange(zDims.size), dtype=int)

    Cz1 = np.random.randn(nz, n1)
    Cz = np.zeros((nz, nx))
    if n1 > 0:
        Cz[:, zDims] = Cz1
    Dz = np.random.randn(nz, nu)
    s.changeParams({
        'Cz': Cz, 
        'Dz': Dz, 
        'zDims': zDims+1 # plus 1 to be consistent with Matlab indices for zDims in simulated systems
    })

    if 'xNScLR' in sysSettings and sysSettings['xNScLR'] is not None:
        rng = copy.copy(sysSettings['xNScLR'])
        rngL = list(np.log10(rng))
        if len(rngL) == 1: rngL.append(rngL[0])
        sc = 10 ** ( np.random.rand()*np.diff(rngL) + rngL[0] )
        s.changeParams({'Q': sc**2 * s.Q, 'S': sc * s.S})

    if 'yNScLR' in sysSettings and sysSettings['yNScLR'] is not None:
        rng = copy.copy(sysSettings['yNScLR'])
        rngL = list(np.log10(rng))
        if len(rngL) == 1: rngL.append(rngL[0])
        sc = 10 ** ( np.random.rand()*np.diff(rngL) + rngL[0] )
        s.changeParams({'R': sc**2 * s.R, 'S': sc * s.S})

    return s, sysU

def generateRandomModel(sysSettings):
    s, sysU = generateRandomLinearModel(sysSettings)

    for p_name in ['A', 'K', 'Cy', 'Cz']:
        p_args = sysSettings[p_name+'_args']
        if 'polOrd' in p_args or 'sin' in p_args and not isinstance(s, SSM):
            sOrig = copy.deepcopy(s)
            s = SSM(lssm=sOrig)
            break
    for p_name in ['A', 'K', 'Cy', 'Cz']:
        p_args = sysSettings[p_name+'_args']
        if p_name == 'Cy':
            p_name = 'C'
        pOld = getattr(s, p_name)
        n_out, n_in = pOld.shape
        in_sym_names = ','.join(['x{}'.format(ii) for ii in range(n_in)])
        in_syms = symbols(in_sym_names)
        if not isinstance(in_syms, tuple):
            in_syms = (in_syms, )
        paramVal = [0 for io in range(n_out)]
        if 'polOrd' in p_args: # Add polynomial functions
            polOrd = p_args['polOrd']
            for io in range(n_out):
                pValThis = paramVal[io]
                numTerms = np.random.randint(1,10)
                for t in range(numTerms):
                    weight = np.random.randn()
                    termVal = weight
                    itemInds = np.array(n_in)
                    while np.all(itemInds == n_in): # We want all outputs to somehow depend on inputs
                        itemInds = np.random.randint(n_in+1, size=polOrd)
                    itemIndsU, iterIndsCount = np.unique(itemInds, return_counts=True)
                    for itemInd, cnt in zip(itemIndsU, iterIndsCount):
                        if itemInd < len(in_syms):
                            termVal *= in_syms[itemInd] ** cnt
                    pValThis += termVal
                paramVal[io] = pValThis.as_poly()
        if 'sin' in p_args:  # Add trigonometric functions
            Y, X, Z = s.generateRealization(1000, return_z=True, random_x0=False) # Just to get a range of params
            if p_name in ['Cy', 'Cz', 'A']:
                in_range = np.percentile(X, 97.5, axis=0) - np.percentile(X, 2.5, axis=0)
            elif p_name in ['K']:
                in_range = np.percentile(Y, 97.5, axis=0) - np.percentile(Y, 2.5, axis=0)
            else:
                in_range = 2*np.pi * np.ones(n_in)
            scale = 2*np.pi/in_range  # To see one full period of sin
            from sympy import sin
            for io in range(n_out):
                paramValThis = paramVal[io]
                if paramValThis == 0:
                    paramVal[io] = sin(scale[0]*in_syms[0])
                else:
                    paramVal[io] = sin(scale[0]*paramValThis)        
        if 'polOrd' in p_args or 'sin' in p_args:
            paramVal = [pValThis.as_poly() for pValThis in paramVal]
            s.changeParamsIsolated({p_name: paramVal})

    return s, sysU
