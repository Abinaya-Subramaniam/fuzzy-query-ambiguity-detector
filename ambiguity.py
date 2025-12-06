import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class AdvancedFuzzyAmbiguitySystem:
    def __init__(self):
        self.setup_fuzzy_system()
    
    def setup_fuzzy_system(self):
        
        self.length = ctrl.Antecedent(np.arange(0, 101, 1), 'length')
        self.length['very_short'] = fuzz.trimf(self.length.universe, [0, 0, 20])
        self.length['short'] = fuzz.trimf(self.length.universe, [10, 30, 50])
        self.length['medium'] = fuzz.trimf(self.length.universe, [40, 60, 80])
        self.length['long'] = fuzz.trimf(self.length.universe, [70, 90, 100])
        
        self.vague_ratio = ctrl.Antecedent(np.arange(0, 101, 1), 'vague_ratio')
        self.vague_ratio['low'] = fuzz.trimf(self.vague_ratio.universe, [0, 0, 30])
        self.vague_ratio['medium'] = fuzz.trimf(self.vague_ratio.universe, [20, 50, 80])
        self.vague_ratio['high'] = fuzz.trimf(self.vague_ratio.universe, [70, 100, 100])
        
        self.specificity = ctrl.Antecedent(np.arange(0, 101, 1), 'specificity')
        self.specificity['low'] = fuzz.trimf(self.specificity.universe, [0, 0, 40])
        self.specificity['medium'] = fuzz.trimf(self.specificity.universe, [30, 50, 70])
        self.specificity['high'] = fuzz.trimf(self.specificity.universe, [60, 100, 100])
        
        self.question_clarity = ctrl.Antecedent(np.arange(0, 101, 1), 'question_clarity')
        self.question_clarity['poor'] = fuzz.trimf(self.question_clarity.universe, [0, 0, 40])
        self.question_clarity['fair'] = fuzz.trimf(self.question_clarity.universe, [30, 50, 70])
        self.question_clarity['good'] = fuzz.trimf(self.question_clarity.universe, [60, 100, 100])
        
        self.ambiguity = ctrl.Consequent(np.arange(0, 101, 1), 'ambiguity')
        self.ambiguity['low'] = fuzz.trimf(self.ambiguity.universe, [0, 0, 30])
        self.ambiguity['medium'] = fuzz.trimf(self.ambiguity.universe, [20, 50, 80])
        self.ambiguity['high'] = fuzz.trimf(self.ambiguity.universe, [70, 100, 100])
        
        self.create_rules()
        
        self.control_system = ctrl.ControlSystem(self.rules)
        self.simulator = ctrl.ControlSystemSimulation(self.control_system)
    
    def create_rules(self):
        self.rules = [
            ctrl.Rule(
                self.length['very_short'] & self.vague_ratio['high'],
                self.ambiguity['high']
            ),
            
            ctrl.Rule(
                self.length['very_short'] & self.specificity['low'],
                self.ambiguity['high']
            ),
            ctrl.Rule(
                self.length['very_short'] & self.specificity['low'],
                self.ambiguity['high']
            ),
            
            ctrl.Rule(
                self.length['long'] & self.specificity['high'],
                self.ambiguity['low']
            ),
            
            ctrl.Rule(
                self.question_clarity['good'],
                self.ambiguity['low']
            ),
            
            ctrl.Rule(
                self.question_clarity['poor'],
                self.ambiguity['high']
            ),
            
            ctrl.Rule(
                self.vague_ratio['high'],
                self.ambiguity['high']
            ),
            
            ctrl.Rule(
                self.length['medium'] & self.specificity['medium'] & self.vague_ratio['medium'],
                self.ambiguity['medium']
            ),
            
            ctrl.Rule(
                self.length['short'] & self.specificity['high'] & self.question_clarity['good'],
                self.ambiguity['medium']
            ),
            
            ctrl.Rule(
                self.length['long'] & self.vague_ratio['high'],
                self.ambiguity['high']
            ),
            
            ctrl.Rule(
                self.specificity['high'] & self.question_clarity['good'],
                self.ambiguity['low']
            )
        ]
    
    def compute_ambiguity(self, length_val, vague_ratio_val, specificity_val, clarity_val):
        try:
            self.simulator.input['length'] = float(length_val)
            self.simulator.input['vague_ratio'] = float(vague_ratio_val)
            self.simulator.input['specificity'] = float(specificity_val)
            self.simulator.input['question_clarity'] = float(clarity_val)
            
            self.simulator.compute()
            return float(self.simulator.output['ambiguity'])
            
        except Exception as e:
            print(f"Fuzzy system error: {e}")
            
            weights = {
                'length': 0.2,
                'vague_ratio': 0.3,
                'specificity': 0.3,
                'question_clarity': 0.2
            }
            
            length_score = (100 - length_val) * weights['length']  
            vague_score = vague_ratio_val * weights['vague_ratio']
            specificity_score = (100 - specificity_val) * weights['specificity']  
            clarity_score = (100 - clarity_val) * weights['question_clarity']  
            
            total_score = length_score + vague_score + specificity_score + clarity_score
            
            return min(max(total_score, 0), 100)

fuzzy_system = AdvancedFuzzyAmbiguitySystem()