# Coding Interview Platform

This is a minimal collaborative coding interview platform prototype.

Architecture
- Backend: Node.js + Express + Socket.IO (handles rooms and realtime messaging)
- Frontend: Static JS using CodeMirror (syntax highlighting) and socket.io-client
- Browser-based code execution:
  - Python: Pyodide (WASM, runs in browser)
  - JavaScript: QuickJS via WASM (if available) or sandboxed iframe fallback

Run locally
1. Install root dev deps:

```bash
cd coding_interview_platform
npm install
```

2. Install server and client deps:
```bash
cd server && npm install
cd ../client && npm install
```

3. Run server and client concurrently (root):
```bash
npm start
```
This runs server on port 3000 and client on 8080 (the server also serves static client files).

Or just run server which serves the client directory:
```bash
cd server
npm start
# opens on http://localhost:3000
```

Create a shareable link:
- Visit `http://localhost:3000/new` to get a JSON response containing a `room` and `url` such as `/ <uuid>`
- Open `http://localhost:3000/<uuid>` in multiple browsers; edits will sync in real-time.

Run tests
- Tests are in `server/test`. From root run:
```bash
npm test
```

Docker
- Build image from repository root:
```bash
docker build -t cip-app ./coding_interview_platform
```
- Run container:
```bash
docker run -p 3000:3000 cip-app
```

Deploy to Render
- Create a Web Service on Render connected to this repo and set the start command to `node server/src/server.js`.
- Or use the GitHub Actions workflow (see `.github/workflows/ci.yml`) which calls the Render API. You must add the following secrets to your repository:
  - `RENDER_SERVICE_ID` (the Render service id)
  - `RENDER_API_KEY` (API key with deploy permission)

CI/CD (GitHub Actions)
- The workflow will:
  1. Run server and client tests
  2. If tests pass, POST to Render API to trigger a deploy

Notes & Limitations
- This is a prototype. The editor synchronization is naive: full-document updates (debounced). For production use, use CRDT/OT (e.g., Yjs, ShareDB) to avoid conflicts.
- QuickJS WASM usage is attempted via CDN; if not present we fall back to a sandboxed iframe for JS execution.
- Pyodide is loaded from CDN on first Python run (large download).

If you want, I can:
- Replace naive synchronization with Yjs for robust CRDT-based realtime editing.
- Add authentication (GitHub/Google) and per-user session handling.
- Expand the CI workflow to build Docker image and push to a registry.

