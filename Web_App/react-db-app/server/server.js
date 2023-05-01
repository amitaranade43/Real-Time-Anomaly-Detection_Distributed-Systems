// const express = require('express');
// const cors = require('cors');
// const mysql = require('mysql');

// const app = express();

// const connection = mysql.createConnection({
//   host: 'db-mysql',
//   user: 'root',
//   password: 'root',
//   database: 'abnormal_db'
// });

// app.use(cors());

// app.get('/data', (req, res) => {
//   connection.query('SELECT * FROM abnormal_table', (error, results) => {
//     if (error) throw error;

//     res.send(results);
//   });
// });

// app.delete('/data/:id', (req, res) => {
//   const { id } = req.params;

//   // Retrieve the abnormal reading from abnormal_table
//   connection.query('SELECT temp, server_id FROM abnormal_table WHERE id = ?', [id], (error, result) => {
//     if (error) throw error;

//     // Insert the abnormal reading into abnormal_history
//     connection.query('INSERT INTO abnormal_history (temp, server_id) VALUES (?, ?)', [result[0].temp, result[0].server_id], (error, result) => {
//       if (error) throw error;

//       // Remove the abnormal reading from abnormal_table
//       connection.query('DELETE FROM abnormal_table WHERE id = ?', [id], (error, result) => {
//         if (error) throw error;

//         res.json({ message: `Entry with id ${id} has been deleted and added to abnormal_history` });
//         console.log(res);
//       });
//     });
//   });
// });


// app.get('/data/history', (req, res) => {
//   connection.query('SELECT * FROM abnormal_history', (error, results) => {
//     if (error) throw error;

//     res.json(results);
//     console.log(res);
//   });
// });




// app.listen(4000, () => {
//   console.log('Server started on port 4000');
// });


const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');

const app = express();

const pool = new Pool({
  user: 'postgres',
  password: 'root',
  host: 'db-postgres',
  port: 5432,
  database: 'postgres',
});

app.use(cors());

app.get('/data', (req, res) => {
  pool.query('SELECT * FROM abnormal_table', (error, results) => {
    if (error) throw error;

    res.send(results.rows);
  });
});

app.delete('/data/:id', (req, res) => {
  const { id } = req.params;

  // Retrieve the abnormal reading from abnormal_table
  pool.query('SELECT temp, server_id FROM abnormal_table WHERE id = $1', [id], (error, result) => {
    if (error) throw error;

    // Insert the abnormal reading into abnormal_history
    pool.query('INSERT INTO abnormal_history (temp, server_id) VALUES ($1, $2)', [result.rows[0].temp, result.rows[0].server_id], (error, result) => {
      if (error) throw error;

      // Remove the abnormal reading from abnormal_table
      pool.query('DELETE FROM abnormal_table WHERE id = $1', [id], (error, result) => {
        if (error) throw error;

        res.json({ message: `Entry with id ${id} has been deleted and added to abnormal_history` });
        console.log(res);
      });
    });
  });
});


app.get('/data/history', (req, res) => {
  pool.query('SELECT * FROM abnormal_history', (error, results) => {
    if (error) throw error;

    res.json(results.rows);
    console.log(res);
  });
});

app.listen(4000, () => {
  console.log('Server started on port 4000');
});
