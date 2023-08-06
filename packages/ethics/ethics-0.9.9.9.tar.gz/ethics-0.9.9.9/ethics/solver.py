#from pysat.solvers import Solver
from ethics.language import *
from ethics.tools import *
from ethics.tools import subToAtoms

def theorySAT(cand_model):
    """ A Solver for Simple Causal Agency Logic
    
    Keyword arguments:
    cand_model --- A list of literals to be checked for consistency
    """
    for m in cand_model:
        if isinstance(m, Good):
            if Bad(m.f1) in cand_model:
                #print("good:bad")
                return False
            if Neutral(m.f1) in cand_model:
                #print("good:neutral")
                return False
        if isinstance(m, Bad):
            if Good(m.f1) in cand_model:
                #print("bad:good")
                return False
            if Neutral(m.f1) in cand_model:
                #print("bad:neutral")
                return False
        if isinstance(m, Neutral):
            if Good(m.f1) in cand_model:
                #print("neutral:good")
                return False
            if Bad(m.f1) in cand_model:
                #print("neutral:bad")
                return False
        if isinstance(m, Causes):
            if Not(m.f1).nnf() in cand_model:
                #print("causes: notf1")
                return False
            if Not(m.f2).nnf() in cand_model:
                #print("causes: notf2")
                return False
            if m.f1 != m.f2 and Causes(m.f2, m.f1) in cand_model:
                #print("causes: symmetry", m)
                return False
            if m == Causes(m.f1, Not(m.f1).nnf()):
                #print("causes: notff")
                return False
            if Causes(m.f1, Not(m.f2).nnf()) in cand_model:
                #print("causes: f1notf2")
                return False
            if Causes(Not(m.f1).nnf(), m.f2) in cand_model:
                #print("causes: notf1nf2")
                return False
        if isinstance(m, Not) and isinstance(m.f1, Causes) and m.f1.f1 == m.f1.f2 and m.f1 in cand_model:
            #print("notcauses", m)
            return False
        if isinstance(m, Not) and isinstance(m.f1, Eq) and m.f1.f1 == m.f1.f2:
            #print("noteq")
            return False
        if isinstance(m, Not) and isinstance(m.f1, Eq) and m.f1.f1 == m.f1.f2:
            return False
        if isinstance(m, Not) and isinstance(m.f1, GEq) and m.f1.f1 == m.f1.f2:
            return False
        if isinstance(m, Eq):
            if Gt(m.f1, m.f2) in cand_model:
                #print("eqgt")
                return False
        if isinstance(m, GEq):
            if Gt(m.f2, m.f1) in cand_model:
                #print("geqgt", m)
                return False
        if isinstance(m, Gt):
            if m.f1 == m.f2:
                return False
            if Gt(m.f2, m.f1) in cand_model:
                return False
            if GEq(m.f2, m.f1) in cand_model:
                return False
            if Eq(m.f1, m.f2) in cand_model:
                return False
            if Eq(m.f2, m.f1) in cand_model:
                return False
        if isinstance(m, Better):
            if m.f1 == m.f2:
                return False
            if Better(m.f2, m.f1) in cand_model:
                return False
            for n in cand_model:
                if isinstance(n, Better):
                    if m.f2 == n.f1:
                        if Not(Better(m.f1, n.f2)) in cand_model:
                            return False
    
    return True
    
    
def smtAllModels(formula):
    formula = subToAtoms(formula)
    s = Solver()
    s.append_formula(formula)
    models = []
    for mod in s.enum_models():
        #f = mapBackToFormulae(mod, m)
        if theorySAT(mod):
            models.append(mod)
    #s.delete()
    return models


def satisfiable(formula):
    if(isinstance(formula, list)):
        formula = Formula.makeConjunction(formula)

    formula = subToAtoms(formula)
    #d, m = formula.dimacs()
    s = Solver()
    s.append_formula(formula)
    for mod in s.enum_models():
        #f = mapBackToFormulae(mod, m)
        if theorySAT(mod):
            #s.delete()
            return True
    #s.delete()
    return False


class Solver:
    def __init__(self):
        self.formulae = []
        self.tree = []

    def append_formula(self, f):
        self.formulae.append(f.nnf())

    def enum_models(self):
        models = []
        while True:
            m = self.get_model()
            if m is False:
                return models
            models.append(m)
            self.formulae.append(Not(Formula.makeConjunction(m)))
            #print("append", Not(Formula.makeConjunction(m)))
            #print("formulae", self.formulae)

    def get_model(self):
        self.tree = []
        self.tree.append(Branch(self, list(self.formulae)))
        self.expanded = []
        for branch in self.tree:
            branch.saturate()
            if branch.consistent():
                #print("branch", branch)
                #print("extr model", branch.extractModel())
                return branch.extractModel()
        return False


class Branch:
    def __init__(self, solver, formulae):
        self.formulae = formulae
        self.solver = solver
        self.expanded = []

    def __eq__(self, other):
        if isinstance(other, Branch):
            for i in self.formulae:
                if i not in other.formulae:
                    return False
            for i in other.formulae:
                if i not in self.formulae:
                    return False
            return True
        return False

    def isCALLiteral(self, f):
        if isinstance(f, And) or isinstance(f, Or) or isinstance(f, Impl) or isinstance(f, BiImpl):
            return False
        if isinstance(f, Not):
            if isinstance(f.f1, And) or isinstance(f.f1, Or) or isinstance(f.f1, Impl) or isinstance(f.f1, BiImpl) or isinstance(f.f1, Not):
                return False
        return True

    def extractModel(self):
        return [e for e in self.formulae if self.isCALLiteral(e)]

    def consistent(self):
        for f in self.formulae:
            if Not(f) in self.formulae:
                return False
        return True

    def appendNew(self, formula):
        if formula not in self.formulae:
            self.formulae.append(formula)

    def equalBranchExists(self, branch):
        for b in self.solver.tree:
            if b == branch:
                return True
        return False

    def appendNewBranch(self, formula):
        newBranch = Branch(self.solver, list(self.formulae+[formula]))
        newBranch.expanded = list(self.expanded)
        #if not self.equalBranchExists(newBranch):
        #print("new branch", len(self.solver.tree))
        self.solver.tree.append(newBranch)

    def saturate(self):
        for f in self.formulae:
            if not self.consistent():
                #print("incons", self.formulae)
                return False
            if f not in self.expanded:
                self.expanded.append(f)
                if isinstance(f, And):
                    self.appendNew(f.f1)
                    self.appendNew(f.f2)
                elif isinstance(f, Or):
                    self.appendNewBranch(f.f2)
                    self.appendNew(f.f1)
                    """                    
                    self.appendNewBranch(And(Not(f.f1), f.f2))
                    self.appendNewBranch(And(f.f1, f.f2))
                    self.appendNew(f.f1)
                    self.appendNew(Not(f.f2))
                    """
                elif isinstance(f, Impl):
                    self.appendNew(Or(Not(f.f1), f.f2))
                elif isinstance(f, BiImpl):
                    self.appendNew(And(Impl(f.f1, f.f2), Impl(f.f2, f.f1)))
                elif isinstance(f, Not) and isinstance(f.f1, Not):
                    self.appendNew(f.f1.f1)
                elif isinstance(f, Not) and isinstance(f.f1, And):
                    self.appendNew(Or(Not(f.f1.f1), Not(f.f1.f2)))
                elif isinstance(f, Not) and isinstance(f.f1, Or):
                    self.appendNew(Not(f.f1.f1))
                    self.appendNew(Not(f.f1.f2))
                elif isinstance(f, Not) and isinstance(f.f1, Impl):
                    self.appendNew(f.f1.f1)
                    self.appendNew(Not(f.f1.f2))
                elif isinstance(f, Not) and isinstance(f.f1, BiImpl):
                    self.appendNew(Or(Not(Impl(f.f1.f1, f.f1.f2)), Not(Impl(f.f1.f2, f.f1.f1))))
        
