import sqlite3




def crear_base_datos():
    conexion = sqlite3.connect('sistema_experto_gimnasio.db')
    cursor = conexion.cursor()


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Hechos (
        id_hecho INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        objetivo TEXT,
        tipo_ejercicio TEXT,
        nivel TEXT,
        edad INTEGER,
        altura INTEGER,
        peso INTEGER,
        condicion_medica TEXT
    );
    ''')


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reglas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        objetivo TEXT,
        tipo_ejercicio TEXT,
        nivel TEXT,
        condicion_medica TEXT
    );
    ''')




    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Conclusiones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_regla INTEGER,
        conclusion TEXT,
        FOREIGN KEY (id_regla) REFERENCES Reglas(id)
    );
    ''')




    reglas = [
        {
            "condiciones": {
                "objetivo": "resistencia",
                "tipo_ejercicio": "cardio",
                "nivel": "principiante"
            },
            "conclusiones": ["caminadora", "bicicleta", "saltar la cuerda"]
        },
        {
            "condiciones": {
                "objetivo": "perder peso",
                "tipo_ejercicio": "cardio",
                "nivel": "intermedio"
            },
            "conclusiones": ["bicicleta estática", "spinning", "elíptica"]
        },
        {
            "condiciones": {
                "objetivo": "ganar masa muscular",
                "tipo_ejercicio": "fuerza",
                "nivel": "avanzado"
            },
            "conclusiones": ["levantamiento de pesas", "ejercicios compuestos", "máquinas de resistencia"]
        },
        {
            "condiciones": {
                "condicion_medica": "problema de rodillas",
                "tipo_ejercicio": "cardio"
            },
            "conclusiones": ["evitar caminadora"]
        }
    ]


    for regla in reglas:
        condiciones = regla["condiciones"]
        cursor.execute('''
            INSERT INTO Reglas (objetivo, tipo_ejercicio, nivel, condicion_medica)
            VALUES (?, ?, ?, ?)
        ''', (
            condiciones.get("objetivo"),
            condiciones.get("tipo_ejercicio"),
            condiciones.get("nivel"),
            condiciones.get("condicion_medica")
        ))
        id_regla = cursor.lastrowid
        for conclusion in regla["conclusiones"]:
            cursor.execute('''
                INSERT INTO Conclusiones (id_regla, conclusion)
                VALUES (?, ?)
            ''', (id_regla, conclusion))


    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    crear_base_datos()
    print("Base de datos creada con éxito y datos insertados.")
