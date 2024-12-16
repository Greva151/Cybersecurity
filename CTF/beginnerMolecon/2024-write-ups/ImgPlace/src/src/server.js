import express, { urlencoded } from "express";
import session from "express-session";
import crypto from "crypto";
import postgres from "postgres";
import cookieParser from "cookie-parser";
import { createChallenge, verifySolution } from "altcha-lib";
import { CHALLENGE_HOST, FLAG, visitUrl } from "./visit_url.js";

const app = express();

const sql = postgres(process.env.DB);

console.log("Waiting for db to be ready...");

while(true) {
    try {
        await sql`SELECT 1`;
        console.log("Connected!");
        break;
    } catch {
        console.log("Retrying in 2 seconds...");
        await new Promise(r => setTimeout(r, 2000));
    }
} 
const photos = [
    "img/01.jpg",
    "img/02.jpg",
    "img/03.jpg",
    "img/04.jpg",
    "img/05.jpg",
    "img/06.jpg",
    "img/07.jpg",
    "img/08.jpg",
    "img/09.jpg",
    "img/10.jpg",
];

await sql`CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)`;

await sql`CREATE TABLE IF NOT EXISTS images(
  id SERIAL PRIMARY KEY,
  src TEXT NOT NULL, 
  description TEXT NOT NULL,
  owner TEXT NOT NULL,
  FOREIGN KEY(owner) REFERENCES users(username)
);`

await sql`INSERT INTO users (username, password) VALUES ('admin', ${crypto.randomBytes(14).toString("hex")}) ON CONFLICT DO NOTHING`

const powKey = crypto.randomBytes(16).toString("hex");

app.use(cookieParser());
app.use(urlencoded({ extended: true }));
app.set("trust proxy", 1);
app.use(express.static("static"));
app.set("view engine", "ejs");

app.use(session({
    secret: crypto.randomBytes(16).toString("hex"),
    resave: false,
    saveUninitialized: true,
    cookie: {},
}));

app.use((req, res, next) => {
    if (
        !req.session.username && req.cookies && req.cookies.flag &&
        req.cookies.flag === FLAG
    ) {
        req.session.username = "admin";
        req.session.save();
    }
    next();
});

app.get("/", function (req, res) {
    if (!req.session.username) {
        res.render("login", { session: req.session, alert: null });
        return;
    }

    res.render("home", { session: req.session, photos });
});

app.post("/", async (req, res) => {

    if (!req.body.username || !req.body.password) {
        res.render("login", { session: req.session, alert: "Invalid body" });
        return;
    }

    const row = await sql`SELECT * FROM users WHERE username = ${String(req.body.username)} AND password = ${String(req.body.password)}`;

    if (row.length > 0 && row[0].id) {
        req.session.username = String(req.body.username);
        req.session.save();
        res.render("home", { session: req.session, photos });
    } else {
        res.render("login", {
            session: req.session,
            alert: "Invalid username or password!",
        });
    }
});

app.get("/register", (req, res) => {
    if (req.session.username) {
        res.redirect("/");
        return;
    }

    res.render("register", { session: req.session, alert: null });
});

app.post("/register", async (req, res) => {
    if (req.session.username) {
        res.redirect("/");
        return;
    }

    if (!req.body.username || !req.body.password || !req.body.confirmPassword) {
        res.statusCode = 400;
        res.render("register", { session: req.session, alert: "Invalid body" });
        return;
    }

    const username = String(req.body.username);
    const password = String(req.body.password);
    const confirmPassword = String(req.body.confirmPassword);

    if (username.length > 16) {
        res.statusCode = 400;
        res.render("register", {
            session: req.session,
            alert: "Username must be at max 16 chars long",
        });
        return;
    }

    if (password.length > 16) {
        res.statusCode = 400;
        res.render("register", {
            session: req.session,
            alert: "Password must be at max 16 chars long",
        });
        return;
    }

    if (confirmPassword !== password) {
        res.statusCode = 400;
        res.render("register", {
            session: req.session,
            alert: "Password do not match!",
        });
        return;
    }

    const row = await sql`SELECT * FROM users WHERE username = ${username}`;

    if (row.length>0 && row[0].id) {
        res.statusCode = 400;
        res.render("register", {
            session: req.session,
            alert: "This username is already taken!",
        });
        return;
    }

    await sql`INSERT INTO users (username, password) VALUES (${username}, ${password})`;

    res.render("login", {
        session: req.session,
        alert: "Registration successful, please log in!",
    });
});

app.get("/profile", async (req, res) => {
    if (!req.session.username) {
        res.redirect("/");
        return;
    }

    const images = await sql`SELECT * FROM images WHERE owner = ${req.session.username}`;

    res.render("profile", {
        username: req.session.username,
        session: req.session,
        images,
    });
});

app.get("/new", (req, res) => {
    if (!req.session.username) {
        res.redirect("/");
        return;
    }

    res.render("new", {
        username: req.session.username,
        session: req.session,
        alert: null,
        descr: "",
        url: "",
    });
});

app.post("/new", async (req, res) => {
    if (!req.session.username) {
        res.redirect("/");
        return;
    }

    if (!req.body.url || !req.body.description) {
        res.statusCode = 400;
        res.render("new", {
            session: req.session,
            alert: "Invalid body",
            descr: "",
            url: "",
        });
        return;
    }

    const url = String(req.body.url);
    const description = String(req.body.description);

    if (!url.startsWith("https://") && !url.startsWith("http://")) {
        res.statusCode = 400;
        res.render("new", {
            session: req.session,
            alert: "You must put a valid url!",
            url: url,
            descr: description,
        });
        return;
    }

    await sql`INSERT INTO images (src, description, owner) VALUES (${url}, ${description}, ${req.session.username});`

    res.redirect("/profile");
});

app.get("/pic/:id", (req, res) => {
    if (!req.session.username) {
        res.redirect("/");
        return;
    }

    const id = parseInt(req.params.id);

    if (isNaN(id)) {
        res.redirect("/");
        return;
    }

    res.render("pic", {
        username: req.session.username,
        session: req.session,
        id: id,
    });
});

app.get("/api/pic/:id", async (req, res) => {
    if (!req.session.username) {
        res.redirect("/");
        return;
    }

    const id = parseInt(req.params.id);

    if (isNaN(id)) {
        res.redirect("/");
        return;
    }

    let image = await sql`SELECT * FROM images WHERE id = ${id}`

    if (image.length == 0 || !image[0].id) {
        res.statusCode = 404;
        res.json({
            message: "Not Found",
        });
        return;
    }

    image = image[0];

    if (
        image.owner !== req.session.username && req.session.username !== "admin"
    ) {
        res.statusCode = 401;
        res.json({
            message: "Unauthorized",
        });
        return;
    }

    res.json({
        id: image.id,
        src: image.src,
        description: image.description,
    });
});

function getRandomArbitrary(min, max) {
    return Math.floor(Math.random() * (max - min) + min);
}

app.get("/api/pow", async (req, res) => {
    if (!req.session.username) {
        res.redirect("/");
        return;
    }

    const expires = new Date();
    expires.setSeconds(expires.getSeconds() + 60);

    const num = getRandomArbitrary(5000000, 10000000)

    console.log(`Generated POW ${num}`)

    const challenge = await createChallenge({
        hmacKey: powKey,
        expires: expires,
        params: {
            ip: req.ip,
        },
        number: num,
        maxnumber: 10000000
    });

    return res.json(challenge);
});

app.post("/api/proposals", async (req, res) => {
    if (!req.session.username) {
        res.redirect("/");
        return;
    }

    if (!req.body.id || !req.body.pow) {
        res.statusCode = 400;
        res.json({
            message: "Bad Request",
        });
        return;
    }

    const id = parseInt(req.body.id);
    const pow = String(req.body.pow);

    if (isNaN(id)) {
        res.statusCode = 400;
        res.json({
            message: "Bad Request",
        });
        return;
    }

    let image = await sql`SELECT * FROM images WHERE id = ${id}`

    if (image.length == 0 || !image[0].id) {
        res.statusCode = 404;
        res.json({
            message: "Not Found",
        });
        return;
    }

    image = image[0];

    if (
        image.owner !== req.session.username && req.session.username !== "admin"
    ) {
        res.statusCode = 401;
        res.json({
            message: "Unauthorized",
        });
        return;
    }

    const check = await verifySolution(pow, powKey, true);

    if (!check) {
        res.statusCode = 406;
        res.json({
            message: "Invalid pow",
        });
        return;
    }

    await visitUrl(CHALLENGE_HOST + "pic/" + id);

    res.json({
        message: "ok",
    });
});

app.get("/logout", (req, res) => {
    req.session.destroy();
    res.redirect("/");
});

app.listen(3000, "0.0.0.0", () => {
    console.log("Listening on http://0.0.0.0:3000");
});
