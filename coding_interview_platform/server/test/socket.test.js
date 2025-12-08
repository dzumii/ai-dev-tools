const { server } = require('../src/server');
const ioClient = require('socket.io-client');

const URL = 'http://localhost:3001';
let httpServer;

beforeAll((done) => {
  // start server on different port for tests
  httpServer = server.listen(3001, () => done());
});

afterAll((done) => {
  httpServer.close(() => done());
});

test('broadcasts code change to other clients in room', (done) => {
  const room = 'test-room-1234-5678-1234-567812345678';
  const client1 = ioClient(URL);
  const client2 = ioClient(URL);

  client1.on('connect', () => {
    client1.emit('join', room);
    // give second client a moment
    setTimeout(() => {
      client2.emit('join', room);
      setTimeout(() => {
        const payload = { room, code: 'console.log(1)', lang: 'javascript' };
        client2.emit('code_change', payload);
      }, 50);
    }, 50);
  });

  client1.on('code_update', (data) => {
    expect(data.code).toBe('console.log(1)');
    client1.close();
    client2.close();
    done();
  });
});
