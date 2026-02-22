const mysql = require('mysql');

// Hardkodovani credentials u kodu
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'password123', // Hardkodovana lozinka
    database: 'testdb'
});

// SQL Injection - direktna konkatenacija korisničkog inputa
function getUserByUsername(username) {
    const query = `SELECT * FROM users WHERE username = '${username}'`;
    
    connection.query(query, (error, results) => {
        if (error) {
            console.error('Error:', error); // Loša praksa - logovanje detalja greške
            return;
        }
        return results;
    });
}

// Još jedna SQL injection greška
function deleteUser(userId) {
    const sql = `DELETE FROM users WHERE id = ${userId}`;
    connection.query(sql, (err, result) => {
        if (err) throw err;
        console.log('User deleted');
    });
}

// XSS vulnerability - direktan output bez sanitizacije
function displayComment(comment) {
    document.getElementById('comments').innerHTML = comment; // XSS!
}

// Command injection mogućnost
function executeSystemCommand(command) {
    const { exec } = require('child_process');
    exec('ls -la ' + command, (error, stdout, stderr) => { // Command injection!
        if (error) {
            console.error(`exec error: ${error}`);
            return;
        }
        console.log(stdout);
    });
}

// Hardkodovani JWT secret
const JWT_SECRET = 'mySecretKey123'; // Hardkodovani secret

// Loša praksa - slanje lozinke u plain text-u
function login(username, password) {
    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password // Loša praksa - trebalo bi hash-ovati
        })
    });
}

// Nema validacije inputa
function processPayment(amount, cardNumber) {
    // Nema validacije da li je amount pozitivan broj
    // Nema validacije formata kartice
    const payment = {
        amount: amount,
        cardNumber: cardNumber
    };
    // Slanje payment podataka...
}

module.exports = {
    getUserByUsername,
    deleteUser,
    displayComment,
    executeSystemCommand,
    login,
    processPayment
};
