import math
import yaml
from typing import Dict, List, Optional, Any
from pathlib import Path

from models.enums import GoalType, SessionType


class GoalNormalizer:
    """Service for normalizing hierarchical goal sliders using sigmoid functions."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize with configuration from YAML file."""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "goal_normalization.yaml"
        
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load normalization configuration from YAML file."""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            # Return default configuration if file not found
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default normalization configuration."""
        return {
            "slider_normalization": {
                "primary": {
                    "steepness": 6.0,
                    "midpoint": 0.5,
                    "influence_range": 0.8
                },
                "secondary_sliders": {
                    "hypertrophy_fat_loss": {
                        "base_weight": 0.5,
                        "strength_influence": 0.3,
                        "endurance_influence": -0.2,
                        "steepness": 4.0,
                        "midpoint": 0.5
                    },
                    "power_mobility": {
                        "base_weight": 0.5,
                        "strength_influence": 0.4,
                        "endurance_influence": -0.3,
                        "steepness": 5.0,
                        "midpoint": 0.5
                    }
                }
            },
            "goal_hierarchy": {
                "primary_goal_weight": 0.6,
                "secondary_goal_weight": 0.4
            },
            "session_probability_modifiers": {
                "strength_bias": {
                    "resistance_accessory": 1.2,
                    "resistance_circuits": 1.1,
                    "hyrox_style": 0.8,
                    "mobility_only": 0.7,
                    "cardio_only": 0.6
                },
                "endurance_bias": {
                    "resistance_accessory": 0.8,
                    "resistance_circuits": 1.1,
                    "hyrox_style": 1.3,
                    "mobility_only": 0.9,
                    "cardio_only": 1.4
                }
            },
            "validation": {
                "mathematical_constraints": {
                    "min_normalized_value": 0.05,
                    "max_normalized_value": 0.95
                }
            }
        }
    
    def normalize_primary_slider(self, primary_value: float) -> Dict[str, float]:
        """
        Normalize the primary slider and calculate influence on secondary sliders.
        
        Args:
            primary_value: Primary slider value (0.0 = endurance, 1.0 = strength)
            
        Returns:
            Dictionary with strength_bias, endurance_bias, and influence metrics
        """
        config = self.config["slider_normalization"]["primary"]
        k = config["steepness"]
        x0 = config["midpoint"]
        
        # Calculate sigmoid-based influence
        strength_influence = 1 / (1 + math.exp(-k * (primary_value - x0)))
        endurance_influence = 1 - strength_influence
        
        return {
            "primary_strength": primary_value,
            "strength_bias": strength_influence,
            "endurance_bias": endurance_influence,
            "influence_range": config["influence_range"]
        }
    
    def normalize_secondary_slider(
        self, 
        slider_name: str, 
        base_value: float, 
        primary_influence: Dict[str, float]
    ) -> float:
        """
        Normalize a secondary slider based on primary slider influence.
        
        Args:
            slider_name: Name of secondary slider (e.g., 'hypertrophy_fat_loss')
            base_value: Base slider value (0.0 to 1.0)
            primary_influence: Influence metrics from primary slider
            
        Returns:
            Normalized slider value (clamped to 0.05-0.95)
        """
        config = self.config["slider_normalization"]["secondary_sliders"][slider_name]
        
        # Get influence factors
        strength_influence = config["strength_influence"]
        endurance_influence = config["endurance_influence"]
        
        # Calculate adjustment based on primary slider influence
        strength_bias = primary_influence["strength_bias"]
        endurance_bias = primary_influence["endurance_bias"]
        
        adjustment = (strength_bias * strength_influence) + (endurance_bias * endurance_influence)
        
        # Apply sigmoid smoothing
        k = config["steepness"]
        x0 = config["midpoint"]
        base_sigmoid = 1 / (1 + math.exp(-k * (base_value - x0)))
        
        # Combine base value with influence adjustment
        normalized_value = base_sigmoid + (adjustment * 0.2)  # Scale influence
        
        # Clamp to valid range
        constraints = self.config["validation"]["mathematical_constraints"]
        return max(constraints["min_normalized_value"], 
                  min(constraints["max_normalized_value"], normalized_value))
    
    def normalize_all_sliders(self, goals: Dict[str, float]) -> Dict[str, float]:
        """
        Normalize all sliders using hierarchical influence.
        
        Args:
            goals: Dictionary with primary_slider, hypertrophy_fat_loss, power_mobility
            
        Returns:
            Dictionary with all normalized values
        """
        primary_value = goals["primary_slider"]
        
        # Normalize primary slider
        primary_influence = self.normalize_primary_slider(primary_value)
        
        # Normalize secondary sliders
        normalized_hfl = self.normalize_secondary_slider(
            "hypertrophy_fat_loss", 
            goals["hypertrophy_fat_loss"], 
            primary_influence
        )
        
        normalized_pm = self.normalize_secondary_slider(
            "power_mobility", 
            goals["power_mobility"], 
            primary_influence
        )
        
        return {
            "primary_strength": primary_value,
            "normalized_hypertrophy_fat_loss": normalized_hfl,
            "normalized_power_mobility": normalized_pm,
            "strength_bias": primary_influence["strength_bias"],
            "endurance_bias": primary_influence["endurance_bias"]
        }
    
    def calculate_session_probabilities(self, normalized_goals: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate session type probabilities based on normalized goals.
        
        Args:
            normalized_goals: Normalized goal weights
            
        Returns:
            Dictionary mapping session types to their probabilities
        """
        # Get bias-based modifiers
        strength_bias = normalized_goals["strength_bias"]
        endurance_bias = normalized_goals["endurance_bias"]
        
        # Get session probability modifiers
        modifiers = self.config["session_probability_modifiers"]
        
        # Calculate weighted probabilities
        session_probs = {}
        for session_type in SessionType:
            session_key = session_type.value
            
            # Base probability from goal mapping (would come from config)
            base_prob = 0.2  # Equal base probability for all
            
            # Apply bias modifiers
            strength_modifier = modifiers["strength_bias"].get(session_key, 1.0)
            endurance_modifier = modifiers["endurance_bias"].get(session_key, 1.0)
            
            # Weighted combination
            weighted_prob = (strength_bias * strength_modifier + 
                           endurance_bias * endurance_modifier) * base_prob
            
            session_probs[session_key] = weighted_prob
        
        # Normalize probabilities to sum to 1.0
        total_prob = sum(session_probs.values())
        if total_prob > 0:
            session_probs = {k: v/total_prob for k, v in session_probs.items()}
        
        return session_probs
    
    def validate_goal_consistency(self, goals: Dict[str, float]) -> List[str]:
        """
        Validate goal configuration for mathematical consistency.
        
        Args:
            goals: Goal configuration dictionary
            
        Returns:
            List of validation warnings/errors
        """
        warnings = []
        
        # Check slider ranges
        for slider_name, value in goals.items():
            if not 0.0 <= value <= 1.0:
                warnings.append(f"{slider_name} value {value} is outside valid range [0.0, 1.0]")
        
        # Check for extreme configurations
        primary_value = goals.get("primary_slider", 0.5)
        if primary_value < 0.1 or primary_value > 0.9:
            warnings.append("Primary slider is at extreme value - may limit session variety")
        
        # Check secondary slider consistency
        hfl_value = goals.get("hypertrophy_fat_loss", 0.5)
        pm_value = goals.get("power_mobility", 0.5)
        
        if (primary_value > 0.7 and hfl_value < 0.3 and pm_value < 0.3):
            warnings.append("High strength focus with low hypertrophy and power may be suboptimal")
        
        if (primary_value < 0.3 and hfl_value > 0.7 and pm_value > 0.7):
            warnings.append("High endurance focus with high hypertrophy and power may conflict")
        
        return warnings
    
    def recommend_program_length(self, normalized_goals: Dict[str, float]) -> int:
        """
        Recommend program length based on normalized goals.
        
        Args:
            normalized_goals: Normalized goal weights
            
        Returns:
            Recommended program length in weeks
        """
        strength_bias = normalized_goals["strength_bias"]
        endurance_bias = normalized_goals["endurance_bias"]
        
        # Get recommendations from config
        recommendations = self.config.get("program_length_recommendations", {})
        
        # Calculate weighted recommendation
        if strength_bias > endurance_bias:
            # Strength-focused programs tend to be longer
            base_recommendation = 12
        else:
            # Endurance-focused programs can be shorter
            base_recommendation = 8
        
        # Apply secondary goal adjustments
        hypertrophy_weight = normalized_goals.get("normalized_hypertrophy_fat_loss", 0.5)
        power_weight = normalized_goals.get("normalized_power_mobility", 0.5)
        
        if hypertrophy_weight > 0.7:
            base_recommendation += 1  # Longer for hypertrophy focus
        if power_weight > 0.7:
            base_recommendation += 0  # Standard length for power focus
        
        # Clamp to valid range
        return max(8, min(12, base_recommendation))