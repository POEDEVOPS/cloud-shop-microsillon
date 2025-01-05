const { Client } = require('pg');
const express = require('express');
const path = require('path');

const app = express();
app.use(express.json());
const PORT = 3000;

// Serve static files from the public folder
app.use(express.static(path.join(__dirname, './website/')));
app.use('/avatars', express.static('./public/avatars'));
app.use('/covers', express.static('./public/covers'));


// website
app.get('/', (req, res) => res.sendFile(path.join(__dirname)));

// DB connect
const client = new Client({
  user: 'postgres',
  host: 'localhost',
  database: 'microsillon',
  password: '####PASSWORD####',
  port: 5432,
});

client.connect();


// start server
app.listen(PORT, function (err) {
    if (err) console.log(err);
    console.log(`Server listening on PORT ${PORT}`);
  });



// API SHOP
app.get('/shop', (req, res) => 
{
    client.query('SELECT * from shop', (err, result) => 
    {
        if (result.rows[0] === undefined)
        {
            res.send("401")
        }
        else
        {
            res.send(result.rows);
        }
    });
});


// API USERS
app.get('/users/:login/:password', (req, res) => 
    {
        let login = req.params.login;
        let pass = req.params.password;
        console.log(login + "," + pass);
        query = `SELECT id, login, role,avatar, orders from users where login='${login}' and password='${pass}';`;
        client.query(query, (err, result) => 
        {
            if (result.rows[0] === undefined)
            {
                res.send("401")
            }
            else
            {
                res.send(result.rows[0]);
            }
        });
    });

// API ALBUMS
app.get('/albums', (req, res) => 
{
    query = `select * from albums inner join artists on albums.artist_id = artists.id;`
    client.query(query, (err, result) => 
    {
        if (result.rows[0] === undefined)
        {
            res.send("500")
        }
        else
        {
            res.send(result.rows);
        }
    });
});

// UPDATE STOCK
app.put('/albums', (req, res) => {
    const addStock = req.body.addtostock;
    const albumId = req.body.id;
    query = `select stock from albums where id=${albumId};`
    client.query(query, (err, result) => 
    {
        if (result.rows[0] === undefined)
        {
            res.send("500")
        }
        else
        {
            let currentStock = parseInt(result.rows[0].stock);
            let newStock = currentStock + addStock;
            if (newStock < 0)
            {
                res.send("403");
            }
            else
            {
                query = `UPDATE albums SET stock=${newStock} where id = ${albumId};`;
                client.query(query, (err, result) => 
                {
                    if (err)
                    {
                        res.send("500")
                    }
                    else
                    {
                        res.send("200");
                    }
                });
            }
        }
    });
});

// API ARTISTS
app.get('/artists', (req, res) => 
    {
        query = `select id, name from artists;`
        client.query(query, (err, result) => 
        {
            if (result.rows[0] === undefined)
            {
                res.send("500")
            }
            else
            {
                res.send(result.rows);
            }
        });
    });

