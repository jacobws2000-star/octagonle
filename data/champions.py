"""
Curated set of UFC fighters who are or have been champions (undisputed or
interim), across all divisions. Merged into the dataset by normalized name to
set the `isChampion` flag. Since the game uses the active roster, this focuses
on current champions plus former champions still fighting.

Maintenance: add names as titles change. Matching is accent/case-insensitive.
"""

CHAMPION_NAMES = {
    # --- Current champions (as of 2026) ---
    "Tom Aspinall",
    "Alex Pereira",
    "Khamzat Chimaev",
    "Islam Makhachev",
    "Ilia Topuria",
    "Justin Gaethje",
    "Alexander Volkanovski",
    "Petr Yan",
    "Joshua Van",
    "Kayla Harrison",
    "Zhang Weili",
    "Valentina Shevchenko",

    # --- Former champions still active / recently active ---
    "Jon Jones",
    "Dricus du Plessis",
    "Magomed Ankalaev",
    "Jack Della Maddalena",
    "Merab Dvalishvili",
    "Alexandre Pantoja",
    "Sean O'Malley",
    "Leon Edwards",
    "Belal Muhammad",
    "Sean Strickland",
    "Israel Adesanya",
    "Charles Oliveira",
    "Dustin Poirier",
    "Max Holloway",
    "Aljamain Sterling",
    "Brandon Moreno",
    "Deiveson Figueiredo",
    "Jamahal Hill",
    "Jiri Prochazka",
    "Ciryl Gane",
    "Francis Ngannou",
    "Stipe Miocic",
    "Kamaru Usman",
    "Colby Covington",
    "Robert Whittaker",
    "Rose Namajunas",
    "Carla Esparza",
    "Julianna Pena",
    "Amanda Nunes",
    "Henry Cejudo",
    "Petr Yan",
    "Glover Teixeira",
}
