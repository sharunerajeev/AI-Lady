"""
Tests for the recommendation engine and related functionality
"""

import pytest
import json
from app.services.recommendation_service import RecommendationEngine
from data.product_catalog import PRODUCT_CATALOG, QUESTIONNAIRES


class TestRecommendationEngine:
    """Test suite for the recommendation engine"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.engine = RecommendationEngine()
    
    def test_get_questionnaire_valid_type(self):
        """Test getting questionnaire for valid insurance type"""
        questionnaire = self.engine.get_questionnaire("health_insurance")
        assert questionnaire is not None
        assert "questions" in questionnaire
        assert len(questionnaire["questions"]) > 0
    
    def test_get_questionnaire_invalid_type(self):
        """Test getting questionnaire for invalid insurance type"""
        questionnaire = self.engine.get_questionnaire("invalid_type")
        assert questionnaire is None
    
    def test_validate_answer_number_valid(self):
        """Test validation of valid number answer"""
        is_valid, error = self.engine.validate_answer(
            "health_insurance", "age", "30"
        )
        assert is_valid is True
        assert error is None
    
    def test_validate_answer_number_below_min(self):
        """Test validation of number below minimum"""
        is_valid, error = self.engine.validate_answer(
            "health_insurance", "age", "10"
        )
        assert is_valid is False
        assert "at least" in error.lower()
    
    def test_validate_answer_number_above_max(self):
        """Test validation of number above maximum"""
        is_valid, error = self.engine.validate_answer(
            "health_insurance", "age", "150"
        )
        assert is_valid is False
        assert "at most" in error.lower()
    
    def test_validate_answer_choice_valid(self):
        """Test validation of valid choice answer"""
        is_valid, error = self.engine.validate_answer(
            "health_insurance", "employment_status", "employed"
        )
        assert is_valid is True
        assert error is None
    
    def test_validate_answer_choice_invalid(self):
        """Test validation of invalid choice answer"""
        is_valid, error = self.engine.validate_answer(
            "health_insurance", "employment_status", "invalid_choice"
        )
        assert is_valid is False
        assert "choose from" in error.lower()
    
    def test_recommend_health_insurance_individual(self):
        """Test health insurance recommendation for individual"""
        requirements = {
            "age": 28,
            "employment_status": "employed",
            "family_size": 1,
            "pre_existing_conditions": "no",
            "budget": 300,
            "coverage_preference": "low_cost"
        }
        
        recommendations = self.engine.recommend_products(
            "health_insurance", requirements
        )
        
        assert len(recommendations) > 0
        # Should recommend Basic plan for individual with low_cost preference
        top_recommendation = recommendations[0]
        assert "Basic" in top_recommendation["product"]["name"]
        assert top_recommendation["score"] > 0
        assert len(top_recommendation["reasons"]) > 0
    
    def test_recommend_health_insurance_family(self):
        """Test health insurance recommendation for family"""
        requirements = {
            "age": 35,
            "employment_status": "employed",
            "family_size": 4,
            "pre_existing_conditions": "no",
            "budget": 800,
            "coverage_preference": "family_benefits"
        }
        
        recommendations = self.engine.recommend_products(
            "health_insurance", requirements
        )
        
        assert len(recommendations) > 0
        # Should recommend Family plan
        top_recommendation = recommendations[0]
        assert "Family" in top_recommendation["product"]["name"]
        assert top_recommendation["match_percentage"] > 60
    
    def test_recommend_health_insurance_pre_existing(self):
        """Test health insurance with pre-existing conditions"""
        requirements = {
            "age": 45,
            "employment_status": "employed",
            "family_size": 1,
            "pre_existing_conditions": "yes",
            "budget": 500,
            "coverage_preference": "comprehensive_coverage"
        }
        
        recommendations = self.engine.recommend_products(
            "health_insurance", requirements
        )
        
        assert len(recommendations) > 0
        # Premium plan should score high for pre-existing conditions
        top_recommendation = recommendations[0]
        assert "Premium" in top_recommendation["product"]["name"]
        assert any("pre-existing" in reason.lower() for reason in top_recommendation["reasons"])
    
    def test_recommend_life_insurance_young_single(self):
        """Test life insurance recommendation for young single person"""
        requirements = {
            "age": 25,
            "dependents": 0,
            "annual_income": 50000,
            "existing_coverage": "no",
            "health_status": "excellent",
            "coverage_goal": "debt_coverage"
        }
        
        recommendations = self.engine.recommend_products(
            "life_insurance", requirements
        )
        
        assert len(recommendations) > 0
        # Basic Term Life should be recommended
        top_recommendation = recommendations[0]
        assert "Basic" in top_recommendation["product"]["name"]
    
    def test_recommend_life_insurance_family_breadwinner(self):
        """Test life insurance for family breadwinner"""
        requirements = {
            "age": 35,
            "dependents": 2,
            "annual_income": 80000,
            "existing_coverage": "no",
            "health_status": "good",
            "coverage_goal": "income_replacement"
        }
        
        recommendations = self.engine.recommend_products(
            "life_insurance", requirements
        )
        
        assert len(recommendations) > 0
        # Family Protection Plan should score high
        assert any("Family" in rec["product"]["name"] for rec in recommendations)
    
    def test_recommend_auto_insurance_new_car(self):
        """Test auto insurance for new car"""
        requirements = {
            "age": 30,
            "driving_experience": 12,
            "accidents_violations": "none",
            "vehicle_count": 1,
            "vehicle_age": "new_0-3_years",
            "vehicle_value": 35000,
            "coverage_need": "full_coverage"
        }
        
        recommendations = self.engine.recommend_products(
            "auto_insurance", requirements
        )
        
        assert len(recommendations) > 0
        # Premium Auto Protection recommended for new expensive car
        top_recommendation = recommendations[0]
        assert "Premium" in top_recommendation["product"]["name"] or "Full Coverage" in top_recommendation["product"]["type"]
    
    def test_recommend_auto_insurance_old_car(self):
        """Test auto insurance for old car"""
        requirements = {
            "age": 25,
            "driving_experience": 7,
            "accidents_violations": "1_violation",
            "vehicle_count": 1,
            "vehicle_age": "very_old_10+_years",
            "vehicle_value": 3000,
            "coverage_need": "minimum_liability"
        }
        
        recommendations = self.engine.recommend_products(
            "auto_insurance", requirements
        )
        
        assert len(recommendations) > 0
        # Basic coverage recommended for old car
        top_recommendation = recommendations[0]
        assert "Basic" in top_recommendation["product"]["name"]
    
    def test_recommend_auto_insurance_multi_vehicle(self):
        """Test auto insurance for multiple vehicles"""
        requirements = {
            "age": 40,
            "driving_experience": 22,
            "accidents_violations": "none",
            "vehicle_count": 3,
            "vehicle_age": "recent_4-7_years",
            "vehicle_value": 25000,
            "coverage_need": "full_coverage"
        }
        
        recommendations = self.engine.recommend_products(
            "auto_insurance", requirements
        )
        
        assert len(recommendations) > 0
        # For 3 vehicles, check if Family Bundle gets recommended
        # The Family Auto Bundle should be in the top 2 recommendations
        top_two_names = [rec["product"]["name"] for rec in recommendations[:2]]
        assert any("Family" in name for name in top_two_names), \
            f"Expected Family Bundle in top 2, got: {top_two_names}"
    
    def test_recommend_home_insurance_basic(self):
        """Test home insurance for basic property"""
        requirements = {
            "property_type": "single-family",
            "property_age": 15,
            "property_value": 200000,
            "location_risk": "no",
            "mortgage": "yes",
            "contents_value": 30000
        }
        
        recommendations = self.engine.recommend_products(
            "home_insurance", requirements
        )
        
        assert len(recommendations) > 0
        assert all(rec["score"] > 0 for rec in recommendations)
    
    def test_recommend_home_insurance_luxury(self):
        """Test home insurance for luxury property"""
        requirements = {
            "property_type": "estate",
            "property_age": 5,
            "property_value": 2000000,
            "location_risk": "no",
            "mortgage": "no",
            "contents_value": 500000
        }
        
        recommendations = self.engine.recommend_products(
            "home_insurance", requirements
        )
        
        assert len(recommendations) > 0
        # Luxury plan should be top recommendation
        top_recommendation = recommendations[0]
        assert "Luxury" in top_recommendation["product"]["name"]
    
    def test_recommend_home_insurance_high_risk(self):
        """Test home insurance for high-risk location"""
        requirements = {
            "property_type": "single-family",
            "property_age": 10,
            "property_value": 400000,
            "location_risk": "yes",
            "mortgage": "yes",
            "contents_value": 50000
        }
        
        recommendations = self.engine.recommend_products(
            "home_insurance", requirements
        )
        
        assert len(recommendations) > 0
        # Premium or Luxury should be recommended for high-risk
        top_recommendation = recommendations[0]
        assert "Premium" in top_recommendation["product"]["name"] or "Luxury" in top_recommendation["product"]["name"]
    
    def test_age_out_of_range(self):
        """Test that products outside age range are not recommended"""
        requirements = {
            "age": 75,  # Beyond most health insurance limits
            "employment_status": "retired",
            "family_size": 1,
            "pre_existing_conditions": "yes",
            "budget": 500
        }
        
        recommendations = self.engine.recommend_products(
            "health_insurance", requirements
        )
        
        # Should either have no recommendations or only those that accept age 75
        for rec in recommendations:
            eligibility = rec["product"]["eligibility"]
            assert eligibility["min_age"] <= 75 <= eligibility["max_age"]
    
    def test_generate_comparison(self):
        """Test generating product comparison"""
        # First get some recommendations
        requirements = {
            "age": 30,
            "employment_status": "employed",
            "family_size": 1,
            "pre_existing_conditions": "no",
            "budget": 300
        }
        
        recommendations = self.engine.recommend_products(
            "health_insurance", requirements
        )
        
        # Generate comparison
        comparison = self.engine.generate_comparison(
            [rec["product"] for rec in recommendations[:2]]
        )
        
        assert "products" in comparison
        assert "features" in comparison
        assert len(comparison["products"]) == 2
        assert len(comparison["features"]) > 0
    
    def test_all_insurance_types_have_questionnaires(self):
        """Test that all insurance types in catalog have questionnaires"""
        for insurance_type in PRODUCT_CATALOG.keys():
            questionnaire = self.engine.get_questionnaire(insurance_type)
            assert questionnaire is not None, f"Missing questionnaire for {insurance_type}"
            assert len(questionnaire["questions"]) > 0
    
    def test_all_insurance_types_have_products(self):
        """Test that all insurance types have products"""
        for insurance_type, data in PRODUCT_CATALOG.items():
            assert "products" in data
            assert len(data["products"]) >= 3, f"{insurance_type} should have at least 3 product variants"
    
    def test_product_structure(self):
        """Test that all products have required fields"""
        required_fields = ["id", "name", "type", "monthly_premium_range", "features", "eligibility", "best_for"]
        
        for insurance_type, data in PRODUCT_CATALOG.items():
            for product in data["products"]:
                for field in required_fields:
                    assert field in product, f"Product {product.get('name', 'unknown')} missing field: {field}"
                
                # Check eligibility - only auto, health, and life have age requirements
                if insurance_type in ["health_insurance", "life_insurance", "auto_insurance"]:
                    assert "min_age" in product["eligibility"], f"{product['name']} missing min_age"
                    assert "max_age" in product["eligibility"], f"{product['name']} missing max_age"
    
    def test_recommendation_reasons_not_empty(self):
        """Test that recommendations always include reasons"""
        test_cases = [
            ("health_insurance", {"age": 30, "employment_status": "employed", "family_size": 1, 
                                  "pre_existing_conditions": "no", "budget": 300}),
            ("life_insurance", {"age": 35, "dependents": 2, "annual_income": 75000, 
                               "existing_coverage": "no", "health_status": "good"}),
            ("auto_insurance", {"age": 28, "driving_experience": 10, "accidents_violations": "none",
                               "vehicle_count": 1, "vehicle_age": "new_0-3_years", "vehicle_value": 30000}),
            ("home_insurance", {"property_type": "single-family", "property_age": 10, 
                               "property_value": 300000, "location_risk": "no", "mortgage": "yes"})
        ]
        
        for insurance_type, requirements in test_cases:
            recommendations = self.engine.recommend_products(insurance_type, requirements)
            assert len(recommendations) > 0, f"No recommendations for {insurance_type}"
            
            for rec in recommendations:
                assert len(rec["reasons"]) > 0, f"No reasons for {rec['product']['name']}"
                assert rec["match_percentage"] > 0, f"Match percentage is 0 for {rec['product']['name']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
