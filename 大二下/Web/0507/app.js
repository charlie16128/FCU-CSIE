import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import cookieParser from 'cookie-parser';
import logger from 'morgan';
import sqlite3 from 'sqlite3';

import indexRouter from './routes/index.js';
import usersRouter from './routes/users.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 初始化資料庫連線
const dbPath = path.join(__dirname, 'db', 'sqlite.db');
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('在 app.js 中無法開啟資料庫:', err.message);
    } else {
        console.log('在 app.js 中成功連接到 SQLite 資料庫: db/sqlite.db');
    }
});

var app = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);

// 查詢所有電影台詞資料的 API 路由
app.get('/api/quotes', (req, res) => {
    const sql = "SELECT * FROM movie_quotes";
    db.all(sql, [], (err, rows) => {
        if (err) {
            res.status(400).json({ "error": err.message });
            return;
        }
        res.json({
            "message": "success",
            "data": rows
        });
    });
});

// 根據台詞提供者篩選資料的 API 路由
app.get('/api', (req, res) => {
    const provider = req.query.provider;
    if (!provider) {
        res.status(400).json({ "error": "請提供 provider 參數" });
        return;
    }

    const sql = "SELECT * FROM movie_quotes WHERE provider = ?";
    db.all(sql, [provider], (err, rows) => {
        if (err) {
            res.status(400).json({ "error": err.message });
            return;
        }

        // 檢查是否有找到任何資料
        if (rows.length === 0) {
            res.status(404).json({
                "status": "fail",
                "message": `找不到來自 '${provider}' 的台詞資料`
            });
            return;
        }

        res.json({
            "message": "success",
            "provider": provider,
            "data": rows
        });
    });
});

// 新增資料
app.get('/api/insert', (req, res) => {
    let provider = req.query.provider;
    let movie_name = req.query.movie_name;
    let quote = req.query.quote;

    let sql = 'INSERT INTO movie_quotes (provider, movie_name, quote, votes) VALUES (?, ?, ?, 0)';

    db.run(sql, [provider, movie_name, quote], function (err) {
        if (err) {
            console.error(err.message);
            res.status(500).json({ error: 'Internal Server Error' });
            return;
        }
        
        // 查詢所有資料並回傳
        db.all('SELECT * FROM movie_quotes', [], (err, rows) => {
            if (err) {
                return res.status(500).json({ error: '查詢資料庫失敗' });
            }
            res.json({
                message: 'Insert success',
                data: rows
            });
        });
    });
});

// 取得所有台詞資料
app.get('/api/quotes', (req, res) => {
    const sql = 'SELECT * FROM movie_quotes';
    db.all(sql, [], (err, rows) => {
        if (err) {
            console.error(err.message);
            res.status(500).json({ error: 'Internal Server Error' });
            return;
        }
        res.json(rows);
    });
});

export default app;