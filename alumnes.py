def alumne_schema(alumne) -> dict:
    # Converteix un registre d'alumne en un diccionari
    return {
        "Id": alumne[0],
        "NomAlumne": alumne[1],
        "Cicle": alumne[2],
        "Curs": alumne[3],
        "Grup": alumne[4],
        "IdAula": alumne[5],
        "CreatedAt": alumne[6],
        "UpdatedAt": alumne[7]
    }

def alumnes_schema(alumnes) -> list:
    # Converteix una llista de registres d'alumnes en una llista de diccionaris
    return [alumne_schema(alumne) for alumne in alumnes]
