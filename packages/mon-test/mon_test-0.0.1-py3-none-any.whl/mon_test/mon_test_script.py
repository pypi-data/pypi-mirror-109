#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
"""
    usage:
    >>> from mon_test import mon_script_methode , favorite_meal, voiture_de_reve
    >>> mon_script_methode()
    >>> favorite_meal()
    >>> voiture_de_reve()
"""

__all__ = ['mon_script_methode', 'favorite_meal', 'voiture_de_reve']

associe = "Francois"

def mon_script_methode():
    print("Hello c'est moi le test, je fonctionne bien.")

def favorite_meal():
    print("la Pizza biensur")

def voiture_de_reve():
    print("Ford")
 
def list_de_toutou():
    print("Pomsky","husky", "malamute","Berger finois laponie")
 


if __name__ == '__main__':
    voiture_de_reve()
