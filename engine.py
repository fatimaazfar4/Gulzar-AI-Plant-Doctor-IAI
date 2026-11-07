"""
engine.py  -  Gulzar-AI inference engine
-----------------------------------------
Forward chaining + Certainty Factors (CF) + explanation trace.

Pipeline:
    form inputs --build_facts()--> working memory (set of facts)
    working memory --run_inference()--> ranked diagnoses + "why" trace

Forward chaining:
    Repeat passes over the rule list. In each pass, every rule whose
    conditions are satisfied by working memory "fires" (once). Firing adds a
    new fact (derived-fact rule) or evidence for a diagnosis (diagnosis rule),
    which can trigger more rules in the next pass. Stop when a full pass
    fires nothing (fixed point).

Certainty factor combination (positive evidence, MYCIN style):
    CF_combined = CF_old + CF_new * (1 - CF_old)
"""
from dataclasses import dataclass, field
from typing import Dict, List, Set

from knowledge_base import RULES, DIAGNOSES, Rule


# --------------------------------------------------------------------------
# 1. Turn UI form inputs into facts
# --------------------------------------------------------------------------
def build_facts(form: dict) -> Set[str]:
    """
    form keys (all optional except plant):
      plant, location, setting, symptoms (list), extras (list),
      watering, drainage, soil_feel, fertilizer, pot_size, season,
      humidity, airflow, water_source, sun_hours, temperature
    """
    facts: Set[str] = set()

    if form.get("plant"):
        facts.add(f"plant_{form['plant']}")
    if form.get("location"):
        facts.add(f"loc_{form['location']}")
    if form.get("setting"):
        facts.add(f"loc_{form['setting']}")

    facts.update(form.get("symptoms", []))
    facts.update(form.get("extras", []))

    simple_prefix = {
        "watering": "water_",
        "drainage": "drainage_",
        "soil_feel": "soil_",
        "season": "season_",
        "humidity": "humidity_",
        "airflow": "airflow_",
        "water_source": "water_",
    }
    for key, prefix in simple_prefix.items():
        if form.get(key):
            facts.add(prefix + form[key])

    if form.get("fertilizer"):
        facts.add("fert_" + form["fertilizer"])
    if form.get("pot_size") == "small":
        facts.add("pot_small")

    # numeric inputs -> threshold facts (crisp "fuzzification")
    sun = form.get("sun_hours")
    if sun is not None:
        if sun < 3:
            facts.add("sun_lt3")
        if sun >= 6:
            facts.add("sun_6plus")

    t = form.get("temperature")
    if t is not None:
        if t >= 28:
            facts.add("temp_28plus")
        if t >= 35:
            facts.add("temp_35plus")
        if t >= 38:
            facts.add("temp_38plus")
        if t >= 40:
            facts.add("temp_40plus")
        if t <= 10:
            facts.add("temp_cold")

    # fert_never_or_old and water_irregular etc. already come as raw ids
    return facts


# --------------------------------------------------------------------------
# 2. Result structures
# --------------------------------------------------------------------------
@dataclass
class FiredRule:
    rule_id: str
    description: str
    cf: float
    cycle: int
    category: str


@dataclass
class Diagnosis:
    id: str
    name: str
    category: str
    cf: float = 0.0
    evidence: List[FiredRule] = field(default_factory=list)

    @property
    def percent(self) -> int:
        return round(self.cf * 100)

    @property
    def level(self) -> str:
        if self.cf >= 0.85:
            return "Very likely"
        if self.cf >= 0.70:
            return "Likely"
        return "Possible"


@dataclass
class InferenceResult:
    diagnoses: List[Diagnosis]
    derived_facts: List[str]
    trace: List[FiredRule]
    cycles: int
    input_facts: Set[str]


# --------------------------------------------------------------------------
# 3. Forward chaining
# --------------------------------------------------------------------------
def _matches(rule: Rule, wm: Set[str]) -> bool:
    if any(f not in wm for f in rule.if_all):
        return False
    if rule.if_any and not any(f in wm for f in rule.if_any):
        return False
    if any(f in wm for f in rule.if_none):
        return False
    return True


def combine_cf(old: float, new: float) -> float:
    return old + new * (1 - old)


def run_inference(facts: Set[str]) -> InferenceResult:
    wm: Set[str] = set(facts)
    pending: List[Rule] = list(RULES)
    trace: List[FiredRule] = []
    results: Dict[str, Diagnosis] = {}
    derived: List[str] = []

    cycle = 0
    changed = True
    while changed:
        changed = False
        cycle += 1
        for rule in list(pending):          # conflict resolution = rule order
            if not _matches(rule, wm):
                continue
            pending.remove(rule)            # each rule fires only once
            changed = True
            fired = FiredRule(rule.id, rule.description, rule.cf, cycle, rule.category)
            trace.append(fired)

            if rule.kind == "fact":
                if rule.concludes not in wm:
                    wm.add(rule.concludes)
                    derived.append(rule.concludes)
            else:
                name, cat = DIAGNOSES[rule.concludes]
                d = results.setdefault(rule.concludes, Diagnosis(rule.concludes, name, cat))
                d.cf = combine_cf(d.cf, rule.cf)
                d.evidence.append(fired)
                wm.add("dx_" + rule.concludes)   # lets later rules chain on it

    ranked = sorted(results.values(), key=lambda d: d.cf, reverse=True)
    return InferenceResult(ranked, derived, trace, cycle, set(facts))


def diagnose(form: dict) -> InferenceResult:
    """One-call helper used by the UI."""
    return run_inference(build_facts(form))


# --------------------------------------------------------------------------
# 4. Command-line demo / self-test:  python engine.py
# --------------------------------------------------------------------------
if __name__ == "__main__":
    from knowledge_base import kb_stats

    print("Knowledge base:", kb_stats(), "\n")

    demo_cases = {
        "Tomato in monsoon, overwatered": dict(
            plant="tomato", location="pot", setting="balcony",
            symptoms=["yellow_lower", "water_soaked"],
            watering="daily", soil_feel="soggy", season="monsoon",
            humidity="high", airflow="poor", temperature=31, sun_hours=5),
        "Rooftop chili in May heat": dict(
            plant="chili", location="pot", setting="rooftop",
            symptoms=["wilting_midday", "bud_drop"],
            watering="every_2_3_days", soil_feel="dry", season="summer",
            humidity="low", temperature=41, sun_hours=8),
        "Karachi rose, tanker water, sea breeze": dict(
            plant="rose", location="pot", setting="balcony",
            symptoms=["brown_tips", "brown_edges", "white_crust"],
            extras=["sea_breeze"], water_source="tanker",
            season="mild", temperature=30, sun_hours=6),
    }
    for title, form in demo_cases.items():
        res = diagnose(form)
        print(f"=== {title}  (cycles: {res.cycles}, rules fired: {len(res.trace)})")
        for d in res.diagnoses[:4]:
            rules = ", ".join(e.rule_id for e in d.evidence)
            print(f"  {d.percent:3d}%  {d.name:<45} [{rules}]")
        print()