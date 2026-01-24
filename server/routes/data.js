const express = require('express');
const { queryAll, queryOne, run, saveDatabase } = require('../db');

const router = express.Router();

// Récupérer toutes les créatrices
router.get('/creators', (req, res) => {
  const creators = queryAll(`
    SELECT id, name, platform, commission_rate, active
    FROM creators
    WHERE active = 1
    ORDER BY name, platform
  `);
  res.json(creators);
});

// Récupérer les stats pour le dashboard (format attendu par le frontend)
router.get('/stats', (req, res) => {
  const { days = 90 } = req.query;

  const stats = queryAll(`
    SELECT
      c.name || ' ' || c.platform as creator_key,
      ds.date,
      ds.subscribers as sub,
      ds.revenue as ca
    FROM daily_stats ds
    JOIN creators c ON ds.creator_id = c.id
    WHERE ds.date >= date('now', '-' || ? || ' days')
    ORDER BY c.name, c.platform, ds.date
  `, [days]);

  // Grouper par créatrice
  const grouped = {};
  stats.forEach(stat => {
    if (!grouped[stat.creator_key]) {
      grouped[stat.creator_key] = [];
    }
    grouped[stat.creator_key].push({
      date: stat.date,
      sub: stat.sub,
      ca: stat.ca
    });
  });

  res.json(grouped);
});

// Récupérer les stats brutes avec pagination
router.get('/daily-stats', (req, res) => {
  const { page = 1, limit = 50, creator_id, start_date, end_date } = req.query;
  const offset = (page - 1) * limit;

  let query = `
    SELECT
      ds.id,
      ds.date,
      ds.subscribers,
      ds.revenue,
      ds.created_at,
      ds.updated_at,
      c.id as creator_id,
      c.name as creator_name,
      c.platform
    FROM daily_stats ds
    JOIN creators c ON ds.creator_id = c.id
    WHERE 1=1
  `;
  const params = [];

  if (creator_id) {
    query += ' AND ds.creator_id = ?';
    params.push(parseInt(creator_id));
  }
  if (start_date) {
    query += ' AND ds.date >= ?';
    params.push(start_date);
  }
  if (end_date) {
    query += ' AND ds.date <= ?';
    params.push(end_date);
  }

  query += ' ORDER BY ds.date DESC, c.name, c.platform LIMIT ? OFFSET ?';
  params.push(parseInt(limit), parseInt(offset));

  const stats = queryAll(query, params);

  // Count total
  let countQuery = 'SELECT COUNT(*) as total FROM daily_stats ds WHERE 1=1';
  const countParams = [];
  if (creator_id) {
    countQuery += ' AND ds.creator_id = ?';
    countParams.push(parseInt(creator_id));
  }
  if (start_date) {
    countQuery += ' AND ds.date >= ?';
    countParams.push(start_date);
  }
  if (end_date) {
    countQuery += ' AND ds.date <= ?';
    countParams.push(end_date);
  }

  const countResult = queryOne(countQuery, countParams);
  const total = countResult?.total || 0;

  res.json({
    data: stats,
    pagination: {
      page: parseInt(page),
      limit: parseInt(limit),
      total,
      pages: Math.ceil(total / limit)
    }
  });
});

// Ajouter ou mettre à jour une stat quotidienne
router.post('/daily-stats', (req, res) => {
  const { creator_id, date, subscribers, revenue } = req.body;

  if (!creator_id || !date) {
    return res.status(400).json({ error: 'creator_id et date sont requis' });
  }

  // Vérifier si la créatrice existe
  const creator = queryOne('SELECT id FROM creators WHERE id = ?', [creator_id]);
  if (!creator) {
    return res.status(404).json({ error: 'Créatrice non trouvée' });
  }

  try {
    // Upsert: INSERT or UPDATE
    const existing = queryOne('SELECT id FROM daily_stats WHERE creator_id = ? AND date = ?', [creator_id, date]);

    if (existing) {
      run(`
        UPDATE daily_stats
        SET subscribers = ?, revenue = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
      `, [subscribers || 0, revenue || 0, existing.id]);

      res.json({ success: true, action: 'updated', id: existing.id });
    } else {
      const result = run(`
        INSERT INTO daily_stats (creator_id, date, subscribers, revenue)
        VALUES (?, ?, ?, ?)
      `, [creator_id, date, subscribers || 0, revenue || 0]);

      res.json({ success: true, action: 'created', id: result.lastInsertRowid });
    }
  } catch (error) {
    console.error('Erreur lors de l\'ajout des stats:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

// Ajouter plusieurs stats en une fois (bulk insert)
router.post('/daily-stats/bulk', (req, res) => {
  const { stats } = req.body;

  if (!Array.isArray(stats) || stats.length === 0) {
    return res.status(400).json({ error: 'Un tableau de stats est requis' });
  }

  const results = { created: 0, updated: 0, errors: [] };

  for (const item of stats) {
    try {
      const existing = queryOne('SELECT id FROM daily_stats WHERE creator_id = ? AND date = ?',
        [item.creator_id, item.date]);

      if (existing) {
        run(`
          UPDATE daily_stats
          SET subscribers = ?, revenue = ?, updated_at = CURRENT_TIMESTAMP
          WHERE id = ?
        `, [item.subscribers || 0, item.revenue || 0, existing.id]);
        results.updated++;
      } else {
        run(`
          INSERT INTO daily_stats (creator_id, date, subscribers, revenue)
          VALUES (?, ?, ?, ?)
        `, [item.creator_id, item.date, item.subscribers || 0, item.revenue || 0]);
        results.created++;
      }
    } catch (error) {
      results.errors.push({ item, error: error.message });
    }
  }

  saveDatabase();
  res.json({ success: true, ...results });
});

// Supprimer une stat
router.delete('/daily-stats/:id', (req, res) => {
  const { id } = req.params;

  const result = run('DELETE FROM daily_stats WHERE id = ?', [parseInt(id)]);

  if (result.changes === 0) {
    return res.status(404).json({ error: 'Stat non trouvée' });
  }

  res.json({ success: true });
});

// Obtenir les commissions des créatrices
router.get('/creators/commissions', (req, res) => {
  const creators = queryAll(`
    SELECT id, name, platform, commission_rate
    FROM creators
    WHERE active = 1
  `);
  res.json(creators);
});

// Mettre à jour le taux de commission
router.put('/creators/:id/commission', (req, res) => {
  const { id } = req.params;
  const { commission_rate } = req.body;

  if (commission_rate === undefined || commission_rate < 0 || commission_rate > 1) {
    return res.status(400).json({ error: 'Taux de commission invalide (entre 0 et 1)' });
  }

  const result = run('UPDATE creators SET commission_rate = ? WHERE id = ?', [commission_rate, parseInt(id)]);

  if (result.changes === 0) {
    return res.status(404).json({ error: 'Créatrice non trouvée' });
  }

  res.json({ success: true });
});

// Ajouter une nouvelle créatrice
router.post('/creators', (req, res) => {
  const { name, platform, commission_rate = 0.40 } = req.body;

  if (!name || !platform) {
    return res.status(400).json({ error: 'name et platform sont requis' });
  }

  if (!['OF', 'MYM'].includes(platform)) {
    return res.status(400).json({ error: 'platform doit être OF ou MYM' });
  }

  try {
    const result = run(`
      INSERT INTO creators (name, platform, commission_rate)
      VALUES (?, ?, ?)
    `, [name, platform, commission_rate]);

    res.json({ success: true, id: result.lastInsertRowid });
  } catch (error) {
    if (error.message && error.message.includes('UNIQUE constraint failed')) {
      return res.status(400).json({ error: 'Cette créatrice existe déjà sur cette plateforme' });
    }
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

module.exports = router;
