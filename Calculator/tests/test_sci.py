from sci import *

# Tests the "validate_subOpNum" function
def test_val_subOpNum():
    # Cases 1-6 should return 1, else 0
    for i in range(1, 6):
        assert validate_subOpNum(i) == 1

    assert validate_subOpNum(17) == 0
    assert validate_subOpNum(-28) == 0

def test_norm_trigo_funcs():
    """-------------------------- NORMAL TRIGO FUNCTIONS TEST --------------------------"""
    
    """----- BASICS + PRECISION + SYMMETRY -----"""
    # SIN
    assert validate_and_eval(1, 1, "sin", sine, 1083.7) == "sin(1083.7) = 0.064532308"
    assert validate_and_eval(1, 1, "sin", sine, -1083.7) == "sin(-1083.7) = -0.064532308"
    # COS
    assert validate_and_eval(1, 2, "cos", cosine, 1083.7) == "cos(1083.7) = 0.997915618"
    assert validate_and_eval(1, 2, "cos", cosine, -1083.7) == "cos(-1083.7) = 0.997915618"
    # TAN
    assert validate_and_eval(1, 3, "tan", tangent, 1083.7) == "tan(1083.7) = 0.064667099"
    assert validate_and_eval(1, 3, "tan", tangent, -1083.7) == "tan(-1083.7) = -0.064667099"
    # COT
    assert validate_and_eval(1, 4, "cot", cot, 1083.7) == "cot(1083.7) = 15.4638141"
    assert validate_and_eval(1, 4, "cot", cot, -1083.7) == "cot(-1083.7) = -15.4638141"
    # SEC
    assert validate_and_eval(1, 5, "sec", sec, 1083.7) == "sec(1083.7) = 1.002088735"
    assert validate_and_eval(1, 5, "sec", sec, -1083.7) == "sec(-1083.7) = 1.002088735"
    # COSEC
    assert validate_and_eval(1, 6, "cosec", cosec, 1083.7) == "cosec(1083.7) = 15.496113917"
    assert validate_and_eval(1, 6, "cosec", cosec, -1083.7) == "cosec(-1083.7) = -15.496113917"

    """----- DOMAIN TEST -----"""
    # TAN → undefined at 90 + n*180
    assert validate_and_eval(1, 3, "tan", tangent, 90) == "Cannot divide by zero"
    assert validate_and_eval(1, 3, "tan", tangent, -90) == "Cannot divide by zero"
    # COT → undefined at 0 + n*180
    assert validate_and_eval(1, 4, "cot", cot, 0) == "Cannot divide by zero"
    assert validate_and_eval(1, 4, "cot", cot, 180) == "Cannot divide by zero"
    # SEC → undefined at 90 + n*180
    assert validate_and_eval(1, 5, "sec", sec, 90) == "Cannot divide by zero"
    assert validate_and_eval(1, 5, "sec", sec, -90) == "Cannot divide by zero"
    # COSEC → undefined at 0 + n*180
    assert validate_and_eval(1, 6, "cosec", cosec, 0) == "Cannot divide by zero"
    assert validate_and_eval(1, 6, "cosec", cosec, -180) == "Cannot divide by zero"

    """----- RANGE TEST -----"""
    for angle in [0, 30, 45, 60, 90, 180, 270, 360]:
        val_sin = sine(angle)
        val_cos = cosine(angle)
        assert -1 <= val_sin <= 1
        assert -1 <= val_cos <= 1

    """----- VERY LARGE INPUT -----"""
    for val in [1_000_000, -1_000_000]:
        assert validate_and_eval(1, 1, "sin", sine, val) in ["sin(1000000) = -0.984807753", "sin(-1000000) = 0.984807753"]
        assert validate_and_eval(1, 2, "cos", cosine, val) in ["cos(1000000) = 0.173648178", "cos(-1000000) = 0.173648178"]
        assert validate_and_eval(1, 3, "tan", tangent, val) in ["tan(1000000) = -5.67128182", "tan(-1000000) = 5.67128182"]
        assert validate_and_eval(1, 4, "cot", cot, val) in ["cot(1000000) = -0.176326981", "cot(-1000000) = 0.176326981"]
        assert validate_and_eval(1, 5, "sec", sec, val) in ["sec(1000000) = 5.758770483", "sec(-1000000) = 5.758770483"]
        assert validate_and_eval(1, 6, "cosec", cosec, val) in ["cosec(1000000) = -1.015426612", "cosec(-1000000) = 1.015426612"]

    """----- VERY SMALL INPUT -----"""
    small_vals = [0.0001, -0.0001]
    for val in small_vals:
        assert validate_and_eval(1, 1, "sin", sine, val) in ["sin(0.0001) = 0.000001745", "sin(-0.0001) = -0.000001745"]
        assert validate_and_eval(1, 2, "cos", cosine, val) in ["cos(0.0001) = 1", "cos(-0.0001) = 1"]
        assert validate_and_eval(1, 3, "tan", tangent, val) in ["tan(0.0001) = 0.000001745", "tan(-0.0001) = -0.000001745"]
        assert validate_and_eval(1, 4, "cot", cot, val) in ["cot(0.0001) = 572957.795130241", "cot(-0.0001) = -572957.795130241"]
        assert validate_and_eval(1, 5, "sec", sec, val) in ["sec(0.0001) = 1", "sec(-0.0001) = 1"]
        assert validate_and_eval(1, 6, "cosec", cosec, val) in ["cosec(0.0001) = 572957.795131114", "cosec(-0.0001) = -572957.795131114"]

    """----- INVALID / WEIRD INPUT -----"""
    weird_inputs = ["", "abc", "🙂", "@#$%^&*", None, [], {}]
    for w in weird_inputs:
        assert validate_and_eval(1, 1, "sin", sine, w) == 0
        assert validate_and_eval(1, 2, "cos", cosine, w) == 0
        assert validate_and_eval(1, 3, "tan", tangent, w) == 0
        assert validate_and_eval(1, 4, "cot", cot, w) == 0
        assert validate_and_eval(1, 5, "sec", sec, w) == 0
        assert validate_and_eval(1, 6, "cosec", cosec, w) == 0


def test_inverse_normal_trigo_funcs():

    """-------------------------- POSITIVE & NEGATIVE VALUES TEST --------------------------"""
    
    # ----- SIN⁻¹ ----- (sub_op = 1)
    assert validate_and_eval(3, 1, "sin⁻¹", sine_inv, 0.564738) == "sin⁻¹(0.564738) = 34.384099541"
    assert validate_and_eval(3, 1, "sin⁻¹", sine_inv, -0.564738) == "sin⁻¹(-0.564738) = -34.384099541"
    
    # ----- COS⁻¹ ----- (sub_op = 2)
    assert validate_and_eval(3, 2, "cos⁻¹", cosine_inv, 0.564738) == "cos⁻¹(0.564738) = 55.615900459"
    assert validate_and_eval(3, 2, "cos⁻¹", cosine_inv, -0.564738) == "cos⁻¹(-0.564738) = 124.384099541"
    
    # ----- TAN⁻¹ ----- (sub_op = 3)
    assert validate_and_eval(3, 3, "tan⁻¹", tangent_inv, 2.718281) == "tan⁻¹(2.718281) = 69.802463052"
    assert validate_and_eval(3, 3, "tan⁻¹", tangent_inv, -2.718281) == "tan⁻¹(-2.718281) = -69.802463052"
    
    # ----- COT⁻¹ ----- (sub_op = 4)
    assert validate_and_eval(3, 4, "cot⁻¹", cot_inv, 0.564738) == "cot⁻¹(0.564738) = 60.544932027"
    assert validate_and_eval(3, 4, "cot⁻¹", cot_inv, -0.564738) == "cot⁻¹(-0.564738) = -60.544932027"
    
    # ----- SEC⁻¹ ----- (sub_op = 5)
    assert validate_and_eval(3, 5, "sec⁻¹", sec_inv, 1.732051) == "sec⁻¹(1.732051) = 54.735614818"
    assert validate_and_eval(3, 5, "sec⁻¹", sec_inv, -1.732051) == "sec⁻¹(-1.732051) = 125.264385182"
    
    # ----- COSEC⁻¹ ----- (sub_op = 6)
    assert validate_and_eval(3, 6, "cosec⁻¹", cosec_inv, 1.732051) == "cosec⁻¹(1.732051) = 35.264385182"
    assert validate_and_eval(3, 6, "cosec⁻¹", cosec_inv, -1.732051) == "cosec⁻¹(-1.732051) = -35.264385182"


    """-------------------------- DOMAIN TEST --------------------------"""

    # SIN⁻¹ domain [-1, 1]
    assert validate_and_eval(3, 1, "sin⁻¹", sine_inv, 1.5) == "Domain error: Enter value between [-1,1]"
    assert validate_and_eval(3, 1, "sin⁻¹", sine_inv, -1.5) == "Domain error: Enter value between [-1,1]"

    # COS⁻¹ domain [-1, 1]
    assert validate_and_eval(3, 2, "cos⁻¹", cosine_inv, 1.5) == "Domain error: Enter value between [-1,1]"
    assert validate_and_eval(3, 2, "cos⁻¹", cosine_inv, -1.5) == "Domain error: Enter value between [-1,1]"

    # TAN⁻¹ domain all real numbers → no error
    # COT⁻¹ special case val = 0
    assert validate_and_eval(3, 4, "cot⁻¹", cot_inv, 0) == "cot⁻¹(0) = 90"

    # SEC⁻¹ domain |x| >= 1
    assert validate_and_eval(3, 5, "sec⁻¹", sec_inv, 0.5) == "Domain error: Enter value which lie in |x|>=1"
    assert validate_and_eval(3, 5, "sec⁻¹", sec_inv, -0.5) == "Domain error: Enter value which lie in |x|>=1"

    # COSEC⁻¹ domain |x| >= 1
    assert validate_and_eval(3, 6, "cosec⁻¹", cosec_inv, 0.5) == "Domain error: Enter value which lie in |x|>=1"
    assert validate_and_eval(3, 6, "cosec⁻¹", cosec_inv, -0.5) == "Domain error: Enter value which lie in |x|>=1"


    """-------------------------- LARGE & SMALL INPUT TEST --------------------------"""

    # LARGE input
    assert validate_and_eval(3, 1, "sin⁻¹", sine_inv, 1.0) == "sin⁻¹(1.0) = 90"
    assert validate_and_eval(3, 2, "cos⁻¹", cosine_inv, 1.0) == "cos⁻¹(1.0) = 0"
    assert validate_and_eval(3, 3, "tan⁻¹", tangent_inv, 1000000) == "tan⁻¹(1000000) = 89.999942704"
    assert validate_and_eval(3, 4, "cot⁻¹", cot_inv, 1000000) == "cot⁻¹(1000000) = 0.000057296"
    assert validate_and_eval(3, 5, "sec⁻¹", sec_inv, 1000000) == "sec⁻¹(1000000) = 89.999942704"
    assert validate_and_eval(3, 6, "cosec⁻¹", cosec_inv, 1000000) == "cosec⁻¹(1000000) = 0.000057296"

    # SMALL input
    assert validate_and_eval(3, 1, "sin⁻¹", sine_inv, 1e-6) == "sin⁻¹(1e-06) = 0.000057296"
    assert validate_and_eval(3, 2, "cos⁻¹", cosine_inv, 1e-6) == "cos⁻¹(1e-06) = 89.999942704"
    assert validate_and_eval(3, 3, "tan⁻¹", tangent_inv, 1e-6) == "tan⁻¹(1e-06) = 0.000057296"
    assert validate_and_eval(3, 4, "cot⁻¹", cot_inv, 1e-6) == "cot⁻¹(1e-06) = 89.999942704"
    assert validate_and_eval(3, 5, "sec⁻¹", sec_inv, 1.000001) == "sec⁻¹(1.000001) = 0.081028435"
    assert validate_and_eval(3, 6, "cosec⁻¹", cosec_inv, 1.000001) == "cosec⁻¹(1.000001) = 89.918971565"


    """-------------------------- INVALID INPUT TEST --------------------------"""

    for invalid in ["", "abc", "🙂", "@#$%", None, []]:
        assert validate_and_eval(3, 1, "sin⁻¹", sine_inv, invalid) == 0
        assert validate_and_eval(3, 2, "cos⁻¹", cosine_inv, invalid) == 0
        assert validate_and_eval(3, 3, "tan⁻¹", tangent_inv, invalid) == 0
        assert validate_and_eval(3, 4, "cot⁻¹", cot_inv, invalid) == 0
        assert validate_and_eval(3, 5, "sec⁻¹", sec_inv, invalid) == 0
        assert validate_and_eval(3, 6, "cosec⁻¹", cosec_inv, invalid) == 0

def test_hyperbolic_trigo_funcs():

    """-------------------------- POSITIVE & NEGATIVE VALUES TEST --------------------------"""
    
    # ----- SINH ----- (sub_op = 1)
    assert validate_and_eval(2, 1, "sinh", sineh, 2.718281) == "sinh(2.718281) = 7.544130798"
    assert validate_and_eval(2, 1, "sinh", sineh, -2.718281) == "sinh(-2.718281) = -7.544130798"
    
    # ----- COSH ----- (sub_op = 2)
    assert validate_and_eval(2, 2, "cosh", cosineh, 2.718281) == "cosh(2.718281) = 7.610118889"
    assert validate_and_eval(2, 2, "cosh", cosineh, -2.718281) == "cosh(-2.718281) = 7.610118889"
    
    # ----- TANH ----- (sub_op = 3)
    assert validate_and_eval(2, 3, "tanh", tangenth, 2.718281) == "tanh(2.718281) = 0.991328901"
    assert validate_and_eval(2, 3, "tanh", tangenth, -2.718281) == "tanh(-2.718281) = -0.991328901"
    
    # ----- COTH ----- (sub_op = 4)
    assert validate_and_eval(2, 4, "coth", coth, 2.718281) == "coth(2.718281) = 1.008746944"
    assert validate_and_eval(2, 4, "coth", coth, -2.718281) == "coth(-2.718281) = -1.008746944"
    
    # ----- SECH ----- (sub_op = 5)
    assert validate_and_eval(2, 5, "sech", sech, 2.718281) == "sech(2.718281) = 0.131403992"
    assert validate_and_eval(2, 5, "sech", sech, -2.718281) == "sech(-2.718281) = 0.131403992"
    
    # ----- COSECH ----- (sub_op = 6)
    assert validate_and_eval(2, 6, "cosech", cosech, 2.718281) == "cosech(2.718281) = 0.132553375"
    assert validate_and_eval(2, 6, "cosech", cosech, -2.718281) == "cosech(-2.718281) = -0.132553375"


    """-------------------------- DOMAIN TEST --------------------------"""

    # SINH domain all real → no error
    # COSH domain all real → no error
    # TANH domain all real → no error
    # COTH domain val != 0
    assert validate_and_eval(2, 4, "coth", coth, 0) == "Cannot divide by zero"
    
    # COSECH domain val != 0
    assert validate_and_eval(2, 6, "cosech", cosech, 0) == "Cannot divide by zero"


    """-------------------------- LARGE & SMALL INPUT TEST --------------------------"""

    # LARGE input
    assert validate_and_eval(2, 1, "sinh", sineh, 20) == "sinh(20) = 242582597.704895139"
    assert validate_and_eval(2, 2, "cosh", cosineh, 20) == "cosh(20) = 242582597.704895139"
    assert validate_and_eval(2, 3, "tanh", tangenth, 2.5) == "tanh(2.5) = 0.986614298"
    assert validate_and_eval(2, 4, "coth", coth, 2.5) == "coth(2.5) = 1.01356731"
    assert validate_and_eval(2, 5, "sech", sech, 2.5) == "sech(2.5) = 0.163071232"
    assert validate_and_eval(2, 6, "cosech", cosech, 2.5) == "cosech(2.5) = 0.16528367"

    # SMALL input
    assert validate_and_eval(2, 1, "sinh", sineh, 0.001234567) == "sinh(0.001234567) = 0.001234567"
    assert validate_and_eval(2, 2, "cosh", cosineh, 0.001234567) == "cosh(0.001234567) = 1.000000762"
    assert validate_and_eval(2, 3, "tanh", tangenth, 0.001234567) == "tanh(0.001234567) = 0.001234566"
    assert validate_and_eval(2, 4, "coth", coth, 0.001234567) == "coth(0.001234567) = 810.001002823"
    assert validate_and_eval(2, 5, "sech", sech, 0.001234567) == "sech(0.001234567) = 0.999999238"
    assert validate_and_eval(2, 6, "cosech", cosech, 0.001234567) == "cosech(0.001234567) = 810.000385539"



    """-------------------------- INVALID INPUT TEST --------------------------"""

    for invalid in ["", "abc", "🙂", "@#$%", None, []]:
        assert validate_and_eval(2, 1, "sinh", sineh, invalid) == 0
        assert validate_and_eval(2, 2, "cosh", cosineh, invalid) == 0
        assert validate_and_eval(2, 3, "tanh", tangenth, invalid) == 0
        assert validate_and_eval(2, 4, "coth", coth, invalid) == 0
        assert validate_and_eval(2, 5, "sech", sech, invalid) == 0
        assert validate_and_eval(2, 6, "cosech", cosech, invalid) == 0

def test_inverse_hyperbolic_trigo_funcs():

    """-------------------------- POSITIVE & NEGATIVE VALUES TEST --------------------------"""
    
    # ----- SINH⁻¹ ----- (sub_op = 1)
    assert validate_and_eval(4, 1, "sinh⁻¹", sineh_inv, 2.718281) == "sinh⁻¹(2.718281) = 1.725382273"
    assert validate_and_eval(4, 1, "sinh⁻¹", sineh_inv, -2.718281) == "sinh⁻¹(-2.718281) = -1.725382273"
    
    # ----- COSH⁻¹ ----- (sub_op = 2)
    assert validate_and_eval(4, 2, "cosh⁻¹", cosineh_inv, 3.141593) == "cosh⁻¹(3.141593) = 1.811526389"
    assert validate_and_eval(4, 2, "cosh⁻¹", cosineh_inv, 10.123456) == "cosh⁻¹(10.123456) = 3.005553917"
    
    # ----- TANH⁻¹ ----- (sub_op = 3)
    assert validate_and_eval(4, 3, "tanh⁻¹", tangenth_inv, 0.564738) == "tanh⁻¹(0.564738) = 0.639762764"
    assert validate_and_eval(4, 3, "tanh⁻¹", tangenth_inv, -0.564738) == "tanh⁻¹(-0.564738) = -0.639762764"
    
    # ----- COTH⁻¹ ----- (sub_op = 4)
    assert validate_and_eval(4, 4, "coth⁻¹", coth_inv, 2.718281) == "coth⁻¹(2.718281) = 0.385968546"
    assert validate_and_eval(4, 4, "coth⁻¹", coth_inv, -2.718281) == "coth⁻¹(-2.718281) = -0.385968546"
    
    # ----- SECH⁻¹ ----- (sub_op = 5)
    assert validate_and_eval(4, 5, "sech⁻¹", sech_inv, 0.564738) == "sech⁻¹(0.564738) = 1.173121432"
    assert validate_and_eval(4, 5, "sech⁻¹", sech_inv, 0.123456789) == "sech⁻¹(0.123456789) = 2.781178892"
    
    # ----- COSECH⁻¹ ----- (sub_op = 6)
    assert validate_and_eval(4, 6, "cosech⁻¹", cosech_inv, 2.718281) == "cosech⁻¹(2.718281) = 0.36004975"
    assert validate_and_eval(4, 6, "cosech⁻¹", cosech_inv, -2.718281) == "cosech⁻¹(-2.718281) = -0.36004975"

    """-------------------------- DOMAIN TEST --------------------------"""

    # SINH⁻¹ domain all real → no error
    # COSH⁻¹ domain >= 1
    assert validate_and_eval(4, 2, "cosh⁻¹", cosineh_inv, 0.5) == "Domain error: Enter value greater than 1"
    
    # TANH⁻¹ domain (-1, 1)
    assert validate_and_eval(4, 3, "tanh⁻¹", tangenth_inv, 1) == "Domain error: Enter value between (-1,1)"
    assert validate_and_eval(4, 3, "tanh⁻¹", tangenth_inv, -1) == "Domain error: Enter value between (-1,1)"
    
    # COTH⁻¹ domain |x|>1
    assert validate_and_eval(4, 4, "coth⁻¹", coth_inv, 0.5) == "Domain error: Enter value outside [-1,1]"
    assert validate_and_eval(4, 4, "coth⁻¹", coth_inv, -0.5) == "Domain error: Enter value outside [-1,1]"
    
    # SECH⁻¹ domain (0, 1]
    assert validate_and_eval(4, 5, "sech⁻¹", sech_inv, 0) == "Domain error: Enter value in range (0,1]"
    assert validate_and_eval(4, 5, "sech⁻¹", sech_inv, 1.5) == "Domain error: Enter value in range (0,1]"
    
    # COSECH⁻¹ domain val != 0
    assert validate_and_eval(4, 6, "cosech⁻¹", cosech_inv, 0) == "Domain error: Enter any value except 0"


    """-------------------------- LARGE & SMALL INPUT TEST --------------------------"""

    # LARGE input
    assert validate_and_eval(4, 1, "sinh⁻¹", sineh_inv, 1000) == "sinh⁻¹(1000) = 7.60090271"
    assert validate_and_eval(4, 2, "cosh⁻¹", cosineh_inv, 1000) == "cosh⁻¹(1000) = 7.60090221"
    assert validate_and_eval(4, 3, "tanh⁻¹", tangenth_inv, 0.999999123) == "tanh⁻¹(0.999999123) = 7.319952793"
    assert validate_and_eval(4, 4, "coth⁻¹", coth_inv, 1.000001234) == "coth⁻¹(1.000001234) = 7.149198715"
    assert validate_and_eval(4, 5, "sech⁻¹", sech_inv, 0.001234567) == "sech⁻¹(0.001234567) = 7.390181777"
    assert validate_and_eval(4, 6, "cosech⁻¹", cosech_inv, 0.001234567) == "cosech⁻¹(0.001234567) = 7.390182539"

    # SMALL input
    assert validate_and_eval(4, 1, "sinh⁻¹", sineh_inv, 0.001234567) == "sinh⁻¹(0.001234567) = 0.001234567"
    assert validate_and_eval(4, 2, "cosh⁻¹", cosineh_inv, 1.000001234) == "cosh⁻¹(1.000001234) = 0.001570987"
    assert validate_and_eval(4, 3, "tanh⁻¹", tangenth_inv, 0.001234567) == "tanh⁻¹(0.001234567) = 0.001234568"
    assert validate_and_eval(4, 4, "coth⁻¹", coth_inv, 1.001234567) == "coth⁻¹(1.001234567) = 3.695399626"
    assert validate_and_eval(4, 5, "sech⁻¹", sech_inv, 0.999999123) == "sech⁻¹(0.999999123) = 0.001324387"
    assert validate_and_eval(4, 6, "cosech⁻¹", cosech_inv, 1.001234567) == "cosech⁻¹(1.001234567) = 0.880501424"


    """-------------------------- INVALID INPUT TEST --------------------------"""

    for invalid in ["", "abc", "🙂", "@#$%", None, []]:
        assert validate_and_eval(4, 1, "sinh⁻¹", sineh_inv, invalid) == 0
        assert validate_and_eval(4, 2, "cosh⁻¹", cosineh_inv, invalid) == 0
        assert validate_and_eval(4, 3, "tanh⁻¹", tangenth_inv, invalid) == 0
        assert validate_and_eval(4, 4, "coth⁻¹", coth_inv, invalid) == 0
        assert validate_and_eval(4, 5, "sech⁻¹", sech_inv, invalid) == 0
        assert validate_and_eval(4, 6, "cosech⁻¹", cosech_inv, invalid) == 0