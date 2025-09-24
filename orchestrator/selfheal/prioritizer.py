import math, random, time
class Prioritizer:
    def score(self, meta):
        # meta: {recent_failures:int, flakiness:float[0..1], code_diff_risk:float[0..1]}
        rf = meta.get('recent_failures', 0)
        fl = meta.get('flakiness', 0.0)
        cd = meta.get('code_diff_risk', 0.0)
        # Weighted score; higher = more urgent
        return 0.6*rf + 0.3*fl*10 + 0.4*cd*10

    def order(self, tests_meta):
        # tests_meta: dict test_name -> meta
        ranked = sorted(tests_meta.items(), key=lambda kv: self.score(kv[1]), reverse=True)
        return [name for name,_ in ranked]
