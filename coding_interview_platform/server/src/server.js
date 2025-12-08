const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const cors = require('cors');

const app = express();
app.use(cors());

// Serve client build if present
const clientDist = path.join(__dirname, '..', '..', 'client');
app.use(express.static(clientDist));

app.get('/new', (req, res) => {
  const id = uuidv4();
  res.json({ room: id, url: `/${id}` });
});

app.get('/:room([0-9a-fA-F\\-]{36})', (req, res) => {
  // serve the client entrypoint for any room
  res.sendFile(path.join(clientDist, 'index.html'));
});

const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: '*',
  }
});

io.on('connection', (socket) => {
  socket.on('join', (room) => {
    socket.join(room);
    socket.room = room;
  });

  socket.on('code_change', (payload) => {
    // payload: {room, code}
    const room = payload.room || socket.room;
    if (!room) return;
    // broadcast to others in the room
    socket.to(room).emit('code_update', { code: payload.code, lang: payload.lang });
  });

  socket.on('lang_change', (payload) => {
    const room = payload.room || socket.room;
    if (!room) return;
    socket.to(room).emit('lang_update', { lang: payload.lang });
  });

  socket.on('disconnect', () => {});
});

// Only start listening if this is the main module
if (require.main === module) {
  const PORT = process.env.PORT || 3000;
  server.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
  });
}

module.exports = { app, server, io };
