const { google } = require('googleapis');
const fs = require('fs');

async function main() {
  const credentialsJson = process.env.GCP_CREDENTIALS;
  if (!credentialsJson) {
    console.error("GCP_CREDENTIALS not found in environment.");
    process.exit(1);
  }

  // File containing a list of URLs that were modified (passed by the workflow)
  const modifiedFiles = fs.readFileSync('modified_files.txt', 'utf-8').split('\n').filter(Boolean);
  
  if (modifiedFiles.length === 0) {
    console.log("No URLs to update.");
    return;
  }

  const credentials = JSON.parse(credentialsJson);
  const auth = new google.auth.JWT(
    credentials.client_email,
    null,
    credentials.private_key,
    ['https://www.googleapis.com/auth/indexing'],
    null
  );

  const indexing = google.indexing({
    version: 'v3',
    auth: auth
  });

  for (const filepath of modifiedFiles) {
    if (!filepath.endsWith('.html')) continue;

    // Convert local filepath to production URL
    // e.g. "blog/article.html" -> "https://zyekh.com/blog/article.html"
    const url = `https://zyekh.com/${filepath.replace('index.html', '')}`;

    try {
      const res = await indexing.urlNotifications.publish({
        requestBody: {
          url: url,
          type: 'URL_UPDATED'
        }
      });
      console.log(`Successfully notified Google for: ${url}`);
    } catch (e) {
      console.error(`Failed to notify Google for ${url}:`, e.message);
    }
  }
}

main().catch(console.error);
