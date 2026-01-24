const { Pool } = require('pg');
const bcrypt = require('bcryptjs');

// Configuration PostgreSQL (Railway fournit DATABASE_URL automatiquement)
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.DATABASE_URL ? { rejectUnauthorized: false } : false
});

// Initialiser la base de données
async function initDatabase() {
  const client = await pool.connect();

  try {
    // Créer les tables
    await client.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'rihanna')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);

    await client.query(`
      CREATE TABLE IF NOT EXISTS creators (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        platform TEXT NOT NULL CHECK(platform IN ('OF', 'MYM')),
        commission_rate REAL NOT NULL,
        active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(name, platform)
      )
    `);

    await client.query(`
      CREATE TABLE IF NOT EXISTS daily_stats (
        id SERIAL PRIMARY KEY,
        creator_id INTEGER NOT NULL REFERENCES creators(id),
        date TEXT NOT NULL,
        subscribers INTEGER NOT NULL DEFAULT 0,
        revenue REAL NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(creator_id, date)
      )
    `);

    // Créer les index
    await client.query(`CREATE INDEX IF NOT EXISTS idx_daily_stats_date ON daily_stats(date)`);
    await client.query(`CREATE INDEX IF NOT EXISTS idx_daily_stats_creator ON daily_stats(creator_id)`);

    // Créer les utilisateurs par défaut s'ils n'existent pas
    const adminCheck = await client.query("SELECT id FROM users WHERE username = 'admin'");
    if (adminCheck.rows.length === 0) {
      const adminHash = bcrypt.hashSync('admin123', 10);
      const rihannaHash = bcrypt.hashSync('rihanna123', 10);

      await client.query("INSERT INTO users (username, password_hash, role) VALUES ($1, $2, $3)", ['admin', adminHash, 'admin']);
      await client.query("INSERT INTO users (username, password_hash, role) VALUES ($1, $2, $3)", ['rihanna', rihannaHash, 'rihanna']);

      console.log('Utilisateurs créés:');
      console.log('  - admin / admin123 (Dashboard + Data)');
      console.log('  - rihanna / rihanna123 (Data uniquement)');
    }

    // Créer les créatrices par défaut
    const creatorsCheck = await client.query("SELECT COUNT(*) as count FROM creators");
    if (parseInt(creatorsCheck.rows[0].count) === 0) {
      await client.query("INSERT INTO creators (name, platform, commission_rate) VALUES ($1, $2, $3)", ['Georgina', 'OF', 0.38]);
      await client.query("INSERT INTO creators (name, platform, commission_rate) VALUES ($1, $2, $3)", ['Georgina', 'MYM', 0.38]);
      await client.query("INSERT INTO creators (name, platform, commission_rate) VALUES ($1, $2, $3)", ['Jade', 'OF', 0.48]);
      await client.query("INSERT INTO creators (name, platform, commission_rate) VALUES ($1, $2, $3)", ['Jade', 'MYM', 0.48]);
      console.log('Créatrices initialisées: Georgina (OF/MYM), Jade (OF/MYM)');
    }

    // Importer les données initiales si la table est vide
    const statsCheck = await client.query("SELECT COUNT(*) as count FROM daily_stats");
    if (parseInt(statsCheck.rows[0].count) === 0) {
      console.log('Import des données initiales...');
      await importInitialData(client);
    }

    console.log('Base de données PostgreSQL initialisée avec succès!');
  } finally {
    client.release();
  }
}

async function importInitialData(client) {
  const initialData = {
    "Georgina OF": [
      {date: "2025-11-01", sub: 29, ca: 20.29},{date: "2025-11-02", sub: 27, ca: 202.94},{date: "2025-11-03", sub: 31, ca: 60.88},{date: "2025-11-04", sub: 24, ca: 412.65},{date: "2025-11-05", sub: 21, ca: 443.09},{date: "2025-11-06", sub: 15, ca: 67.65},{date: "2025-11-07", sub: 7, ca: 136.99},{date: "2025-11-08", sub: 12, ca: 83.71},{date: "2025-11-09", sub: 17, ca: 59.19},{date: "2025-11-10", sub: 23, ca: 286.66},{date: "2025-11-11", sub: 26, ca: 497.21},{date: "2025-11-12", sub: 22, ca: 240.15},{date: "2025-11-13", sub: 12, ca: 181.80},{date: "2025-11-14", sub: 19, ca: 214.78},{date: "2025-11-15", sub: 29, ca: 235.08},{date: "2025-11-16", sub: 30, ca: 97.24},{date: "2025-11-17", sub: 28, ca: 250.30},{date: "2025-11-18", sub: 67, ca: 121.77},{date: "2025-11-19", sub: 48, ca: 415.19},{date: "2025-11-20", sub: 30, ca: 267.21},{date: "2025-11-21", sub: 40, ca: 211.40},{date: "2025-11-22", sub: 20, ca: 536.11},{date: "2025-11-23", sub: 32, ca: 175.04},{date: "2025-11-24", sub: 32, ca: 298.50},{date: "2025-11-25", sub: 32, ca: 347.54},{date: "2025-11-26", sub: 32, ca: 489.60},{date: "2025-11-27", sub: 21, ca: 387.28},{date: "2025-11-28", sub: 22, ca: 635.05},{date: "2025-11-29", sub: 26, ca: 266.36},{date: "2025-11-30", sub: 22, ca: 22.83},{date: "2025-12-01", sub: 25, ca: 186.88},{date: "2025-12-02", sub: 27, ca: 284.97},{date: "2025-12-03", sub: 23, ca: 164.89},{date: "2025-12-04", sub: 43, ca: 47.35},{date: "2025-12-05", sub: 38, ca: 135.30},{date: "2025-12-06", sub: 45, ca: 257.06},{date: "2025-12-07", sub: 23, ca: 147.13},{date: "2025-12-08", sub: 12, ca: 67.65},{date: "2025-12-09", sub: 18, ca: 104.85},{date: "2025-12-10", sub: 15, ca: 453.24},{date: "2025-12-11", sub: 24, ca: 133.60},{date: "2025-12-12", sub: 18, ca: 260.44},{date: "2025-12-13", sub: 20, ca: 381.37},{date: "2025-12-14", sub: 19, ca: 175.88},{date: "2025-12-15", sub: 15, ca: 257.06},{date: "2025-12-16", sub: 25, ca: 469.31},{date: "2025-12-17", sub: 16, ca: 122.61},{date: "2025-12-18", sub: 50, ca: 251.14},{date: "2025-12-19", sub: 22, ca: 65.96},{date: "2025-12-20", sub: 25, ca: 138.68},{date: "2025-12-21", sub: 29, ca: 145.44},{date: "2025-12-22", sub: 40, ca: 300.19},{date: "2025-12-23", sub: 29, ca: 345.00},{date: "2025-12-24", sub: 27, ca: 145.44},{date: "2025-12-25", sub: 29, ca: 193.64},{date: "2025-12-26", sub: 42, ca: 354.31},{date: "2025-12-27", sub: 43, ca: 295.11},{date: "2025-12-28", sub: 33, ca: 246.92},{date: "2025-12-29", sub: 37, ca: 290.04},{date: "2025-12-30", sub: 68, ca: 186.03},{date: "2025-12-31", sub: 37, ca: 44.82},{date: "2026-01-01", sub: 38, ca: 93.86},{date: "2026-01-02", sub: 45, ca: 520.89},{date: "2026-01-03", sub: 47, ca: 425.34},{date: "2026-01-04", sub: 50, ca: 295.11},{date: "2026-01-05", sub: 37, ca: 321.33},{date: "2026-01-06", sub: 35, ca: 261.29},{date: "2026-01-07", sub: 33, ca: 368.68},{date: "2026-01-08", sub: 62, ca: 226.62},{date: "2026-01-09", sub: 44, ca: 277.36},{date: "2026-01-10", sub: 64, ca: 143.75},{date: "2026-01-11", sub: 46, ca: 141.22},{date: "2026-01-12", sub: 32, ca: 263.83},{date: "2026-01-13", sub: 19, ca: 470.15},{date: "2026-01-14", sub: 23, ca: 831.22},{date: "2026-01-15", sub: 12, ca: 237.61},{date: "2026-01-16", sub: 22, ca: 131.07},{date: "2026-01-17", sub: 24, ca: 138.68},{date: "2026-01-18", sub: 24, ca: 250.30},{date: "2026-01-19", sub: 24, ca: 607.99}
    ],
    "Georgina MYM": [
      {date: "2025-11-01", sub: 1, ca: 147.0},{date: "2025-11-02", sub: 6, ca: 297.0},{date: "2025-11-03", sub: 3, ca: 281.0},{date: "2025-11-04", sub: 3, ca: 274.0},{date: "2025-11-05", sub: 5, ca: 38.0},{date: "2025-11-06", sub: 3, ca: 182.0},{date: "2025-11-07", sub: 1, ca: 106.0},{date: "2025-11-08", sub: 0, ca: 39.0},{date: "2025-11-09", sub: 5, ca: 42.0},{date: "2025-11-10", sub: 44, ca: 245.0},{date: "2025-11-11", sub: 24, ca: 504.0},{date: "2025-11-12", sub: 15, ca: 609.0},{date: "2025-11-13", sub: 6, ca: 337.0},{date: "2025-11-14", sub: 8, ca: 198.0},{date: "2025-11-15", sub: 5, ca: 151.0},{date: "2025-11-16", sub: 8, ca: 393.0},{date: "2025-11-17", sub: 2, ca: 58.0},{date: "2025-11-18", sub: 296, ca: 185.0},{date: "2025-11-19", sub: 23, ca: 530.0},{date: "2025-11-20", sub: 68, ca: 367.0},{date: "2025-11-21", sub: 59, ca: 179.0},{date: "2025-11-22", sub: 25, ca: 353.0},{date: "2025-11-23", sub: 75, ca: 286.0},{date: "2025-11-24", sub: 46, ca: 432.0},{date: "2025-11-25", sub: 68, ca: 431.0},{date: "2025-11-26", sub: 45, ca: 359.0},{date: "2025-11-27", sub: 52, ca: 298.0},{date: "2025-11-28", sub: 75, ca: 86.0},{date: "2025-11-29", sub: 60, ca: 242.0},{date: "2025-11-30", sub: 33, ca: 40.0},{date: "2025-12-01", sub: 35, ca: 614.0},{date: "2025-12-02", sub: 69, ca: 307.0},{date: "2025-12-03", sub: 76, ca: 85.0},{date: "2025-12-04", sub: 80, ca: 69.0},{date: "2025-12-05", sub: 42, ca: 216.0},{date: "2025-12-06", sub: 33, ca: 297.0},{date: "2025-12-07", sub: 27, ca: 149.0},{date: "2025-12-08", sub: 24, ca: 264.0},{date: "2025-12-09", sub: 44, ca: 138.0},{date: "2025-12-10", sub: 59, ca: 674.0},{date: "2025-12-11", sub: 44, ca: 178.0},{date: "2025-12-12", sub: 39, ca: 429.0},{date: "2025-12-13", sub: 37, ca: 112.0},{date: "2025-12-14", sub: 39, ca: 66.0},{date: "2025-12-15", sub: 38, ca: 232.0},{date: "2025-12-16", sub: 87, ca: 72.0},{date: "2025-12-17", sub: 59, ca: 1581.0},{date: "2025-12-18", sub: 46, ca: 1995.0},{date: "2025-12-19", sub: 41, ca: 120.0},{date: "2025-12-20", sub: 0, ca: 0.0},{date: "2025-12-21", sub: 41, ca: 299.0},{date: "2025-12-22", sub: 62, ca: 188.0},{date: "2025-12-23", sub: 75, ca: 318.0},{date: "2025-12-24", sub: 78, ca: 56.0},{date: "2025-12-25", sub: 89, ca: 34.0},{date: "2025-12-26", sub: 229, ca: 669.0},{date: "2025-12-27", sub: 171, ca: 387.0},{date: "2025-12-28", sub: 134, ca: 226.0},{date: "2025-12-29", sub: 102, ca: 382.0},{date: "2025-12-30", sub: 91, ca: 342.0},{date: "2025-12-31", sub: 41, ca: 802.0},{date: "2026-01-01", sub: 34, ca: 709.0},{date: "2026-01-02", sub: 22, ca: 334.0},{date: "2026-01-03", sub: 25, ca: 578.0},{date: "2026-01-04", sub: 51, ca: 477.0},{date: "2026-01-05", sub: 31, ca: 626.0},{date: "2026-01-06", sub: 72, ca: 420.0},{date: "2026-01-07", sub: 49, ca: 1155.0},{date: "2026-01-08", sub: 54, ca: 292.0},{date: "2026-01-09", sub: 36, ca: 467.0},{date: "2026-01-10", sub: 44, ca: 867.0},{date: "2026-01-11", sub: 86, ca: 754.0},{date: "2026-01-12", sub: 81, ca: 422.0},{date: "2026-01-13", sub: 67, ca: 270.0},{date: "2026-01-14", sub: 97, ca: 261.0},{date: "2026-01-15", sub: 73, ca: 235.0},{date: "2026-01-16", sub: 56, ca: 591.0},{date: "2026-01-17", sub: 53, ca: 598.0},{date: "2026-01-18", sub: 112, ca: 1450.0},{date: "2026-01-19", sub: 36, ca: 453.0}
    ],
    "Jade OF": [
      {date: "2025-11-01", sub: 17, ca: 267.21},{date: "2025-11-02", sub: 9, ca: 311.18},{date: "2025-11-03", sub: 11, ca: 199.56},{date: "2025-11-04", sub: 17, ca: 192.80},{date: "2025-11-05", sub: 25, ca: 142.06},{date: "2025-11-06", sub: 31, ca: 189.41},{date: "2025-11-07", sub: 12, ca: 175.88},{date: "2025-11-08", sub: 36, ca: 43.97},{date: "2025-11-09", sub: 29, ca: 101.47},{date: "2025-11-10", sub: 28, ca: 37.21},{date: "2025-11-11", sub: 12, ca: 104.85},{date: "2025-11-12", sub: 14, ca: 108.24},{date: "2025-11-13", sub: 18, ca: 253.68},{date: "2025-11-14", sub: 23, ca: 118.38},{date: "2025-11-15", sub: 13, ca: 192.80},{date: "2025-11-16", sub: 11, ca: 40.59},{date: "2025-11-17", sub: 19, ca: 37.21},{date: "2025-11-18", sub: 15, ca: 268.06},{date: "2025-11-19", sub: 16, ca: 57.50},{date: "2025-11-20", sub: 12, ca: 147.13},{date: "2025-11-21", sub: 59, ca: 157.28},{date: "2025-11-22", sub: 49, ca: 87.94},{date: "2025-11-23", sub: 56, ca: 32.98},{date: "2025-11-24", sub: 39, ca: 124.30},{date: "2025-11-25", sub: 20, ca: 94.71},{date: "2025-11-26", sub: 49, ca: 54.12},{date: "2025-11-27", sub: 34, ca: 86.25},{date: "2025-11-28", sub: 17, ca: 187.72},{date: "2025-11-29", sub: 22, ca: 121.77},{date: "2025-11-30", sub: 19, ca: 0.00},{date: "2025-12-01", sub: 17, ca: 241.00},{date: "2025-12-02", sub: 15, ca: 199.56},{date: "2025-12-03", sub: 13, ca: 188.57},{date: "2025-12-04", sub: 14, ca: 259.60},{date: "2025-12-05", sub: 13, ca: 68.49},{date: "2025-12-06", sub: 12, ca: 0.00},{date: "2025-12-07", sub: 14, ca: 27.90},{date: "2025-12-08", sub: 15, ca: 33.82},{date: "2025-12-09", sub: 9, ca: 71.88},{date: "2025-12-10", sub: 26, ca: 38.05},{date: "2025-12-11", sub: 17, ca: 40.59},{date: "2025-12-12", sub: 10, ca: 101.47},{date: "2025-12-13", sub: 7, ca: 98.09},{date: "2025-12-14", sub: 10, ca: 20.29},{date: "2025-12-15", sub: 47, ca: 71.88},{date: "2025-12-16", sub: 19, ca: 56.66},{date: "2025-12-17", sub: 6, ca: 160.66},{date: "2025-12-18", sub: 11, ca: 152.21},{date: "2025-12-19", sub: 6, ca: 54.96},{date: "2025-12-20", sub: 3, ca: 253.68},{date: "2025-12-21", sub: 2, ca: 186.03},{date: "2025-12-22", sub: 8, ca: 151.36},{date: "2025-12-23", sub: 9, ca: 13.53},{date: "2025-12-24", sub: 9, ca: 76.10},{date: "2025-12-25", sub: 3, ca: 104.01},{date: "2025-12-26", sub: 6, ca: 38.05},{date: "2025-12-27", sub: 4, ca: 0.00},{date: "2025-12-28", sub: 6, ca: 10.99},{date: "2025-12-29", sub: 10, ca: 60.88},{date: "2025-12-30", sub: 6, ca: 314.56},{date: "2025-12-31", sub: 8, ca: 179.27},{date: "2026-01-01", sub: 10, ca: 6.76},{date: "2026-01-02", sub: 6, ca: 122.61},{date: "2026-01-03", sub: 10, ca: 476.92},{date: "2026-01-04", sub: 11, ca: 145.44},{date: "2026-01-05", sub: 15, ca: 56.66},{date: "2026-01-06", sub: 8, ca: 196.18},{date: "2026-01-07", sub: 6, ca: 153.05},{date: "2026-01-08", sub: 8, ca: 169.97},{date: "2026-01-09", sub: 7, ca: 99.78},{date: "2026-01-10", sub: 5, ca: 71.88},{date: "2026-01-11", sub: 5, ca: 261.29},{date: "2026-01-12", sub: 10, ca: 54.12},{date: "2026-01-13", sub: 2, ca: 308.64},{date: "2026-01-14", sub: 3, ca: 146.29},{date: "2026-01-15", sub: 5, ca: 165.74},{date: "2026-01-16", sub: 3, ca: 386.44},{date: "2026-01-17", sub: 10, ca: 118.38},{date: "2026-01-18", sub: 6, ca: 84.56},{date: "2026-01-19", sub: 5, ca: 71.88}
    ],
    "Jade MYM": [
      {date: "2025-11-01", sub: 0, ca: 0.0},{date: "2025-11-02", sub: 0, ca: 6.0},{date: "2025-11-03", sub: 2, ca: 6.0},{date: "2025-11-04", sub: 0, ca: 27.0},{date: "2025-11-05", sub: 0, ca: 0.0},{date: "2025-11-06", sub: 0, ca: 13.0},{date: "2025-11-07", sub: 0, ca: 6.0},{date: "2025-11-08", sub: 0, ca: 27.0},{date: "2025-11-09", sub: 0, ca: 0.0},{date: "2025-11-10", sub: 0, ca: 6.0},{date: "2025-11-11", sub: 1, ca: 13.0},{date: "2025-11-12", sub: 0, ca: 13.0},{date: "2025-11-13", sub: 0, ca: 13.0},{date: "2025-11-14", sub: 0, ca: 6.0},{date: "2025-11-15", sub: 0, ca: 6.0},{date: "2025-11-16", sub: 1, ca: 6.0},{date: "2025-11-17", sub: 0, ca: 6.0},{date: "2025-11-18", sub: 1, ca: 0.0},{date: "2025-11-19", sub: 79, ca: 27.0},{date: "2025-11-20", sub: 38, ca: 0.0},{date: "2025-11-21", sub: 42, ca: 6.0},{date: "2025-11-22", sub: 22, ca: 6.0},{date: "2025-11-23", sub: 21, ca: 6.0},{date: "2025-11-24", sub: 21, ca: 98.0},{date: "2025-11-25", sub: 102, ca: 843.0},{date: "2025-11-26", sub: 30, ca: 335.0},{date: "2025-11-27", sub: 17, ca: 156.0},{date: "2025-11-28", sub: 16, ca: 173.0},{date: "2025-11-29", sub: 22, ca: 603.0},{date: "2025-11-30", sub: 10, ca: 19.0},{date: "2025-12-01", sub: 13, ca: 37.0},{date: "2025-12-02", sub: 61, ca: 10.0},{date: "2025-12-03", sub: 81, ca: 34.0},{date: "2025-12-04", sub: 37, ca: 18.0},{date: "2025-12-05", sub: 43, ca: 61.0},{date: "2025-12-06", sub: 42, ca: 23.0},{date: "2025-12-07", sub: 21, ca: 55.0},{date: "2025-12-08", sub: 33, ca: 0.0},{date: "2025-12-09", sub: 26, ca: 5.0},{date: "2025-12-10", sub: 25, ca: 132.0},{date: "2025-12-11", sub: 38, ca: 102.0},{date: "2025-12-12", sub: 26, ca: 193.0},{date: "2025-12-13", sub: 28, ca: 122.0},{date: "2025-12-14", sub: 23, ca: 144.0},{date: "2025-12-15", sub: 22, ca: 27.0},{date: "2025-12-16", sub: 70, ca: 68.0},{date: "2025-12-17", sub: 48, ca: 151.0},{date: "2025-12-18", sub: 53, ca: 87.0},{date: "2025-12-19", sub: 51, ca: 59.0},{date: "2025-12-20", sub: 27, ca: 43.0},{date: "2025-12-21", sub: 37, ca: 32.0},{date: "2025-12-22", sub: 47, ca: 7.0},{date: "2025-12-23", sub: 52, ca: 99.0},{date: "2025-12-24", sub: 133, ca: 25.0},{date: "2025-12-25", sub: 125, ca: 61.0},{date: "2025-12-26", sub: 160, ca: 457.0},{date: "2025-12-27", sub: 143, ca: 139.0},{date: "2025-12-28", sub: 134, ca: 54.0},{date: "2025-12-29", sub: 121, ca: 224.0},{date: "2025-12-30", sub: 75, ca: 157.0},{date: "2025-12-31", sub: 80, ca: 139.0},{date: "2026-01-01", sub: 92, ca: 153.0},{date: "2026-01-02", sub: 89, ca: 59.0},{date: "2026-01-03", sub: 72, ca: 147.0},{date: "2026-01-04", sub: 56, ca: 763.0},{date: "2026-01-05", sub: 41, ca: 95.0},{date: "2026-01-06", sub: 32, ca: 272.0},{date: "2026-01-07", sub: 48, ca: 394.0},{date: "2026-01-08", sub: 25, ca: 296.0},{date: "2026-01-09", sub: 14, ca: 221.0},{date: "2026-01-10", sub: 17, ca: 217.0},{date: "2026-01-11", sub: 46, ca: 195.0},{date: "2026-01-12", sub: 61, ca: 85.0},{date: "2026-01-13", sub: 67, ca: 52.0},{date: "2026-01-14", sub: 94, ca: 506.0},{date: "2026-01-15", sub: 73, ca: 164.0},{date: "2026-01-16", sub: 87, ca: 273.0},{date: "2026-01-17", sub: 80, ca: 185.0},{date: "2026-01-18", sub: 91, ca: 388.0},{date: "2026-01-19", sub: 144, ca: 328.0}
    ]
  };

  for (const [key, stats] of Object.entries(initialData)) {
    const [name, platform] = key.split(' ');
    const creatorResult = await client.query('SELECT id FROM creators WHERE name = $1 AND platform = $2', [name, platform]);
    const creatorId = creatorResult.rows[0]?.id;

    if (creatorId) {
      for (const stat of stats) {
        await client.query(
          'INSERT INTO daily_stats (creator_id, date, subscribers, revenue) VALUES ($1, $2, $3, $4) ON CONFLICT (creator_id, date) DO NOTHING',
          [creatorId, stat.date, stat.sub, stat.ca]
        );
      }
    }
  }

  console.log('Données initiales importées avec succès!');
}

// Fonctions helpers pour les requêtes
async function queryAll(sql, params = []) {
  // Convertir les ? en $1, $2, etc. pour PostgreSQL
  let pgSql = sql;
  let paramIndex = 0;
  pgSql = pgSql.replace(/\?/g, () => `$${++paramIndex}`);

  const result = await pool.query(pgSql, params);
  return result.rows;
}

async function queryOne(sql, params = []) {
  const results = await queryAll(sql, params);
  return results[0] || null;
}

async function run(sql, params = []) {
  // Convertir les ? en $1, $2, etc. pour PostgreSQL
  let pgSql = sql;
  let paramIndex = 0;
  pgSql = pgSql.replace(/\?/g, () => `$${++paramIndex}`);

  const result = await pool.query(pgSql, params);
  return {
    lastInsertRowid: result.rows[0]?.id,
    changes: result.rowCount
  };
}

function getPool() {
  return pool;
}

module.exports = {
  initDatabase,
  getPool,
  queryAll,
  queryOne,
  run,
  saveDatabase: () => {} // No-op pour compatibilité
};
