import { preview } from 'vite';
import http from 'http';

async function testServer() {
  const server = await preview({
    preview: { port: 4173 },
  });
  console.log('VITE_PREVIEW_URL:', server.resolvedUrls.local[0]);

  http.get('http://localhost:4173/', (res) => {
    console.log('HTTP_STATUS:', res.statusCode);
    console.log('CONTENT_TYPE:', res.headers['content-type']);
    let body = '';
    res.on('data', (chunk) => (body += chunk));
    res.on('end', () => {
      console.log('CONTAINS_ROOT:', body.includes('<div id="root">'));
      console.log('CONTAINS_DOCUEASE:', body.includes('DocuEase'));
      server.httpServer.close();
      process.exit(0);
    });
  });
}

testServer();
