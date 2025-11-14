import pytest
from mediscan.bloodwork_calculator import calculate_bmi,categorize_bmi, calculate_anemia_severity, calculate_nlr

def test_categorize_bmi():
    bmi_values = [15.0, 16.5, 18.0, 22.0, 27.0, 32.0, 37.0, 45.0]
    expected_result = [
        "wygłodzenie",
        "wychudzenie",
        "niedowaga",
        "waga prawidłowa",
        "nadwaga",
        "otyłość I stopnia",
        "otyłość II stopnia",
        "otyłość III stopnia"
    ]
    for i, bmi in enumerate(bmi_values):
        result = categorize_bmi(bmi)
        assert result == expected_result[i], \
            f"Dla BMI {bmi} oczekiwano kategorii '{expected_result[i]}', otrzymano '{result}'"
def test_calculate_BMI():
    test_cases = [
        (70, 175, 22.86),
        (50, 160, 19.53),
        (90, 180, 27.78),
        (110, 165, 40.40)
    ]
    for weight, height, expected_bmi in test_cases:
        calculated_bmi = round(calculate_bmi(weight, height), 2)
        assert calculated_bmi == expected_bmi, \
            f"Dla wagi {weight} kg i wzrostu {height} m oczekiwano BMI {expected_bmi}, otrzymano {calculated_bmi}"

def test_calculate_BMI_negative_values():
    test_cases = [
        (70, -175, "błąd - ujemny wzrost"), # fail - brak obsługi ujemnych wartości w kodzie
        (-50, 160, "błąd - ujemna waga"), # fail - brak obsługi ujemnych wartości w kodzie
        (0, 180, "błąd - zerowa waga"), # fail - brak obsługi zerowych wartości w kodzie
        (110, 0, "błąd - zerowy wzrost") # fail - brak obsługi zerowych wartości w kodzie
        ("pięćdziesiąt", 165, "błąd - nieprawidłowy typ wagi"), # fail - brak obsługi nieprawidlowego typu wartości w kodzie
        (90, "sto osiemdziesiąt centymetrów", "błąd - nieprawidłowy typ wzrostu") # fail - brak obsługi nieprawidlowego typu wartości w kodzie
    ]
    for weight, height, expected_bmi in test_cases:
        calculated_bmi = round(calculate_bmi(weight, height), 2)
        assert calculated_bmi == expected_bmi, \
            f"Dla wagi {weight} kg i wzrostu {height} m oczekiwano BMI {expected_bmi}, otrzymano {calculated_bmi}"
def test_calculate_nlr():
    test_cases = [
        (4.0, 2.0, 2.0),
        (6.0, 3.0, 2.0),
        (3.5, 1.5, 2.33),
        (5.0, 2.5, 2.0)
    ]
    for neutrophils, lymphocytes, expected_nlr in test_cases:
        calculated_nlr = round(calculate_nlr(neutrophils, lymphocytes), 2)
        assert calculated_nlr == expected_nlr, \
            f"Dla neutrofili {neutrophils} i limfocytów {lymphocytes} oczekiwano NLR {expected_nlr}, otrzymano {calculated_nlr}"
        
def test_calculate_anemia_severity():
    test_cases = [
        ("F", 13.0,  "brak"), # fail - źle podana wartość w kodzie
        ("F", 11.0,  "łagodna"),
        ("F", 8.50,  "umiarkowana"),
        ("F", 7.50, "ciężka"),
        ("M", 14.0,  "brak"),
        ("M", 11.50,  "łagodna"),
        ("M", 9.00,"umiarkowana"),
        ("M", 7.00,  "ciężka")
    ]
    for sex, hemoglobin, expected_as in test_cases:
        calculated_as = calculate_anemia_severity(hemoglobin, sex)
        assert calculated_as == expected_as, \
            f"Dla płci {sex} i hemoglobiny {hemoglobin} oczekiwano stopnia niedokrwistości '{expected_as}', otrzymano '{calculated_as}'"
        
def test_calculate_anemia_severity_edge_cases():
    test_cases = [
        ("N", 12.0,  "nieznana_płeć"), # fail - brak obsługi nieprawidlowego typu płci w kodzie
    ]
    for sex, hemoglobin, expected_as in test_cases:
        calculated_as = calculate_anemia_severity(hemoglobin, sex)
        assert calculated_as == expected_as, \
            f"Dla płci {sex} i hemoglobiny {hemoglobin} oczekiwano stopnia niedokrwistości '{expected_as}', otrzymano '{calculated_as}'"
    