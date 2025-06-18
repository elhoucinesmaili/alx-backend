import express from 'express';
import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';

const app = express();
const port = 1245;

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

const queue = kue.createQueue();
let reservationEnabled = true;

async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return parseInt(seats) || 0;
}

// Initialize
reserveSeat(50);

app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats.toString() });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: "Reservation are blocked" });
    return;
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      res.json({ status: "Reservation failed" });
    } else {
      res.json({ status: "Reservation in process" });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err}`);
  });
});

app.get('/process', async (req, res) => {
  res.json({ status: "Queue processing" });

  queue.process('reserve_seat', async (job, done) => {
    const currentSeats = await getCurrentAvailableSeats();
    const newSeats = currentSeats - 1;

    if (newSeats < 0) {
      done(new Error('Not enough seats available'));
    } else {
      await reserveSeat(newSeats);
      if (newSeats === 0) reservationEnabled = false;
      done();
    }
  });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

export default app;
