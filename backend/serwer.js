const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');
const cors = require('cors');

//inicjalizacja
const app = express();
const PORT = 3000;

app.use(cors());
app.use(bodyParser.json());

// połączenie z bazą
const db = new sqlite3.Database('./users.db', (err) => {
    if (err) {
        console.error("Problem połączenia z bazą sqlite3: ", err.message);
    } else {
        console.log("Połączono z bazą sqlite3.");
    }
});

// zapytanie tworzące bazę + tabele
db.run(`CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)`,
    (err) => {
        if (err) {
            console.error("Błąd tworzenia tabeli w bazie: ", err.message);
        } else {
            console.log("Utworzono tabelę users.");
        }
    }
);

// rejestracja użytkownika
app.post('/register', (req, res) => {
    const { username, password } = req.body;
    if (!username || !password) {
        return res.status(400).json({ message: "Nazwa użytkownika i hasło są wymagane" }); //bad_request
    } else {
        const query = `INSERT INTO users (username, password) VALUE (?, ?)`;
        db.run(query, [username, password], function(err) {
            if (err) {
                return res.status(500).json({ message: "Błąd rejestracji.", error: err.message }); //internal_server_error
            }
            return res.status(201).json({ message: "Rejestracja poprawna.", userId: this.lastId });
        })
        return res.status(200).json({})
    }
});

// logowanie użytkownika
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    if (!username || !password) {
        return res.status(400).json({ message: "Nazwa użytkownika i hasło są wymagane" }); //bad_request
    } else {
        const query = `SELECT * FROM users WHERE username = ? AND password = ?`;
        db.get(query, [username, password], function(err, row) {
            if (err) {
                return res.status(500).json({ message: "Błąd logowania.", error: err.message }); //internal_server_error
            }
            if (!row) {
                return res.status(401).json({ message: "Błędne dane logowania." }); //unauthorized
            }
            return res.status(200).json({ message: "Logowanie udane.", user: row.username }); //ok
        })
    }
});

// uruchomienie serwera
app.listen(PORT, () => {
    console.log(`Serwer działą na porcie: ${PORT}`);
});
