// Script d'auto-update pour les articles
// Ce script peut être exécuté par un cron job toutes les heures

import fetch from 'node-fetch';
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const SUPABASE_URL = process.env.SUPABASE_URL;
const SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;

function parseArgs() {
  const args = process.argv.slice(2);
  const result = {
    maxPerSite: 5,
    limitSites: undefined,
    rescrapeFile: undefined,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if ((arg === '--max' || arg === '--maxPerSite') && args[i + 1]) {
      result.maxPerSite = Number(args[++i]);
    } else if ((arg === '--limit' || arg === '--limitSites') && args[i + 1]) {
      result.limitSites = Number(args[++i]);
    } else if ((arg === '--rescrape' || arg === '--urls') && args[i + 1]) {
      result.rescrapeFile = args[++i];
    }
  }

  return result;
}

async function loadRescrapeUrls(filePath) {
  if (!filePath) return [];
  try {
    const abs = path.isAbsolute(filePath) ? filePath : path.join(process.cwd(), filePath);
    if (!fs.existsSync(abs)) return [];
    const content = fs.readFileSync(abs, 'utf-8');
    return content
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter((line) => line.startsWith('http'));
  } catch (error) {
    console.error('⚠️ Impossible de lire le fichier rescrape:', error);
    return [];
  }
}

async function main() {
  if (!SUPABASE_URL || !SERVICE_ROLE_KEY) {
    console.error('❌ Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY environment variables.');
    process.exit(1);
  }

  const options = parseArgs();
  const rescrapeUrls = await loadRescrapeUrls(options.rescrapeFile);

  console.log('🚀 Triggering auto-update (cron/manual)...');
  console.log('   maxPerSite =', options.maxPerSite);
  if (options.limitSites) console.log('   limitSites =', options.limitSites);
  if (rescrapeUrls.length) console.log(`   rescrapeUrls (${rescrapeUrls.length}) loaded.`);

  try {
    const response = await fetch(`${SUPABASE_URL}/functions/v1/auto-update-news`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${SERVICE_ROLE_KEY}`,
      },
      body: JSON.stringify({
        maxPerSite: options.maxPerSite,
        limitSites: options.limitSites,
        rescrapeUrls: rescrapeUrls.length ? rescrapeUrls : undefined,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('❌ auto-update-news failed:', response.status, errorText);
      process.exit(1);
    }

    const json = await response.json();
    console.log('✅ Auto-update completed:', json);
  } catch (error) {
    console.error('❌ auto-update error:', error);
    process.exit(1);
  }
}

main();
