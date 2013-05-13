MonteCarloVowels
================

A program for calculating the optimization of vowel systems. The program takes mean
formant values for F1, F2, and F3 for a given language, and calculates how optimized
that system is by comparing it to random distributions of vowels within a space of
approximately the same size. The method uses Liljencrants and Lindblom's (1972)
measure of energy in a vowel space.

Example
-------

analyse("Zulu", 10000, "mel")

Returns a z-score. The higher the z-score, the less likely the system is to have been
produced by chance, and therefore the more optimized that system is.

References
----------

Liljencrants, J., & Lindblom, B. (1972). Numerical simulation of vowel quality
systems: The role of perceptual contrast. Language, 48, 839–862. doi:10.2307/411991

See also: https://dl.dropboxusercontent.com/u/34347263/Downloads/carr-2012-avml-poster.pdf
