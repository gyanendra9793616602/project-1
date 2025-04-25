const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const app = express();
const port = 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize SQLite database
const db = new sqlite3.Database('./users.db', (err) => {
    if (err) {
        console.error('Error opening database:', err.message);
    } else {
        console.log('Connected to SQLite database.');
        // Create users table if it doesn't exist
        db.run(`
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL UNIQUE,
                role TEXT NOT NULL CHECK(role IN ('seeker', 'recruiter'))
            )
        `, (err) => {
            if (err) {
                console.error('Error creating table:', err.message);
            }
        });
    }
});

// Route to save user details
app.post('/save-details', (req, res) => {
    const { name, email, phone, role } = req.body;

    // Server-side validation
    if (!name || !email || !phone || !role || !['seeker', 'recruiter'].includes(role)) {
        return res.status(400).json({ success: false, message: 'Invalid input data.' });
    }

    // Insert user data into the database
    const query = `INSERT INTO users (name, email, phone, role) VALUES (?, ?, ?, ?)`;
    db.run(query, [name, email, phone, role], function(err) {
        if (err) {
            console.error('Error inserting data:', err.message);
            if (err.message.includes('UNIQUE constraint failed')) {
                return res.status(400).json({ success: false, message: 'Email or phone number already exists.' });
            }
            return res.status(500).json({ success: false, message: 'Database error.' });
        }
        res.json({ success: true, id: this.lastID });
    });
});

// Route to retrieve all users (for admin purposes, optional)
app.get('/users', (req, res) => {
    db.all('SELECT * FROM users', [], (err, rows) => {
        if (err) {
            console.error('Error fetching users:', err.message);
            return res.status(500).json({ success: false, message: 'Database error.' });
        }
        res.json({ success: true, users: rows });
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});