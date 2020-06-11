import sys
#hacky way to get around doing things with modules
sys.path.append("..") #https://stackoverflow.com/questions/8951255/import-script-from-a-parent-directory
from punct_split import * # this line is the cause of the bug with pytest

# functions:
# - space_parantheses
# - space_punct
# - space_coursecodes
# - has_vowels
# - semantic_split
# - punct_split

def test_space_parantheses():
    assert space_parantheses("here are(), I wonder if it will give()spaces") == "here are (), I wonder if it will give () spaces"

def test_space_punct():
    assert space_punct("here are(), I wonder if it will give()spaces") == "here  are() ,   I  wonder  if  it  will  give() spaces"

def test_space_coursecodes():
    assert space_coursecodes("(CHM111/113,CHM112/114,CHM211/213,andCHM212-/214),twosemestersofphysics (PCS201/20") == "(CHM111/113, CHM112/114, CHM211/213,and CHM212-/214),twosemestersofphysics (PCS201/20"

def test_has_vowels():
    assert has_vowels('the quick brown fox jumped over the lazy dog') == True
    assert has_vowels('th qck brwn fx jmpd vr th lz dg') == False

def test_semantic_split():
    assert semantic_split("atonofbricks") == "at on of bricks" # bug - a ton of bricks <- ideal out
    assert semantic_split("hrsatstr") == "hrs at str" # bug - should return input string?
    assert semantic_split("hrststr") == "hrststr"

def test_punct_split():
    assert punct_split("Foursemestersofchemistry(CHM111/113,CHM112/114,CHM211/213,andCHM212-/214),twosemestersofphysics (PCS201/203andPCS202/204) andmathematicsthroughcalculusI(MAT160)arerequired.") == "Four semesters of chemistry (CHM111/113, CHM112/114, CHM211/213, and CHM212-/214), two semesters of physics (PCS201/203 and PCS202/204) and mathematics through calculus I (MAT 160) are required."


