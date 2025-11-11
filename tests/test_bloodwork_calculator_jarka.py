import pytest
from mediscan.bloodwork_calculator import (
    calculate_bmi,
    calculate_nlr,
    categorize_bmi,
    calculate_anemia_severity
)

def test_calculate_bmi_normal_case():
    """Test BMI dla typowych wartości."""
    # Dla osoby o wadze 70 kg i wzroście 175 cm, BMI powinno wynosić 22.86
    weight = 70  # kg
    height = 175  # cm
    expected_bmi = 70 / ((175/100) ** 2)  # ręczne obliczenie oczekiwanego wyniku
    
    # Wywołanie testowanej funkcji
    result = calculate_bmi(weight, height)
    
    # Sprawdzenie rezultatu
    # Używamy round(x, 2) aby zaokrąglić do 2 miejsc po przecinku
    assert round(result, 2) == round(expected_bmi, 2), \
        f"BMI dla wagi {weight}kg i wzrostu {height}cm powinno wynosić {expected_bmi}, ale otrzymano {result}"

# Parametryzowany test dla różnych przypadków BMI
@pytest.mark.parametrize("weight, height, expected_bmi", [
    (50, 150, 22.22),  # niski wzrost, niska waga
    (100, 200, 25.00),  # wysoki wzrost, wysoka waga
    (80, 180, 24.69),   # średni wzrost, średnia waga
    (60, 160, 23.44),   # proporcjonalne wartości
])
def test_calculate_bmi_various_cases(weight, height, expected_bmi):
    """Test BMI dla różnych kombinacji wagi i wzrostu."""
    result = calculate_bmi(weight, height)
    assert round(result, 2) == expected_bmi, \
        f"BMI dla wagi {weight}kg i wzrostu {height}cm powinno wynosić {expected_bmi}, ale otrzymano {round(result, 2)}"

# Test na błędne dane - wzrost zerowy
def test_calculate_bmi_zero_height():
    """Test jak funkcja radzi sobie ze wzrostem równym 0."""
    with pytest.raises(ZeroDivisionError):
        calculate_bmi(70, 0)  # Powinno zgłosić błąd dzielenia przez zero
		

def test_calculate_nlr_normal_case():
    """Test NLR dla typowych wartości."""
    neutrophils = 4.5  # 10^9/L
    lymphocytes = 2.5  # 10^9/L
    expected_nlr = 4.5 / 2.5  # Powinno być 1.8
    
    result = calculate_nlr(neutrophils, lymphocytes)
    
    assert result == expected_nlr, \
        f"NLR dla neutrofili {neutrophils} i limfocytów {lymphocytes} powinno wynosić {expected_nlr}, ale otrzymano {result}"

@pytest.mark.parametrize("neutrophils, lymphocytes, expected_nlr", [
    (5.0, 2.0, 2.5),     # typowe wartości
    (10.0, 1.0, 10.0),   # wysokie neutrofile, niskie limfocyty
    (3.0, 3.0, 1.0),     # równe wartości
    (7.5, 1.5, 5.0)      # inne typowe wartości
])
def test_calculate_nlr_various_cases(neutrophils, lymphocytes, expected_nlr):
    """Test NLR dla różnych kombinacji neutrofili i limfocytów."""
    result = calculate_nlr(neutrophils, lymphocytes)
    assert result == expected_nlr, \
        f"NLR dla neutrofili {neutrophils} i limfocytów {lymphocytes} powinno wynosić {expected_nlr}, ale otrzymano {result}"

def test_calculate_nlr_zero_lymphocytes():
    """Test jak funkcja radzi sobie z limfocytami równymi 0."""
    with pytest.raises(ZeroDivisionError):
        calculate_nlr(5.0, 0)  # Powinno zgłosić błąd dzielenia przez zero
		
@pytest.fixture
def sample_patients():
    """Fixture dostarczająca przykładowe dane pacjentów."""
    return [
        {"id": 1, "weight": 70, "height": 175, "sex": "M", "hemoglobin": 14.5, "neutrophils": 4.5, "lymphocytes": 2.5},
        {"id": 2, "weight": 55, "height": 160, "sex": "F", "hemoglobin": 11.5, "neutrophils": 3.8, "lymphocytes": 2.2},
        {"id": 3, "weight": 90, "height": 180, "sex": "M", "hemoglobin": 10.5, "neutrophils": 6.5, "lymphocytes": 1.5},
        {"id": 4, "weight": 60, "height": 165, "sex": "F", "hemoglobin": 9.5, "neutrophils": 5.0, "lymphocytes": 1.8}
    ]

@pytest.mark.parametrize("bmi, expected_category", [
    (16, "wygłodzenie"),
    (16.5, "wychudzenie"),
    (18.0, "niedowaga"),
    (22.0, "waga prawidłowa"),
    (27.5, "nadwaga"),
    (32.5, "otyłość I stopnia"),
    (37.5, "otyłość II stopnia"),
    (42.0, "otyłość III stopnia")
])
def test_categorize_bmi(bmi, expected_category):
    """Test kategoryzacji BMI dla różnych wartości."""
    result = categorize_bmi(bmi)
    assert result == expected_category, \
        f"Dla BMI {bmi} kategoria powinna być '{expected_category}', ale otrzymano '{result}'"

# Test wartości granicznych
@pytest.mark.parametrize("bmi, expected_category", [
    (16.0, "wygłodzenie"),     # dokładnie na granicy wygłodzenie/wychudzenie
    (17.0, "niedowaga"),       # dokładnie na granicy wychudzenie/niedowaga
    (18.5, "waga prawidłowa"), # dokładnie na granicy niedowaga/waga prawidłowa
    (25.0, "nadwaga"),         # dokładnie na granicy waga prawidłowa/nadwaga
    (30.0, "otyłość I stopnia"), # na granicy nadwaga/otyłość I stopnia
    (35.0, "otyłość II stopnia"), # na granicy otyłość I/II stopnia
    (40.0, "otyłość III stopnia") # na granicy otyłość II/III stopnia
])
def test_categorize_bmi_boundary(bmi, expected_category):
    """Test kategoryzacji BMI dla wartości granicznych."""
    result = categorize_bmi(bmi)
    assert result == expected_category, \
        f"Dla granicznego BMI {bmi} kategoria powinna być '{expected_category}', ale otrzymano '{result}'"

@pytest.mark.parametrize("hemoglobin, sex, expected_severity", [
    (14.0, "M", "brak"),        # mężczyzna, normalna hemoglobina
    (12.0, "M", "łagodna"),     # mężczyzna, łagodna niedokrwistość
    (9.0, "M", "umiarkowana"),  # mężczyzna, umiarkowana niedokrwistość
    (7.0, "M", "ciężka"),       # mężczyzna, ciężka niedokrwistość
    
    (13.0, "F", "brak"),        # kobieta, normalna hemoglobina, taka sytuacja
    (11.0, "F", "łagodna"),        # kobieta, łagodna niedokrwistość
    (9.5, "F", "umiarkowana"),      # kobieta, umiarkowana niedokrwistość
    (7.5, "F", "ciężka"),  # kobieta, ciężka niedokrwistość
    (6.0, "F", "ciężka")        # kobieta, ciężka niedokrwistość
])
def test_calculate_anemia_severity(hemoglobin, sex, expected_severity):
    """Test określania stopnia niedokrwistości dla różnych poziomów hemoglobiny i płci."""
    result = calculate_anemia_severity(hemoglobin, sex)
    assert result == expected_severity, \
        f"Dla hemoglobiny {hemoglobin} g/dL i płci {sex}, stopień niedokrwistości powinien być '{expected_severity}', ale otrzymano '{result}'"

# Test dla nieprawidłowej płci
def test_calculate_anemia_severity_invalid_sex():
    """Test jak funkcja radzi sobie z nieprawidłową płcią."""
    # Ta funkcja powinna obsługiwać tylko 'M' i 'F'
    with pytest.raises(Exception):  # Ogólna klasa Exception, bo nie wiemy dokładnie jaki wyjątek będzie zgłoszony
        calculate_anemia_severity(12.0, "X")

def test_patient_bmi_calculation(sample_patients):
    """Test obliczania BMI dla przykładowych pacjentów."""
    for patient in sample_patients:
        bmi = calculate_bmi(patient["weight"], patient["height"])
        category = categorize_bmi(bmi)
        
        # Sprawdź czy BMI jest liczbą dodatnią
        assert bmi > 0, f"BMI pacjenta {patient['id']} powinno być dodatnie, ale wynosi {bmi}"
        
        # Sprawdź czy kategoria nie jest pusta
        assert category, f"Kategoria BMI pacjenta {patient['id']} nie powinna być pusta"
        
        print(f"Pacjent {patient['id']}: BMI = {bmi:.2f}, kategoria: {category}")

def test_patient_nlr_calculation(sample_patients):
    """Test obliczania NLR dla przykładowych pacjentów."""
    for patient in sample_patients:
        nlr = calculate_nlr(patient["neutrophils"], patient["lymphocytes"])
        
        # NLR powinno być liczbą dodatnią
        assert nlr > 0, f"NLR pacjenta {patient['id']} powinno być dodatnie, ale wynosi {nlr}"
        
        # Sprawdzamy czy obliczenia są poprawne
        expected = patient["neutrophils"] / patient["lymphocytes"]
        assert nlr == expected, \
            f"NLR pacjenta {patient['id']} powinno wynosić {expected}, ale wynosi {nlr}"
        
        print(f"Pacjent {patient['id']}: NLR = {nlr:.2f}")

def test_patient_anemia_evaluation(sample_patients):
    """Test oceny niedokrwistości dla przykładowych pacjentów."""
    for patient in sample_patients:
        severity = calculate_anemia_severity(patient["hemoglobin"], patient["sex"])
        
        # Sprawdź czy wynik nie jest pusty
        assert severity, f"Stopień niedokrwistości pacjenta {patient['id']} nie powinien być pusty"
        
        print(f"Pacjent {patient['id']}: Stopień niedokrwistości = {severity}")