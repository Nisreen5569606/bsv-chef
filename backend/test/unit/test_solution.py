import pytest
from unittest.mock import Mock, patch
from src.controllers.recipecontroller import RecipeController
from src.util.dao import DAO
from src.static.diets import Diet

@pytest.fixture
def mock_dao():
    dao = Mock(spec=DAO)
    return dao

@pytest.fixture
def controller(mock_dao):
    return RecipeController(items_dao=mock_dao)

def test_no_recipes_available(controller):
    controller.recipes = []
    result = controller.get_recipe(Diet.NONE, take_best=True)
    assert result is None

def test_no_recipes_match_diet(controller):
    controller.recipes = [{'name': 'Recipe1', 'diets': ['vegetarian']}]
    result = controller.get_recipe(Diet.VEGAN, take_best=True)
    assert result is None

def test_recipes_match_diet_low_readiness(controller):
    controller.recipes = [{'name': 'Recipe1', 'diets': ['vegetarian']}]
    with patch('src.controllers.recipecontroller.calculate_readiness', return_value=0.05):
        result = controller.get_recipe(Diet.VEGETARIAN, take_best=True)
    assert result is None

def test_recipes_match_diet_sufficient_readiness(mock_calculate, controller):
    controller.recipes = [{'name': 'Tomatoe Soup', 'diets': ['vegan']}]
    result = controller.get_recipe(Diet.VEGAN, take_best=True)
    assert result == 'Tomatoe Soup'

