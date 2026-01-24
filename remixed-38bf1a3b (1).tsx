import React, { useState, useMemo, useEffect } from 'react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { TrendingUp, Users, DollarSign, Target, Award, MessageCircle, Megaphone, Zap, RefreshCw } from 'lucide-react';

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

const COLORS = {"Georgina OF": "#000000", "Georgina MYM": "#666666", "Jade OF": "#3B82F6", "Jade MYM": "#93C5FD"};
const TARGET_SUBS = 800, TARGET_LTV = 15;
const STORAGE_KEY = 'agency-dashboard-data';

export default function AgencyDashboard() {
  const [rawData, setRawData] = useState(initialData);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState(30);
  const [lastUpdate, setLastUpdate] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const result = await window.storage.get(STORAGE_KEY, true);
      if (result && result.value) {
        setRawData(JSON.parse(result.value));
      }
    } catch (e) { console.log('Using initial data'); }
    setLoading(false);
    setLastUpdate(new Date());
  };

  const lastDataDate = useMemo(() => {
    const allDates = Object.values(rawData).flatMap(arr => arr.map(d => d.date));
    return allDates.length ? new Date(Math.max(...allDates.map(d => new Date(d)))) : new Date();
  }, [rawData]);

  const getFilteredData = (creatorName, days) => {
    const data = rawData[creatorName] || [];
    const cutoff = new Date(lastDataDate);
    cutoff.setDate(cutoff.getDate() - days + 1);
    return data.filter(d => new Date(d.date) >= cutoff && new Date(d.date) <= lastDataDate);
  };

  const calculateLTV = (data) => {
    const totalCA = data.reduce((sum, d) => sum + d.ca, 0);
    const totalSubs = data.reduce((sum, d) => sum + d.sub, 0);
    return totalSubs > 0 ? totalCA / totalSubs : 0;
  };

  const getCreatorFocus = (subs, ltv) => {
    if (subs < TARGET_SUBS) return { focus: "Focus Marketing", icon: Megaphone, type: "marketing" };
    if (ltv < TARGET_LTV) return { focus: "Focus Chatting", icon: MessageCircle, type: "chatting" };
    return { focus: "Focus Scale", icon: Zap, type: "scale" };
  };

  const stats = useMemo(() => {
    const creators = Object.keys(rawData);
    const result = {};
    creators.forEach(creator => {
      const last30 = getFilteredData(creator, 30);
      result[creator] = { subs: last30.reduce((s, d) => s + d.sub, 0), ca: last30.reduce((s, d) => s + d.ca, 0), ltv: calculateLTV(last30), dailyData: last30 };
    });
    return result;
  }, [rawData]);

  const globalStats = useMemo(() => {
    const creators = Object.keys(rawData);
    const cutoff = new Date(lastDataDate);
    cutoff.setDate(cutoff.getDate() - dateRange + 1);
    const result = {};
    creators.forEach(creator => {
      const data = (rawData[creator] || []).filter(d => new Date(d.date) >= cutoff && new Date(d.date) <= lastDataDate);
      result[creator] = { subs: data.reduce((s, d) => s + d.sub, 0), ca: data.reduce((s, d) => s + d.ca, 0) };
    });
    const georginaCA = (result["Georgina OF"]?.ca || 0) + (result["Georgina MYM"]?.ca || 0);
    const jadeCA = (result["Jade OF"]?.ca || 0) + (result["Jade MYM"]?.ca || 0);
    const totalSubs = Object.values(result).reduce((s, c) => s + c.subs, 0);
    const totalCA = Object.values(result).reduce((s, c) => s + c.ca, 0);
    return { subs: totalSubs, ca: totalCA, ltv: totalSubs > 0 ? totalCA / totalSubs : 0, profit: georginaCA * 0.38 + jadeCA * 0.48 };
  }, [dateRange, rawData, lastDataDate]);

  const totalCA = Object.values(stats).reduce((s, v) => s + v.ca, 0);

  const chartData = useMemo(() => {
    const dates = [];
    const cutoff = new Date(lastDataDate);
    cutoff.setDate(cutoff.getDate() - 29);
    for (let d = new Date(cutoff); d <= lastDataDate; d.setDate(d.getDate() + 1)) {
      const dateStr = d.toISOString().split('T')[0];
      const dayData = { date: dateStr, displayDate: new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit' }) };
      let totalDayCA = 0;
      Object.keys(rawData).forEach(creator => {
        const found = (rawData[creator] || []).find(r => r.date === dateStr);
        dayData[`${creator}_sub`] = found ? found.sub : 0;
        dayData[`${creator}_ca`] = found ? found.ca : 0;
        totalDayCA += found ? found.ca : 0;
      });
      dayData.total_ca = totalDayCA;
      dates.push(dayData);
    }
    return dates;
  }, [rawData, lastDataDate]);

  const pieData = Object.keys(rawData).map(creator => ({
    name: creator, value: stats[creator]?.ca || 0, percent: totalCA > 0 ? (((stats[creator]?.ca || 0) / totalCA) * 100).toFixed(1) : 0, color: COLORS[creator]
  }));

  const KPICard = ({ title, value, unit, icon: Icon, subtitle }) => (
    <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-xl bg-gray-100 flex items-center justify-center"><Icon className="w-5 h-5 text-gray-600" /></div>
        <span className="text-sm text-gray-500 font-medium">{title}</span>
      </div>
      <p className="text-3xl font-semibold text-gray-900 tracking-tight">
        {typeof value === 'number' ? value.toLocaleString('fr-FR', { maximumFractionDigits: 2 }) : value}
        <span className="text-lg text-gray-400 ml-1 font-normal">{unit}</span>
      </p>
      {subtitle && <p className="text-sm text-gray-400 mt-1">{subtitle}</p>}
    </div>
  );

  const CreatorCard = ({ creator }) => {
    const data = stats[creator] || { subs: 0, ca: 0, ltv: 0, dailyData: [] };
    const platform = creator.includes('OF') ? 'OF' : 'MYM';
    const name = creator.replace(' OF', '').replace(' MYM', '');
    const focusInfo = getCreatorFocus(data.subs, data.ltv);
    const FocusIcon = focusInfo.icon;
    const progressValue = focusInfo.type === 'marketing' ? Math.min((data.subs / TARGET_SUBS) * 100, 100) : focusInfo.type === 'chatting' ? Math.min((data.ltv / TARGET_LTV) * 100, 100) : 100;
    const progressLabel = focusInfo.type === 'marketing' ? `${data.subs} / ${TARGET_SUBS} subs` : focusInfo.type === 'chatting' ? `${data.ltv.toFixed(2)}€ / ${TARGET_LTV}€ LTV` : 'Objectifs atteints';
    return (
      <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center text-white font-bold text-sm ${platform === 'OF' ? 'bg-black' : 'bg-gradient-to-br from-purple-500 to-pink-500'}`}>{platform}</div>
            <div><h3 className="text-lg font-semibold text-gray-900">{name}</h3><span className="text-xs text-gray-400">{platform === 'OF' ? 'OnlyFans' : 'MYM.fans'}</span></div>
          </div>
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium ${focusInfo.type === 'marketing' ? 'bg-amber-50 text-amber-700' : focusInfo.type === 'chatting' ? 'bg-blue-50 text-blue-700' : 'bg-emerald-50 text-emerald-700'}`}>
            <FocusIcon className="w-3.5 h-3.5" />{focusInfo.focus}
          </div>
        </div>
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div><p className="text-xs text-gray-400 mb-1">Subs L30</p><p className="text-xl font-semibold text-gray-900">{data.subs.toLocaleString('fr-FR')}</p></div>
          <div><p className="text-xs text-gray-400 mb-1">CA L30</p><p className="text-xl font-semibold text-gray-900">{data.ca.toLocaleString('fr-FR', {maximumFractionDigits: 0})}€</p></div>
          <div><p className="text-xs text-gray-400 mb-1">LTV L30</p><p className="text-xl font-semibold text-gray-900">{data.ltv.toFixed(2)}€</p></div>
        </div>
        <div>
          <div className="flex justify-between text-xs mb-2"><span className="text-gray-500">{focusInfo.type === 'scale' ? 'Performance' : 'Objectif'}</span><span className="text-gray-700 font-medium">{progressLabel}</span></div>
          <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
            <div className={`h-full rounded-full transition-all duration-700 ${focusInfo.type === 'marketing' ? 'bg-amber-500' : focusInfo.type === 'chatting' ? 'bg-blue-500' : 'bg-emerald-500'}`} style={{ width: `${progressValue}%` }} />
          </div>
        </div>
        <div className="h-16 mt-4">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={(data.dailyData || []).slice(-14)}>
              <defs><linearGradient id={`mini-${creator.replace(/ /g, '')}`} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={COLORS[creator]} stopOpacity={0.2} /><stop offset="100%" stopColor={COLORS[creator]} stopOpacity={0} /></linearGradient></defs>
              <Area type="monotone" dataKey="ca" stroke={COLORS[creator]} strokeWidth={1.5} fill={`url(#mini-${creator.replace(/ /g, '')})`} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (!active || !payload) return null;
    return (
      <div className="bg-white border border-gray-200 rounded-xl p-4 shadow-lg">
        <p className="text-gray-500 text-sm mb-2 font-medium">{label}</p>
        {payload.map((p, i) => (
          <div key={i} className="flex items-center gap-2 text-sm py-0.5">
            <div className="w-2 h-2 rounded-full" style={{ background: p.color }} />
            <span className="text-gray-600">{p.name}:</span>
            <span className="font-semibold text-gray-900">{typeof p.value === 'number' ? p.value.toLocaleString('fr-FR', {maximumFractionDigits: 0}) : p.value}{p.name.includes('ca') || p.name === 'Total Agence' ? '€' : ''}</span>
          </div>
        ))}
      </div>
    );
  };

  if (loading) {
    return <div className="min-h-screen bg-gray-50 flex items-center justify-center"><RefreshCw className="w-8 h-8 text-gray-400 animate-spin" /></div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'); * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }`}</style>
      <header className="bg-white border-b border-gray-100 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div><h1 className="text-xl font-semibold text-gray-900">Agency Dashboard</h1><p className="text-sm text-gray-400">Performance overview</p></div>
            <div className="flex items-center gap-6">
              <div className="flex items-center bg-gray-100 rounded-xl p-1">
                {[7, 14, 30, 60].map((days) => (
                  <button key={days} onClick={() => setDateRange(days)} className={`px-4 py-2 text-sm font-medium rounded-lg transition-all ${dateRange === days ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}>{days}j</button>
                ))}
              </div>
              <button onClick={loadData} className="p-2 rounded-xl bg-gray-100 text-gray-600 hover:bg-gray-200 transition-all"><RefreshCw className="w-5 h-5" /></button>
              <div className="text-right"><p className="text-xs text-gray-400">Dernière donnée</p><p className="text-sm font-medium text-gray-700">{lastDataDate.toLocaleDateString('fr-FR')}</p></div>
            </div>
          </div>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <KPICard title={`Subscribers L${dateRange}`} value={globalStats.subs} unit="subs" icon={Users} subtitle={`${(globalStats.subs / dateRange).toFixed(0)}/jour`} />
          <KPICard title={`CA L${dateRange}`} value={globalStats.ca.toFixed(0)} unit="€" icon={DollarSign} subtitle={`${(globalStats.ca / dateRange).toFixed(0)}€/jour`} />
          <KPICard title={`LTV L${dateRange}`} value={globalStats.ltv.toFixed(2)} unit="€" icon={Target} subtitle="CA ÷ Subs" />
          <KPICard title={`Profit Agence L${dateRange}`} value={globalStats.profit.toFixed(0)} unit="€" icon={Award} subtitle="Georgina 38% • Jade 48%" />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-8">{Object.keys(rawData).map(creator => <CreatorCard key={creator} creator={creator} />)}</div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-8">
          <div className="lg:col-span-2 bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-base font-semibold text-gray-900">Évolution du CA</h3>
              <div className="flex gap-4 text-xs">{Object.keys(rawData).map(creator => (<div key={creator} className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full" style={{ background: COLORS[creator] }} /><span className="text-gray-500">{creator}</span></div>))}</div>
            </div>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="displayDate" stroke="#94a3b8" fontSize={11} tickLine={false} axisLine={false} />
                  <YAxis stroke="#94a3b8" fontSize={11} tickLine={false} axisLine={false} tickFormatter={(v) => `${v}€`} />
                  <Tooltip content={<CustomTooltip />} />
                  {Object.keys(rawData).map(creator => (<Line key={creator} type="monotone" dataKey={`${creator}_ca`} name={creator} stroke={COLORS[creator]} strokeWidth={2} dot={false} />))}
                  <Line type="monotone" dataKey="total_ca" name="Total Agence" stroke="#10B981" strokeWidth={2.5} strokeDasharray="5 5" dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
            <h3 className="text-base font-semibold text-gray-900 mb-6">Répartition CA L30</h3>
            <div className="h-48">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart><Pie data={pieData} cx="50%" cy="50%" innerRadius={50} outerRadius={75} paddingAngle={2} dataKey="value">{pieData.map((entry, index) => <Cell key={index} fill={entry.color} />)}</Pie></PieChart>
              </ResponsiveContainer>
            </div>
            <div className="space-y-2 mt-4">
              {pieData.map(item => (<div key={item.name} className="flex items-center justify-between text-sm"><div className="flex items-center gap-2"><div className="w-2 h-2 rounded-full" style={{ background: item.color }} /><span className="text-gray-600">{item.name}</span></div><div className="text-right"><span className="font-medium text-gray-900">{item.value.toLocaleString('fr-FR', {maximumFractionDigits: 0})}€</span><span className="text-gray-400 ml-2">({item.percent}%)</span></div></div>))}
            </div>
          </div>
        </div>
        <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-base font-semibold text-gray-900">Évolution des Fans</h3>
            <div className="flex gap-4 text-xs">{Object.keys(rawData).map(creator => (<div key={creator} className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full" style={{ background: COLORS[creator] }} /><span className="text-gray-500">{creator}</span></div>))}</div>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <defs>{Object.keys(rawData).map(creator => (<linearGradient key={creator} id={`area-${creator.replace(/ /g, '')}`} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={COLORS[creator]} stopOpacity={0.3} /><stop offset="100%" stopColor={COLORS[creator]} stopOpacity={0.05} /></linearGradient>))}</defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="displayDate" stroke="#94a3b8" fontSize={11} tickLine={false} axisLine={false} />
                <YAxis stroke="#94a3b8" fontSize={11} tickLine={false} axisLine={false} />
                <Tooltip content={<CustomTooltip />} />
                {Object.keys(rawData).map(creator => (<Area key={creator} type="monotone" dataKey={`${creator}_sub`} name={creator} stroke={COLORS[creator]} strokeWidth={2} fill={`url(#area-${creator.replace(/ /g, '')})`} />))}
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </main>
      <footer className="border-t border-gray-100 mt-12 py-6"><p className="text-center text-sm text-gray-400">Dashboard Agency • Données jusqu'au {lastDataDate.toLocaleDateString('fr-FR')}</p></footer>
    </div>
  );
}
