const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = 8000;
const HOSTNAME = 'localhost';

const server = http.createServer((req, res) => {
    // Default to index.html for root path
    let filePath = req.url === '/' ? '/index.html' : req.url;
    filePath = path.join(__dirname, filePath);

    // Security: prevent directory traversal
    const realPath = fs.realpathSync(__dirname);
    if (!fs.realpathSync(filePath).startsWith(realPath)) {
        res.statusCode = 403;
        res.end('Forbidden');
        return;
    }

    // Get file extension
    const ext = path.extname(filePath);
    
    // Set content type
    let contentType = 'text/html';
    switch(ext) {
        case '.js':
            contentType = 'text/javascript';
            break;
        case '.css':
            contentType = 'text/css';
            break;
        case '.json':
            contentType = 'application/json';
            break;
        case '.png':
            contentType = 'image/png';
            break;
        case '.jpg':
        case '.jpeg':
            contentType = 'image/jpeg';
            break;
        case '.svg':
            contentType = 'image/svg+xml';
            break;
    }

    // Read and serve file
    fs.readFile(filePath, (err, data) => {
        if (err) {
            if (err.code === 'ENOENT') {
                res.statusCode = 404;
                res.setHeader('Content-Type', 'text/html');
                res.end('<h1>404 - File Not Found</h1>');
            } else {
                res.statusCode = 500;
                res.end('Server Error');
            }
        } else {
            res.statusCode = 200;
            res.setHeader('Content-Type', contentType);
            res.setHeader('Access-Control-Allow-Origin', '*');
            res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
            res.end(data);
        }
    });
});

server.listen(PORT, HOSTNAME, () => {
    console.log('\n' + '='.repeat(60));
    console.log('🌐 ZKAS Website Server');
    console.log('='.repeat(60));
    console.log(`\n✓ Server running at: http://${HOSTNAME}:${PORT}`);
    console.log(`✓ Open your browser and visit: http://${HOSTNAME}:${PORT}`);
    console.log(`✓ Press Ctrl+C to stop\n`);
});

// Handle server close
server.on('close', () => {
    console.log('\n✓ Server stopped');
    console.log('='.repeat(60) + '\n');
});

// Handle errors
server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.error(`✗ Port ${PORT} is already in use`);
        console.error('Please close other applications or use a different port');
    } else {
        console.error('Server error:', err);
    }
    process.exit(1);
});
