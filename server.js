const express = require('express');
const { Pool } = require('pg');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Base de données PostgreSQL
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

app.use(express.json());
app.use(express.static('public'));

// ============ API ============

// Récupérer toutes les créatrices
app.get('/api/creators', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM creators ORDER BY name, platform');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  }
});

// Récupérer les stats
app.get('/api/stats', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT ds.*, c.name, c.platform, c.commission_rate
      FROM daily_stats ds
      JOIN creators c ON ds.creator_id = c.id
      ORDER BY ds.date DESC, c.name, c.platform
    `);
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  }
});

// Ajouter/modifier une stat
app.post('/api/stats', async (req, res) => {
  const { creator_id, date, subscribers, revenue } = req.body;
  try {
    const result = await pool.query(`
      INSERT INTO daily_stats (creator_id, date, subscribers, revenue)
      VALUES ($1, $2, $3, $4)
      ON CONFLICT (creator_id, date)
      DO UPDATE SET subscribers = $3, revenue = $4, updated_at = NOW()
      RETURNING *
    `, [creator_id, date, subscribers, revenue]);
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  }
});

// Supprimer une stat
app.delete('/api/stats/:id', async (req, res) => {
  try {
    await pool.query('DELETE FROM daily_stats WHERE id = $1', [req.params.id]);
    res.json({ success: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  }
});

// ============ PAGES ============

// Page Dashboard (pour toi)
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Page Data (pour Rihanna)
app.get('/data', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'data.html'));
});

// ============ INIT DB ============

async function initDB() {
  const client = await pool.connect();
  try {
    // Tables
    await client.query(`
      CREATE TABLE IF NOT EXISTS creators (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        platform TEXT NOT NULL,
        commission_rate REAL NOT NULL,
        UNIQUE(name, platform)
      )
    `);

    await client.query(`
      CREATE TABLE IF NOT EXISTS daily_stats (
        id SERIAL PRIMARY KEY,
        creator_id INTEGER REFERENCES creators(id),
        date DATE NOT NULL,
        subscribers INTEGER DEFAULT 0,
        revenue REAL DEFAULT 0,
        updated_at TIMESTAMP DEFAULT NOW(),
        UNIQUE(creator_id, date)
      )
    `);

    // Créatrices par défaut
    const check = await client.query('SELECT COUNT(*) FROM creators');
    if (parseInt(check.rows[0].count) === 0) {
      await client.query("INSERT INTO creators (name, platform, commission_rate) VALUES ('Georgina', 'OF', 0.38)");
      await client.query("INSERT INTO creators (name, platform, commission_rate) VALUES ('Georgina', 'MYM', 0.38)");
      await client.query("INSERT INTO creators (name, platform, commission_rate) VALUES ('Jade', 'OF', 0.48)");
      await client.query("INSERT INTO creators (name, platform, commission_rate) VALUES ('Jade', 'MYM', 0.48)");
      console.log('Créatrices créées: Georgina (OF/MYM), Jade (OF/MYM)');
    }

    console.log('Base de données prête');
  } finally {
    client.release();
  }
}

// Démarrage
initDB().then(() => {
  app.listen(PORT, () => {
    console.log(`Serveur: http://localhost:${PORT}`);
    console.log(`Dashboard: http://localhost:${PORT}/`);
    console.log(`Data: http://localhost:${PORT}/data`);
  });
}).catch(err => {
  console.error('Erreur DB:', err);
  process.exit(1);
});
