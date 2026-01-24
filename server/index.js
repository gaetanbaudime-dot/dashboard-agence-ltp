const express = require('express');
const session = require('express-session');
const cors = require('cors');
const path = require('path');

const { initDatabase } = require('./db');
const { router: authRouter, requireAuth } = require('./routes/auth');
const dataRouter = require('./routes/data');
const reportsRouter = require('./routes/reports');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors({
  origin: true,
  credentials: true
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Session
app.use(session({
  secret: 'agence-ltp-secret-key-change-in-production',
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: false, // Mettre à true en production avec HTTPS
    httpOnly: true,
    maxAge: 24 * 60 * 60 * 1000 // 24 heures
  }
}));

// Servir les fichiers statiques
app.use(express.static(path.join(__dirname, '..', 'public')));

// Routes API
app.use('/api/auth', authRouter);
app.use('/api', requireAuth, dataRouter);
app.use('/api/reports', requireAuth, reportsRouter);

// Routes des pages
app.get('/login', (req, res) => {
  if (req.session.user) {
    return res.redirect('/');
  }
  res.sendFile(path.join(__dirname, '..', 'public', 'login.html'));
});

app.get('/admin', (req, res) => {
  if (!req.session.user) {
    return res.redirect('/login');
  }
  res.sendFile(path.join(__dirname, '..', 'public', 'admin.html'));
});

app.get('/', (req, res) => {
  if (!req.session.user) {
    return res.redirect('/login');
  }
  res.sendFile(path.join(__dirname, '..', 'public', 'index.html'));
});

// Gestion des erreurs
app.use((err, req, res, next) => {
  console.error('Erreur:', err);
  res.status(500).json({ error: 'Erreur serveur interne' });
});

// Démarrer le serveur après l'initialisation de la base de données
async function startServer() {
  try {
    await initDatabase();

    app.listen(PORT, () => {
      console.log('');
      console.log('='.repeat(50));
      console.log('  Dashboard Agence LTP');
      console.log('='.repeat(50));
      console.log(`  Serveur démarré sur: http://localhost:${PORT}`);
      console.log('');
      console.log('  Pages disponibles:');
      console.log(`    - Dashboard: http://localhost:${PORT}/`);
      console.log(`    - Admin:     http://localhost:${PORT}/admin`);
      console.log(`    - Login:     http://localhost:${PORT}/login`);
      console.log('');
      console.log('  Identifiants par défaut:');
      console.log('    - Admin:     admin / admin123');
      console.log('    - Assistant: assistant / assistant123');
      console.log('='.repeat(50));
      console.log('');
    });
  } catch (error) {
    console.error('Erreur lors du démarrage:', error);
    process.exit(1);
  }
}

startServer();
