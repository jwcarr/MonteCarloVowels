import math
import random

### The pitch function converts an acoustic hertz value into a perceptual pitch
### value using a transformation method of your choice.

def pitch(hertz, method):
        if method == "bark":
                return 13 * math.atan(0.00076 * hertz) + 3.5 * math.atan((hertz / 7500)**2)

        elif method == "erb":
                return 11.17268 * math.log(1 + ((46.06538 * hertz) / (hertz + 14678.49)))

        elif method == "mel":
                return 1127.01048 * math.log(1 + (hertz / 700))

        elif method == "semitone":
                return 39.87 * math.log(hertz / 50)
        else:
                return "Error: The method \"" + method + "\" is not valid. Use either \"bark\", \"erb\", \"mel\", or \"semitone\"."

### ----------------------------------------------------------------------------

### The dist function calculates the distance between two vowels in n-dimensional
### space, given the formant values for two vowels (alpha and beta).

def dist(alpha, beta):
        dist_total = 0
        a = 0
        while (a < len(alpha)):
                dist_total = dist_total + ((alpha[a] - beta[a])**2)
                a = a + 1

        return math.sqrt(dist_total)

### ----------------------------------------------------------------------------

### The inverse_square function calculates the energy in a vowel system, given the
### distances between each pair of vowels

def inverse_square(distances):
        inv_squares = []
        for d in distances:
                inv_squares.append(1 / d**2)

        return sum(inv_squares)

### ----------------------------------------------------------------------------

### The pitch_vowels function takes a list of vowels and converts them to a psycho-
### acoustic scale.

def pitch_vowels(vowels, scale):
        N = len(vowels)
        n = 0
        new_vowels = []

        while (n < N):
                F = len(vowels[n])
                f = 0
                pitched_vowels = []
                while (f < F):
                        pitched_vowels.append(pitch(vowels[n][f], scale))
                        f = f + 1

                new_vowels.append(pitched_vowels)
                n = n + 1

        return new_vowels

### ----------------------------------------------------------------------------

### The energy function takes a list of vowels and returns the energy in the system

def energy(vowel_set):
        N = len(vowel_set)
        dist_list = []
        i = 0
        while (i < N):
                j = 0
                while (j < N):
                        if (i < j):
                                vowel_dist = dist(vowel_set[i], vowel_set[j])
                                dist_list.append(vowel_dist)
                        j = j + 1
                i = i + 1

        return inverse_square(dist_list)

### ----------------------------------------------------------------------------

### The space_size function takes a matrix of vowels and returns the min and max for
### each formant.

def space_size(vowel_matrix):

        F1s = [row[0] for row in vowel_matrix]
        F2s = [row[1] for row in vowel_matrix]
        F3s = [row[2] for row in vowel_matrix]

        F1_max = int(max(F1s) * 10000)
        F2_max = int(max(F2s) * 10000)
        F3_max = int(max(F3s) * 10000)

        F1_min = int(min(F1s) * 10000)
        F2_min = int(min(F2s) * 10000)
        F3_min = int(min(F3s) * 10000)

        return [[F1_min, F1_max], [F2_min, F2_max], [F3_min, F3_max]]

### ----------------------------------------------------------------------------

### The create_random_system function takes an inventory size and dimension values to
### produce a randomized set of vowels given these constraints.

def create_random_system(inventory_size, min_max):
        v = 0
        new_set = []
        while (v < inventory_size):
                F1_value = random.randrange(min_max[0][0], min_max[0][1])
                if min_max[1][0] < F1_value:
                        min_alt = F1_value
                else:
                        min_alt = min_max[1][0]

                F2_value = random.randrange(min_alt, min_max[1][1])
                if min_max[2][0] < F2_value:
                        min_alt = F2_value
                else:
                        min_alt = min_max[2][0]

                F3_value = random.randrange(min_alt, min_max[2][1])

                new_vowel = [float(F1_value) / 10000, float(F2_value) / 10000, float(F3_value) / 10000]

                new_set.append(new_vowel)

                v = v + 1

        return new_set

### ----------------------------------------------------------------------------

### The analyse function runs the analysis and prints the results

def analyse(language_name, simulations=10000, psychoacoustic_scale="mel"):

        ### First load in the formant data
        formant_data = load(language_name)

        ### Now we convert to a psychoacoustic scale
        vowel_set_converted = pitch_vowels(formant_data, psychoacoustic_scale)

        ### Then we calculate the energy in the system
        vowel_system_energy = energy(vowel_set_converted)

        ### Finally, we take the inverse of the energy
        x = 1 / vowel_system_energy

        ### Next we need to determine the size of the natural vowel space
        dimensions = space_size(vowel_set_converted)

        ### Now run the Monte Carlo simulation
        results = []
        sim = 0

        while (sim < simulations):

                ### Create a randomized vowel system
                random_set = create_random_system(len(formant_data), dimensions)

                ### Measure the energy in the randomized system, and take the inverse
                result = 1 / energy(random_set)

                ### Store the measurement
                results.append(result)

                sim = sim + 1

        ### Calculate mean of Monte Carlo sample
        m = sum(results) / simulations

        ### Calculate standard deviation of Monte Carlo sample
        total = 0.0
        for r in results:
                dev = (r-m)**2
                total = total + dev
                
        sd = math.sqrt(total/(simulations-1))

        ### Compare the randomized systems to the veridical one to produce a z-score
        z = (x - m) / sd

        ### Output final results
        print("MONTE CARLO VOWELS\n")
        print("Analysis of the \"" + language_name + "\" language:\n")
        print("  Number of simulations = " + str(simulations))
        print("  Psychoacoustic scale  = " + psychoacoustic_scale)
        print("\nResults:\n")
        print("  x  = " + str(x))
        print("  m  = " + str(m))
        print("  sd = " + str(sd))
        print("  z  = " + str(z))

### ----------------------------------------------------------------------------

### The load function imports data from the database files for a given language name

def load(filename):
        open_file = open("database/" + filename, "r")
        file_content = open_file.read()
        lines = file_content.split("\n")

        language_data = []
        l=0
        while (l < len(lines)):
                formant_freqs = lines[l].split("\t")
                formant_set = []
                lf = 0
                while (lf < len(formant_freqs)):
                        formant_set.append(float(formant_freqs[lf]))
                        lf = lf + 1
                language_data.append(formant_set)
                l = l + 1

        return language_data
        
### ----------------------------------------------------------------------------
