"""
Set of every fighter who has held a UFC championship (undisputed or interim),
across all divisions, men's and women's — current and former. Merged into the
dataset by accent/case-insensitive name match to set the `isChampion` flag.

Because the game uses the active roster, only champions still fighting actually
get tagged; the rest are harmless. Sourced from the full historical list of UFC
champions, so it stays complete as retired champions (e.g. José Aldo) return.
"""

CHAMPION_NAMES = {
    # Heavyweight
    "Mark Coleman", "Maurice Smith", "Randy Couture", "Bas Rutten",
    "Kevin Randleman", "Josh Barnett", "Ricco Rodriguez", "Tim Sylvia",
    "Frank Mir", "Andrei Arlovski", "Brock Lesnar", "Cain Velasquez",
    "Junior dos Santos", "Fabrício Werdum", "Fabricio Werdum", "Stipe Miocic",
    "Daniel Cormier", "Francis Ngannou", "Jon Jones", "Tom Aspinall", "Ciryl Gane",
    # Light Heavyweight
    "Frank Shamrock", "Tito Ortiz", "Chuck Liddell", "Quinton Jackson",
    "Forrest Griffin", "Rashad Evans", "Lyoto Machida", "Maurício Rua",
    "Mauricio Rua", "Jan Błachowicz", "Jan Blachowicz", "Glover Teixeira",
    "Jiří Procházka", "Jiri Prochazka", "Jamahal Hill", "Alex Pereira",
    "Magomed Ankalaev", "Carlos Ulberg",
    # Middleweight
    "Dave Menne", "Murilo Bustamante", "Evan Tanner", "Rich Franklin",
    "Anderson Silva", "Chris Weidman", "Luke Rockhold", "Michael Bisping",
    "Robert Whittaker", "Georges St-Pierre", "Israel Adesanya",
    "Sean Strickland", "Dricus du Plessis", "Khamzat Chimaev",
    # Welterweight
    "Pat Miletich", "Carlos Newton", "Matt Hughes", "B.J. Penn", "BJ Penn",
    "Matt Serra", "Tyron Woodley", "Kamaru Usman", "Leon Edwards",
    "Belal Muhammad", "Jack Della Maddalena",
    # Lightweight
    "Islam Makhachev", "Jens Pulver", "Sean Sherk", "Frankie Edgar",
    "Benson Henderson", "Anthony Pettis", "Rafael dos Anjos", "Eddie Alvarez",
    "Conor McGregor", "Khabib Nurmagomedov", "Charles Oliveira", "Ilia Topuria",
    "Justin Gaethje",
    # Featherweight
    "José Aldo", "Jose Aldo", "Max Holloway", "Alexander Volkanovski",
    # Bantamweight
    "Dominick Cruz", "Renan Barão", "Renan Barao", "T.J. Dillashaw",
    "TJ Dillashaw", "Cody Garbrandt", "Petr Yan", "Aljamain Sterling",
    "Sean O'Malley", "Merab Dvalishvili", "Henry Cejudo",
    # Flyweight
    "Demetrious Johnson", "Deiveson Figueiredo", "Brandon Moreno",
    "Alexandre Pantoja", "Joshua Van",
    # Women's Bantamweight
    "Ronda Rousey", "Holly Holm", "Miesha Tate", "Amanda Nunes",
    "Julianna Peña", "Julianna Pena", "Raquel Pennington", "Kayla Harrison",
    # Women's Featherweight
    "Cris Cyborg", "Germaine de Randamie",
    # Women's Flyweight
    "Nicco Montaño", "Nicco Montano", "Valentina Shevchenko", "Alexa Grasso",
    # Women's Strawweight
    "Carla Esparza", "Joanna Jędrzejczyk", "Joanna Jedrzejczyk",
    "Rose Namajunas", "Jéssica Andrade", "Jessica Andrade", "Zhang Weili",
    "Mackenzie Dern",

    # --- Interim champions ---
    # `isChampion` covers ANY held UFC title, undisputed OR interim (current or
    # former). Most interim winners also held (or challenged for) the undisputed
    # belt and so already appear above; the names below are interim-only holders
    # who would otherwise be missed.
    #
    # Include ONLY fighters who actually WON an interim title. Do not add
    # interim-title *challengers who lost* — e.g. Ovince Saint Preux (lost to
    # Jones), Kelvin Gastelum (lost to Adesanya), Paddy Pimblett (lost to
    # Gaethje) are NOT champions and must stay untagged.
    #
    # When refreshing the roster, verify each new interim champion won the bout;
    # public list pages often mix in challengers.
    "Colby Covington",       # interim welterweight (2018)
    "Dustin Poirier",        # interim lightweight (2019)
    "Yair Rodríguez", "Yair Rodriguez",  # interim featherweight (2023)
    "Tony Ferguson",         # interim lightweight (2017)
}
