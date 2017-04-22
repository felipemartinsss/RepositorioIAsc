# Author: Felipe M. Santos
# Date: 22/04/2017.
# Description: A simple program to demonstrate Prolog's Knowledge Base and Inference Engine concepts.
# The program is a simple book recommender.

# liked(P, B): Person P liked the book B.
# Books that Felipe liked.
liked(felipe, 'Eu, robo').
liked(felipe, 'Memorias postumas de Bras Cubas').
liked(felipe, 'Casais inteligentes enriquecem juntos').
liked(felipe, 'Fortaleza digital').

# Books that Regina liked.
liked(regina, 'Memorias postumas de Bras Cubas').
liked(regina, 'Crash').
liked(regina, 'Livre para viver').
liked(regina, 'Fortaleza digital').

# Book that Dilacy liked.
liked(dilacy, 'Biblia Sagrada').

# recommend(P1, P2, B): P1 recomemends to P2 a book B if P1 liked the book B, P1 is not P2 and P2 didn't say anything about the book B.
recommend(P1, P2, B) :- liked(P1, B), P1 \= P2, \+ liked(P2, B).
