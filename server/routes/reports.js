const express = require('express');
const PDFDocument = require('pdfkit');
const { queryAll } = require('../db');

const router = express.Router();

// Générer un rapport PDF pour une créatrice
router.get('/pdf/:creatorName', (req, res) => {
  const { creatorName } = req.params;
  const { start_date, end_date, platform } = req.query;

  // Valider les dates
  const endDate = end_date || new Date().toISOString().split('T')[0];
  const startDate = start_date || (() => {
    const d = new Date();
    d.setDate(d.getDate() - 30);
    return d.toISOString().split('T')[0];
  })();

  // Récupérer les créatrices correspondantes
  let creatorsQuery = 'SELECT * FROM creators WHERE name = ? AND active = 1';
  const params = [creatorName];

  if (platform) {
    creatorsQuery += ' AND platform = ?';
    params.push(platform);
  }

  const creators = queryAll(creatorsQuery, params);

  if (creators.length === 0) {
    return res.status(404).json({ error: 'Créatrice non trouvée' });
  }

  // Récupérer les stats
  const creatorIds = creators.map(c => c.id);
  const placeholders = creatorIds.map(() => '?').join(',');

  const stats = queryAll(`
    SELECT
      c.name,
      c.platform,
      c.commission_rate,
      ds.date,
      ds.subscribers,
      ds.revenue
    FROM daily_stats ds
    JOIN creators c ON ds.creator_id = c.id
    WHERE ds.creator_id IN (${placeholders})
    AND ds.date BETWEEN ? AND ?
    ORDER BY ds.date
  `, [...creatorIds, startDate, endDate]);

  // Déterminer le taux de commission selon la créatrice
  const getCommissionRate = (name) => {
    if (name.toLowerCase().includes('georgina')) return 0.50;
    if (name.toLowerCase().includes('jade')) return 0.60;
    return 0.40; // Taux par défaut
  };

  const commissionRate = getCommissionRate(creatorName);

  // Calculer les totaux par plateforme
  const totals = {};
  stats.forEach(stat => {
    const key = stat.platform;
    if (!totals[key]) {
      totals[key] = { subs: 0, revenue: 0, commission_rate: commissionRate };
    }
    totals[key].subs += stat.subscribers;
    totals[key].revenue += stat.revenue;
  });

  // Créer le PDF
  const doc = new PDFDocument({ margin: 50, size: 'A4' });

  res.setHeader('Content-Type', 'application/pdf');
  res.setHeader('Content-Disposition', `attachment; filename=rapport_${creatorName}_${startDate}_${endDate}.pdf`);

  doc.pipe(res);

  // Header
  doc.fontSize(24).font('Helvetica-Bold').text('Rapport de Performance', { align: 'center' });
  doc.moveDown(0.5);
  doc.fontSize(18).font('Helvetica').text(creatorName, { align: 'center' });
  doc.moveDown(0.3);
  doc.fontSize(12).fillColor('#666')
    .text(`Période: ${formatDate(startDate)} - ${formatDate(endDate)}`, { align: 'center' });
  doc.moveDown(2);

  // Ligne de séparation
  doc.strokeColor('#e5e7eb').lineWidth(1)
    .moveTo(50, doc.y).lineTo(545, doc.y).stroke();
  doc.moveDown(1);

  // Résumé global
  doc.fillColor('#000').fontSize(16).font('Helvetica-Bold').text('Résumé Global');
  doc.moveDown(0.5);

  let totalGlobalSubs = 0;
  let totalGlobalRevenue = 0;
  let totalGlobalProfit = 0;

  Object.entries(totals).forEach(([platform, data]) => {
    totalGlobalSubs += data.subs;
    totalGlobalRevenue += data.revenue;
    totalGlobalProfit += data.revenue * data.commission_rate;
  });

  const ltv = totalGlobalSubs > 0 ? totalGlobalRevenue / totalGlobalSubs : 0;

  // KPIs en grid
  doc.fontSize(11).font('Helvetica');

  const kpis = [
    { label: 'Total Fans', value: formatNumber(totalGlobalSubs) },
    { label: 'Chiffre d\'Affaires', value: formatEuro(totalGlobalRevenue) },
    { label: 'LTV Moyenne', value: formatEuro(ltv, 2) },
    { label: 'Commission Agence', value: formatEuro(totalGlobalProfit) }
  ];

  const kpiY = doc.y;
  kpis.forEach((kpi, i) => {
    const x = 50 + (i % 2) * 250;
    const y = kpiY + Math.floor(i / 2) * 50;

    doc.fillColor('#6b7280').fontSize(10).text(kpi.label, x, y);
    doc.fillColor('#000').fontSize(16).font('Helvetica-Bold').text(kpi.value, x, y + 15);
    doc.font('Helvetica');
  });

  doc.y = kpiY + 120;

  // Détails par plateforme
  Object.entries(totals).forEach(([platform, data]) => {
    doc.moveDown(1);
    doc.strokeColor('#e5e7eb').lineWidth(1)
      .moveTo(50, doc.y).lineTo(545, doc.y).stroke();
    doc.moveDown(1);

    const platformName = platform === 'OF' ? 'OnlyFans' : 'MYM.fans';
    const platformColor = platform === 'OF' ? '#000000' : '#8B5CF6';

    doc.fillColor(platformColor).fontSize(14).font('Helvetica-Bold')
      .text(`${platformName}`, { continued: false });
    doc.moveDown(0.5);

    doc.fillColor('#000').fontSize(11).font('Helvetica');

    const platformLTV = data.subs > 0 ? data.revenue / data.subs : 0;
    const profit = data.revenue * data.commission_rate;

    doc.text(`Fans: ${formatNumber(data.subs)}`);
    doc.text(`Chiffre d'affaires: ${formatEuro(data.revenue)}`);
    doc.text(`LTV: ${formatEuro(platformLTV, 2)}`);
    doc.text(`Commission (${(data.commission_rate * 100).toFixed(0)}%): ${formatEuro(profit)}`);
  });

  // Analyse et recommandations
  doc.moveDown(2);
  doc.strokeColor('#e5e7eb').lineWidth(1)
    .moveTo(50, doc.y).lineTo(545, doc.y).stroke();
  doc.moveDown(1);

  doc.fillColor('#000').fontSize(14).font('Helvetica-Bold').text('Analyse & Recommandations');
  doc.moveDown(0.5);
  doc.fontSize(11).font('Helvetica');

  const TARGET_SUBS = 800;
  const TARGET_LTV = 15;

  if (totalGlobalSubs < TARGET_SUBS) {
    doc.fillColor('#f59e0b').text('! ', { continued: true });
    doc.fillColor('#000').text(`Focus Marketing recommandé - Objectif: ${TARGET_SUBS} abonnés/mois (actuellement ${totalGlobalSubs})`);
  } else if (ltv < TARGET_LTV) {
    doc.fillColor('#3b82f6').text('> ', { continued: true });
    doc.fillColor('#000').text(`Focus Chatting recommandé - Objectif: LTV de ${TARGET_LTV}€ (actuellement ${ltv.toFixed(2)}€)`);
  } else {
    doc.fillColor('#10b981').text('+ ', { continued: true });
    doc.fillColor('#000').text('Excellente performance! Focus sur le scaling.');
  }

  // Footer
  doc.moveDown(3);
  doc.fontSize(9).fillColor('#9ca3af')
    .text(`Rapport généré le ${new Date().toLocaleDateString('fr-FR')} à ${new Date().toLocaleTimeString('fr-FR')}`, { align: 'center' });
  doc.text('Dashboard Agence LTP', { align: 'center' });

  doc.end();
});

// Générer un rapport PDF global de l'agence
router.get('/pdf-agency', (req, res) => {
  const { start_date, end_date } = req.query;

  const endDate = end_date || new Date().toISOString().split('T')[0];
  const startDate = start_date || (() => {
    const d = new Date();
    d.setDate(d.getDate() - 30);
    return d.toISOString().split('T')[0];
  })();

  // Récupérer toutes les stats
  const stats = queryAll(`
    SELECT
      c.name,
      c.platform,
      c.commission_rate,
      ds.date,
      ds.subscribers,
      ds.revenue
    FROM daily_stats ds
    JOIN creators c ON ds.creator_id = c.id
    WHERE ds.date BETWEEN ? AND ?
    AND c.active = 1
    ORDER BY c.name, c.platform, ds.date
  `, [startDate, endDate]);

  // Déterminer le taux de commission selon la créatrice
  const getCommissionRateByName = (name) => {
    if (name.toLowerCase().includes('georgina')) return 0.50;
    if (name.toLowerCase().includes('jade')) return 0.60;
    return 0.40;
  };

  // Calculer les totaux par créatrice
  const byCreator = {};
  stats.forEach(stat => {
    const key = `${stat.name} ${stat.platform}`;
    if (!byCreator[key]) {
      byCreator[key] = {
        name: stat.name,
        platform: stat.platform,
        subs: 0,
        revenue: 0,
        commission_rate: getCommissionRateByName(stat.name)
      };
    }
    byCreator[key].subs += stat.subscribers;
    byCreator[key].revenue += stat.revenue;
  });

  // Créer le PDF
  const doc = new PDFDocument({ margin: 50, size: 'A4' });

  res.setHeader('Content-Type', 'application/pdf');
  res.setHeader('Content-Disposition', `attachment; filename=rapport_agence_${startDate}_${endDate}.pdf`);

  doc.pipe(res);

  // Header
  doc.fontSize(24).font('Helvetica-Bold').text('Rapport Agence LTP', { align: 'center' });
  doc.moveDown(0.5);
  doc.fontSize(12).fillColor('#666')
    .text(`Période: ${formatDate(startDate)} - ${formatDate(endDate)}`, { align: 'center' });
  doc.moveDown(2);

  // Calculs globaux
  let totalSubs = 0;
  let totalRevenue = 0;
  let totalProfit = 0;

  Object.values(byCreator).forEach(data => {
    totalSubs += data.subs;
    totalRevenue += data.revenue;
    totalProfit += data.revenue * data.commission_rate;
  });

  const ltv = totalSubs > 0 ? totalRevenue / totalSubs : 0;

  // KPIs globaux
  doc.fillColor('#000').fontSize(16).font('Helvetica-Bold').text('Performance Globale');
  doc.moveDown(0.5);

  doc.strokeColor('#e5e7eb').lineWidth(1)
    .moveTo(50, doc.y).lineTo(545, doc.y).stroke();
  doc.moveDown(0.5);

  const kpis = [
    { label: 'Total Fans', value: formatNumber(totalSubs) },
    { label: 'CA Total', value: formatEuro(totalRevenue) },
    { label: 'LTV Moyenne', value: formatEuro(ltv, 2) },
    { label: 'Profit Agence', value: formatEuro(totalProfit) }
  ];

  const kpiY = doc.y;
  doc.fontSize(11).font('Helvetica');
  kpis.forEach((kpi, i) => {
    const x = 50 + (i % 2) * 250;
    const y = kpiY + Math.floor(i / 2) * 50;

    doc.fillColor('#6b7280').fontSize(10).text(kpi.label, x, y);
    doc.fillColor('#000').fontSize(16).font('Helvetica-Bold').text(kpi.value, x, y + 15);
    doc.font('Helvetica');
  });

  doc.y = kpiY + 120;

  // Détail par créatrice
  doc.moveDown(1);
  doc.fillColor('#000').fontSize(16).font('Helvetica-Bold').text('Détail par Créatrice');
  doc.moveDown(0.5);

  // Grouper par nom
  const byName = {};
  Object.values(byCreator).forEach(data => {
    if (!byName[data.name]) {
      byName[data.name] = [];
    }
    byName[data.name].push(data);
  });

  Object.entries(byName).forEach(([name, platforms]) => {
    doc.strokeColor('#e5e7eb').lineWidth(1)
      .moveTo(50, doc.y).lineTo(545, doc.y).stroke();
    doc.moveDown(0.5);

    doc.fillColor('#000').fontSize(14).font('Helvetica-Bold').text(name);
    doc.moveDown(0.3);

    let creatorTotalSubs = 0;
    let creatorTotalRevenue = 0;
    let creatorTotalProfit = 0;

    platforms.forEach(platform => {
      const platformName = platform.platform === 'OF' ? 'OnlyFans' : 'MYM.fans';
      const profit = platform.revenue * platform.commission_rate;

      creatorTotalSubs += platform.subs;
      creatorTotalRevenue += platform.revenue;
      creatorTotalProfit += profit;

      doc.fontSize(10).font('Helvetica').fillColor('#6b7280')
        .text(`${platformName}: ${formatNumber(platform.subs)} fans - ${formatEuro(platform.revenue)} CA - ${formatEuro(profit)} profit`);
    });

    const creatorLTV = creatorTotalSubs > 0 ? creatorTotalRevenue / creatorTotalSubs : 0;
    doc.fontSize(11).font('Helvetica-Bold').fillColor('#000')
      .text(`Total: ${formatNumber(creatorTotalSubs)} fans - ${formatEuro(creatorTotalRevenue)} CA - LTV ${formatEuro(creatorLTV, 2)} - ${formatEuro(creatorTotalProfit)} profit`);

    doc.moveDown(0.5);
  });

  // Footer
  doc.moveDown(2);
  doc.fontSize(9).fillColor('#9ca3af')
    .text(`Rapport généré le ${new Date().toLocaleDateString('fr-FR')} à ${new Date().toLocaleTimeString('fr-FR')}`, { align: 'center' });
  doc.text('Dashboard Agence LTP', { align: 'center' });

  doc.end();
});

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  });
}

// Formater les nombres avec espaces (format français)
function formatNumber(num, decimals = 0) {
  return num.toLocaleString('fr-FR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  });
}

// Formater les montants en euros
function formatEuro(num, decimals = 0) {
  return `${formatNumber(num, decimals)} €`;
}

module.exports = router;
