from app.services.combined_service import calculate_difficulty_score

def test_empty_achievements_returns_zero():
    assert calculate_difficulty_score([]) == 0

def test_none_achievements_returns_zero():
    assert calculate_difficulty_score(None) == 0

def test_single_achievement():
    achievements = [{"global_percentage": 10.0}]
    assert calculate_difficulty_score(achievements) == 90.0

def test_multiple_achievements():
    achievements = [
        {"global_percentage": 10.0},  # contributes 90
        {"global_percentage": 90.0},  # contributes 10
    ]
    assert calculate_difficulty_score(achievements) == 50.0

def test_missing_percentage_is_skipped():
    achievements = [
        {"global_percentage": None},
        {"global_percentage": 50.0},
    ]
    assert calculate_difficulty_score(achievements) == 50.0

def test_invalid_percentage_is_skipped():
    achievements = [
        {"global_percentage": "notanumber"},
        {"global_percentage": 20.0},
    ]
    assert calculate_difficulty_score(achievements) == 80.0

def test_all_missing_percentage_returns_zero():
    achievements = [
        {"global_percentage": None},
        {"global_percentage": None},
    ]
    assert calculate_difficulty_score(achievements) == 0

def test_score_is_rounded():
    achievements = [
        {"global_percentage": 33.0},
        {"global_percentage": 66.0},
        {"global_percentage": 50.0},
    ]
    score = calculate_difficulty_score(achievements)
    assert isinstance(score, float)
    assert score == round(score, 2)
