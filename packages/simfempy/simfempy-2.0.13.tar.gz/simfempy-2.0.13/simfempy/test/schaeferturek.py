import sys
from os import path
simfempypath = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.insert(0,simfempypath)

from simfempy.tools.comparemethods import CompareMethods
from simfempy.applications.navierstokes import NavierStokes
from simfempy.examples.incompflow import schaeferTurek


def postproc(infos):
    print(f"{infos['bdrynflux']=}")

def run(paramsdict, applicationargs={}, **kwargs):
    niter = kwargs.pop('niter', 3)
    h1 = kwargs.pop('h1', 1)
    h = [h1*0.5**i for i in range(niter)]
    mesh, data = schaeferTurek(h[0])
    applicationargs['problemdata'] = data
    sims = {}
    for pname, params in paramsdict.items():
        for param in params:
            name = param
            applicationargs[pname] = param
            sims[name] = NavierStokes(**applicationargs)
    # raise ValueError(f"{kwargs=}")
    def createMesh(h): return schaeferTurek(h)[0]
    kwargs['postproc'] = postproc
    comp = CompareMethods(sims, createMesh=createMesh, **kwargs)
    naps, pname, params, infos = comp.compare(h=h)

#================================================================#
if __name__ == '__main__':
    paramsdict = {'convmethod': ['lps','supg']}
    run(paramsdict, niter=1)